# scilightcon Change Log

## [0.4.1] 2026-08-27
### Added
- External spectra importer for Thorlabs, Edmund Optics, Chroma, Eksma and
generic CSV spectra with cataloging into the dataset module based on spectrum
type
- CSV data extractor from MATLAB Figures
- New transmission and reflection spectra from Thorlabs, Edumund Optics and
Chroma
- New Emitters dataset with absorption and emission spectra for Eosin, NADH,
FAD, GCaMP6f, mChery and tdTomato

### Changed
- interpolate_and_multiply() now works on Tuples of Lists and ndarrays

## [0.3.2] 2024-07-25
### Changed
- Removed log parsing time range granularity by day in scilightcon.datasets.LogsReader

## [0.3.1] 2024-07-17
### Fixed
- lightcon.plot styling routines error, when PIL >= 9.5 used