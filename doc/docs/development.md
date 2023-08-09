## Preparation

- Install Python 3.11 and `pip`
- Run `./build_tools/prepare.ps1` from root folder.

## Building package on local machine
Run `pip install -e ./` from root folder.

### Testing
Run `./build_tools/run_tests.ps1` from root folder.

### Preview the documentation

Make sure you're in the `doc` directory:

```console
$ mkdocs serve
INFO     -  Building documentation...
INFO     -  Cleaning site directory
INFO     -  Documentation built in 0.31 seconds
INFO     -  [12:07:03] Watching paths for changes: 'docs', 'mkdocs.yml', 'C:\code\lightcon-scipack\scilightcon'
INFO     -  [12:07:03] Serving on http://127.0.0.1:8000/
```

Open up `http://127.0.0.1:8000/` in your browser, and you'll see the documentation page being displayed.

### Build the documentation

Make sure you're in the `doc` directory:

```bash
mkdocs build
```

This will create a new directory, named `site`. Open `index.html` from there.



## General

- Do not create new modules
- All methods and classes:
    - must be referenced in the `__init__.py` file of the corresponding module
    - must be added to `__all__` list in `__init__.py`
    - must have a corresponding unit test
    - must be documented and documentation must contain use example

### Style guide

- Use [Google Style Guide](https://google.github.io/styleguide/) for coding
- Comment methods, classes using [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)


### Unit tests

Unit tests are prepared with `pytest`

## Roadmap

- [datasets] Add spectra of Light Conversion devices to scilightcon
- [plot] fancy hist() – granularity detection, autoranging, lin/log, vertical/horizontal
- [signals] fancy fft() – calculate FFT with absolute X and Y axis values dBm, dBc/Hz,etc.
- [datasets] Reflection coefficient dependence on wavelength for different popular mirror types at 45deg
- [datasets] Big file reader (chunk-based BIN/CSV file reader that can work inside ZIP files)
- [plot] export_figure – generate PNG and PDF at consistent and correct DPI
- [plot] imshow_ex – image panel with adjacent profile and/or histogram panels
- [signals] Single-call curve smoothing, data reduction tool (SG, FFT, occurrence plot)
- [optics] Time-bandwidth calculator

