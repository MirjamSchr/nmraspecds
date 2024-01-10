import unittest

import matplotlib.pyplot as plt
import numpy as np
import scipy

import nmraspecds.dataset
import nmraspecds.io
from nmraspecds import analysis


class TestChemicalShiftCalibration(unittest.TestCase):
    def setUp(self):
        self.chemical_shift_calibration = analysis.ChemicalShiftCalibration()
        self.dataset = nmraspecds.dataset.ExperimentalDataset()
        self.data = scipy.signal.windows.gaussian(99, std=2)
        self.axis = np.linspace(0,30,num=99)



    def test_instantiate_class(self):
        pass

    def test_has_appropriate_description(self):
        self.assertIn('chemical shift offset',
                      self.chemical_shift_calibration.description.lower())

    def test_perform_without_spectrometer_frequency_raises(self):
        with self.assertRaisesRegex(ValueError, 'spectrometer frequency'):
            self.dataset.analyse(self.chemical_shift_calibration)

    def test_without_standard_and_chemical_shift_raises(self):
        self.chemical_shift_calibration.parameters['spectrometer_frequency'] \
            = 400.1
        with self.assertRaisesRegex(ValueError, 'standard or chemical shift'):
            self.dataset.analyse(self.chemical_shift_calibration)

    def test_set_new_frequency(self):
        self.dataset.data.data = self.data
        self.dataset.data.axes[0].values = self.axis
        self.dataset.metadata.experiment.spectrometer_frequency.from_string(
            '400 MHz')
        frequency_before = (
            self.dataset.metadata.experiment.spectrometer_frequency.value)
        self.chemical_shift_calibration.parameters['chemical_shift'] = 17
        self.dataset.analyse(self.chemical_shift_calibration)
        frequency_after = (
            self.dataset.metadata.experiment.spectrometer_frequency.value)
        self.assertNotEqual(frequency_before, frequency_after)

    def test_axis_is_adapted(self):
        self.dataset.data.data = self.data
        self.dataset.data.axes[0].values = self.axis
        self.dataset.metadata.experiment.spectrometer_frequency.from_string(
            '400 MHz')
        self.chemical_shift_calibration.parameters['chemical_shift'] = 17
        self.dataset.analyse(self.chemical_shift_calibration)
        ppm_at_maximum = self.dataset.data.axes[0].values[np.argmax(
            self.dataset.data.data)]
        self.assertEqual(ppm_at_maximum, 17.)

    def test_perform_with_one_signal_returns_correct_value(self):
        """Only valid if reference signal is the one at the global maximum."""
        importer = nmraspecds.io.BrukerImporter()
        importer.source = 'testdata/Adamantane/1/pdata/1'
        self.dataset.import_from(importer)
        self.chemical_shift_calibration.parameters['chemical_shift'] = 1.33
        analysis = self.dataset.analyse(self.chemical_shift_calibration)
        self.assertTrue(analysis.result)
        self.assertAlmostEqual(analysis.result, 2.3307,3)
