from _external_spectra_parser import thorlabs_xls_to_csv, edumund_optics_xls_to_csv, chroma_txt_to_csv, emitter_txt_to_csv
import matplotlib.pyplot as plt
import sys
from pathlib import Path

VENDORS = ['Thorlabs', 'Edmund Optics', 'Chroma', 'Fluor. Emitter']
OPTIC_OPTIONS = ['trans', 'refl']
EMITTER_OPTIONS = ['ex', 'em', '2pex']

def choose_type(prompt, options):
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        raw = input(f"{prompt} (1-{len(options)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("Invalid choice.")

file_names = None
if __name__ == '__main__':
    if file_names is None and len(sys.argv) == 1:
        print("=== scilightcon spectrum importer ===")
        print("\nThis script imports spectra into scilightcon's datset module."
        "Thorlabs XLS, Edmund XLSX, Chroma TXT, and generic "
        "fluorophoreluminophore absorption/emission CSV spectra are supported."
        "\nThis script should be run on a build machine to update the database"
        "and then the database is commited to repo."
        "\nUsage:"
        "\t{Path(sys.argv[0]).name} <file1> <file2> ... <fileN>"
        "\tYou can also drag and drop one or more input files onto the script .py file")
    else:
        plt.figure()
        if file_names is None:
            file_names = sys.argv[1:]

        print("Importing files:")
        for file_name in file_names:
            print(f"\t{Path(file_name).name}")
        print("\n")

        vendor = choose_type("Select vendor", VENDORS)

        if vendor == 'Fluor. Emitter':
            mode = choose_type("Select spectrum type", EMITTER_OPTIONS)
        else:
            mode = choose_type("Select spectrum type", OPTIC_OPTIONS)
        
        for file_name in file_names:
            try:
                if vendor == 'Thorlabs':
                    wavl, trans = thorlabs_xls_to_csv(file_name, mode=mode)
                elif vendor == 'Edmund Optics':
                    wavl, trans = edumund_optics_xls_to_csv(file_name, mode=mode)
                elif vendor == 'Chroma':
                    wavl, trans = chroma_txt_to_csv(file_name, mode=mode)
                elif vendor == 'Fluor. Emitter':
                    wavl, trans = emitter_txt_to_csv(file_name, mode=mode)
                else:
                    raise RuntimeError(f"Unhandled vendor {vendor}")

                plt.plot(wavl, trans, label=Path(file_name).name)
            except Exception as excpt:
                print(f"Could not import {Path(file_name).name}. Reason: {excpt}")

        plt.xlabel('Wavelength')
        plt.ylabel('Transmission')
        plt.legend()
        plt.grid(True)
        plt.show()


