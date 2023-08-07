from scilightcon.datasets import _load_zipped_csv_data

data_file_name = r'C:\Code\lightcon-scipack\scilightcon\datasets\data\data_test_detect_peaks.csv.gz'
data, header = _load_zipped_csv_data(data_file_name)


# Code for compressing a file with gzip
# input_file= r"C:\Code\lightcon-scipack\scilightcon\datasets\data\data_test_detect_peaks.csv"
# def compress_file(input_filename, output_filename):
#     with open(input_filename, 'rb') as fille_in:
#         with gzip.open(output_filename, 'wb') as fille_out:
#             shutil.copyfileobj(fille_in, fille_out)
# compress_file(input_file, compresed_file)
# print(compress_file)
