# Changelog

This the log of changes to [QuasarNP](https://github.com/desihub/QuasarNP).

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - Unreleased

## [0.2.0] - 2024-05-01
This release significantly changes the QuasarNP API in a way that **is not** backwards compatible.
### Added
- [#8310be5e] `load_model` and `load_file` now auto derive whether the QuasarNP model
represented by the weights file uses a linear or a logarithmic grid. By default
the function assumes the default QuasarNET logarithmic grid.
- [#a546c2e7] A post processing script,
`scripts/post_process_weights.py` is provided that can embed either the default
QuasarNET logarithmic grid or the QuasarNET linear grid directly into a weights
file in the way that these functions expect.


### Changed
- [#c629d43c] `load_desi_*` now accepts an arbitrary input grid instead of a boolean for linear grids.
This means that instead of passing `linear=True` to load to a linear QuasarNET grid the user must
explicitly pass the linear grid. The default is to use the logarithmic grid.
- [#b0a79e65] `regrid`, `rebin` and other associated functions now also accept arbitrary grids
and not a boolean. Note that these will fail on "unusual" grids, i.e. all arbitrary output
grids must have either constant linear or constant logarithmic spacing.
- [various] Unit tests are added or updated to reflect the various API changes.

## [0.1.6] - 2024-04-30
### Added
- [#9500d28e] Added an option to use a linear QuasarNET grid.
- [#3a279e4a] Added unit test for regridding to a linear grid.
- [#1816846f] Added unit test for rebinning to a linear grid.

### Changed


## [0.1.5] - 2022-09-08
### Added
- [#1a063232] Added unit test to catch the bug fixed in [#a7621bb1]

### Changed
- [#a7621bb1] Fixed a bug where models with $n\neq4$ layers would use the wrong
batch normalization weights in the fully connected layer.
- [#2a6d6395] Removed all lambda functions and replaced them with partial functions or
full functions to enable pickling of QuasarNP objects. This is necessary for
multiprocessing purposes.


## [0.1.4] - 2022-07-20
### Added
- [#b5562d69] Add `read_spall` from QuasarNET.
- [#5372189d] Tests for rebinning spectra.
- [#79cc5e48] `conv1d` can now accept two different padding modes.


### Changed
- [#acd75825] Renormalizing spectra is now its own function (`utils.renormalize`)
- [#e37dcde3] Rebin now also works on eBOSS data, not just DESI data.
- [#c4dd52c6] `load_model` and `load_file` now dynamically determine the number
of convolution layers in the trained model.
- [#7e3f7141] `load_model` and `load_file` now dynamically determine the padding mode
and stride of each convolution layer

## [0.1.3] - 2021-10-04
### Added
- Unit tests.

### Changed
- Fix PEP-8 style errors in layers.py.

## [0.1.2] - 2021-07-12
### Changed
- Fix a bug with `rows == None` sometimes not working as intended, and instead
use `rows is None`
- Fix PEP-8 style errors in io.py.


## [0.1.1] - 2021-06-04
### Added
- Add version string.
- Add Sphinx docfiles.

## [0.1.0] - 2021-05-26
Initial release.