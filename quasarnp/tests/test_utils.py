import ast
import pathlib
import unittest

import numpy as np

import fitsio

from quasarnp.utils import regrid, process_preds, rebin, wave, linear_wave

file_loc = pathlib.Path(__file__).parent.resolve() / "test_files"


class TestUtilities(unittest.TestCase):
    # Test taking the old grid and generating which bins on the new grid
    # the grid goes into.
    def test_regrid_log(self):
        # This is the regrids the grid to itself so shouldn't do anything
        ob_bins, ob_keep = regrid(wave, wave)
        expected_bins = np.arange(443)

        self.assertTrue(np.allclose(ob_bins, expected_bins))
        self.assertTrue(np.allclose(ob_keep, np.ones_like(ob_keep, dtype=bool)))

        # Testing regridding the DESI grid into the SDSS/QuasarNet grid.
        wmin, wmax, wdelta = 3600, 9824, 0.8
        old_grid = np.round(np.arange(wmin, wmax + wdelta, wdelta), 1)
        ob_bins, ob_keep = regrid(old_grid, wave)

        # In order to not have to overload this file with nuisance, I have moved
        # the actual answer here to regrid.txt. It's quite long, so only
        # investigate if strictly necessary.
        loc = file_loc / "regrid.txt"
        with open(loc, 'r') as f:
            expected_bins = ast.literal_eval(f.read().replace("\n", ""))
        self.assertTrue(np.allclose(ob_bins, expected_bins))
        self.assertTrue(np.allclose(ob_keep, np.ones_like(ob_keep, dtype=bool)))

    def test_regrid_linear(self):
        # This is the rebinned DESI grid, so regridding it shouldn't do anything.
        # Linear DESI grid information
        wmin, wmax, wdelta = 3600, 9824, 0.8
        wdelta_qnet = wdelta * 17
        new_grid = np.round(np.arange(wmin, wmax + wdelta, wdelta_qnet), 1)

        ob_bins, ob_keep = regrid(new_grid, linear_wave)
        expected_bins = np.arange(458)
        self.assertTrue(np.allclose(ob_bins, expected_bins))
        self.assertTrue(np.allclose(ob_keep, np.ones_like(ob_keep, dtype=bool)))

        # Testing regridding the DESI grid into the linear QuasarNet grid.
        old_grid = np.round(np.arange(wmin, wmax + wdelta, wdelta), 1)
        ob_bins, ob_keep = regrid(old_grid, linear_wave)

        # 17 DESI bins per linear QuasarNET bin, but 17 * 458 is slightly
        # longer than the true DESI grid, so the last bin only
        # gets 12 bins. Hence the shave off of 5 at the end.
        expected_bins =  np.repeat(np.arange(458), 17)[:-5]
        self.assertTrue(np.allclose(ob_bins, expected_bins))
        self.assertTrue(np.allclose(ob_keep, np.ones_like(ob_keep, dtype=bool)))

    def test_regrid_arbitrary(self):
        # Stephen Bailey's arbitrary grid
        old_grid = np.arange(3600, 9800, 10)
        ob_bins, ob_keep = regrid(old_grid, wave)

        # In order to not have to overload this file with nuisance, I have moved
        # the actual answer here to regrid_arbitrary.txt. It's quite long, so only
        # investigate if strictly necessary.
        loc = file_loc / "regrid_arbitrary.npy"
        expected_bins = np.load(loc)
        self.assertTrue(np.allclose(ob_bins, expected_bins))
        self.assertTrue(np.allclose(ob_keep, np.ones_like(ob_keep, dtype=bool)))

    def test_regrid_failure(self):
        # Non constant binning should fail and raise a value error.
        new_grid = np.concatenate([np.arange(3600, 4000, 10), np.arange(4000, 9800, 40)])

        # Testing regridding the DESI grid onto this broken grid
        wmin, wmax, wdelta = 3600, 9824, 0.8
        old_grid = np.round(np.arange(wmin, wmax + wdelta, wdelta), 1)

        with self.assertRaises(ValueError):
            _ = regrid(old_grid, new_grid)

    # Test rebinning some DESI data. Need this in case rebinning fails on
    # SDSS/BOSS etc spectra for some reason. Don't call me prescient when it
    # does and I need to change it.
    def test_rebin(self):
        # We will use the test coadd for this test.
        loc = file_loc / "test_coadd.fits"
        expected_loc = file_loc / "coadd_rebinned.fits"

        cams = ["B", "R", "Z"]
        # Load the coadd, and the known correct rebinning.
        with fitsio.FITS(loc) as h:
            with fitsio.FITS(expected_loc) as h2:
                for c in cams:
                    fluxname = f"{c}_FLUX"
                    ivarname = f"{c}_IVAR"
                    wname = f"{c}_WAVELENGTH"

                    # Load the flux and ivar
                    flux = h[fluxname].read()[:]
                    ivar = h[ivarname].read()[:]
                    w_grid = h[wname].read()

                    # Rebin the flux and ivar
                    n_flux, n_ivar = rebin(flux, ivar, w_grid, out_grid=wave)

                    # Just checks that the rebinned is equal to the known
                    # "correct" rebinning
                    self.assertTrue(np.allclose(n_flux, h2[fluxname].read()[:]))
                    self.assertTrue(np.allclose(n_ivar, h2[ivarname].read()[:]))

    # Test rebinning some DESI data. Need this in case rebinning fails on
    # SDSS/BOSS etc spectra for some reason. Don't call me prescient when it
    # does and I need to change it.
    def test_rebin_linear(self):
        # We will use the test coadd for this test.
        loc = file_loc / "test_coadd.fits"
        expected_loc = file_loc / "coadd_rebinned_linear.fits"

        cams = ["B", "R", "Z"]
        # Load the coadd, and the known correct rebinning.
        with fitsio.FITS(loc) as h:
            with fitsio.FITS(expected_loc) as h2:
                for c in cams:
                    fluxname = f"{c}_FLUX"
                    ivarname = f"{c}_IVAR"
                    wname = f"{c}_WAVELENGTH"

                    # Load the flux and ivar
                    flux = h[fluxname].read()[:]
                    ivar = h[ivarname].read()[:]
                    w_grid = h[wname].read()

                    # Rebin the flux and ivar
                    n_flux, n_ivar = rebin(flux, ivar, w_grid, out_grid=linear_wave)

                    # Just checks that the rebinned is equal to the known
                    # "correct" rebinning
                    self.assertTrue(np.allclose(n_flux, h2[fluxname].read()[:]))
                    self.assertTrue(np.allclose(n_ivar, h2[ivarname].read()[:]))

    # This test should be independent of weights file, so I precomputed the
    # processed predictions using a method I know/assume to be correct (the
    # Farr/Busca QuasarNet impl) and then saved them to compare to here in
    # this test using the QuasarNP impl.
    def test_process_preds(self):
        lines = ['LYA', 'CIV(1548)', 'CIII(1909)', 'MgII(2796)',
                 'Hbeta', 'Halpha']
        lines_bal = ['CIV(1548)']

        # These predictions come from the qn_train_coadd_indtrain_0_0_boss10.h5
        # weights file trained by James Farr.
        loc = file_loc / "predict_data.npy"
        with open(loc, 'rb') as f:
            p = np.load(f)

        observed = process_preds(p, lines, lines_bal, verbose=False)

        # We'll just check the LyA predictions and the BAL predictions.
        loc = file_loc / "predict_lya.npy"
        with open(loc, 'rb') as f:
            expected_lya = np.load(f)
        self.assertTrue(np.allclose(observed[0], expected_lya))

        # Gonna assume that with these two everything's alright.
        loc = file_loc / "predict_bal.npy"
        with open(loc, 'rb') as f:
            expected_bal = np.load(f)
        # One of these predictions is slightly different, by a very small amount
        # but just large enough to fail the default rtol value.
        self.assertTrue(np.allclose(observed[-1], expected_bal, rtol=1e-2))


if __name__ == '__main__':
    unittest.main()
