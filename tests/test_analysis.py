import unittest

import matplotlib.pyplot as plt
import numpy as np
import scipy

import nmraspecds.dataset
import nmraspecds.metadata
import nmraspecds.io
import nmraspecds.analysis


class TestChemicalShiftCalibration(unittest.TestCase):
    def setUp(self):
        self.calibration = nmraspecds.analysis.ChemicalShiftCalibration()
        self.dataset = nmraspecds.dataset.ExperimentalDataset()
        self.data = scipy.signal.windows.gaussian(99, std=2)
        self.axis = np.linspace(0, 30, num=99)

    def _create_dataset(self):
        self.dataset.data.data = self.data
        self.dataset.data.axes[0].values = self.axis

    def _import_dataset(self):
        importer = nmraspecds.io.BrukerImporter()
        importer.source = "/home/mirjam/Daten/NMR/231106_Adamantane_Ref_4mm/1"
        self.dataset.import_from(importer)

    def test_instantiate_class(self):
        pass

    def test_has_appropriate_description(self):
        self.assertIn(
            "chemical shift offset",
            self.calibration.description.lower(),
        )

    def test_without_standard_and_chemical_shift_raises(self):
        self.calibration.parameters["spectrometer_frequency"] = 400.1
        with self.assertRaisesRegex(ValueError, "standard or chemical shift"):
            self.dataset.analyse(self.calibration)

    def test_with_standard_without_nucleus_raises(self):
        self.calibration.parameters["standard"] = "adamantane"
        with self.assertRaisesRegex(ValueError, "nucleus"):
            self.dataset.analyse(self.calibration)

    def test_get_offset_with_transmission_and_spectrometer_frequency_equal(
        self,
    ):
        self.dataset.data.data = self.data
        self.dataset.data.axes[0].values = self.axis
        self.dataset.metadata.experiment.spectrometer_frequency.from_string(
            "400.0000 MHz"
        )
        nucleus = nmraspecds.metadata.Nucleus()
        nucleus.base_frequency.from_string("400.00000 MHz")
        self.dataset.metadata.experiment.add_nucleus(nucleus)
        self.calibration.parameters["chemical_shift"] = 13
        analysis = self.dataset.analyse(self.calibration)
        self.assertAlmostEqual(analysis.result, 800.0, 3)

    def test_get_offset_with_transmission_and_spectrometer_frequency_different(
        self,
    ):
        self.dataset.data.data = self.data
        self.dataset.data.axes[0].values = (
            self.axis + 50 / 400
        )  # accounts for the offset of the base frequency
        self.dataset.metadata.experiment.spectrometer_frequency.from_string(
            "400.0 MHz"
        )
        nucleus = nmraspecds.metadata.Nucleus()
        nucleus.base_frequency.from_string("400.00005 MHz")
        self.dataset.metadata.experiment.add_nucleus(nucleus)
        self.calibration.parameters["chemical_shift"] = 17
        analysis = self.dataset.analyse(self.calibration)
        self.assertAlmostEqual(analysis.result, -800, 3)

    def test_perform_with_one_signal_returns_correct_value(self):
        """Only valid if reference signal is the one at the global maximum."""
        self._import_dataset()
        self.calibration.parameters["chemical_shift"] = 1.8
        analysis = self.dataset.analyse(self.calibration)
        self.assertTrue(analysis.result)
        self.assertAlmostEqual(analysis.result, -1439.44, -2)

    def test_nucleus_is_accounted_for(self):
        self.dataset.data.data = self.data
        self.dataset.data.axes[0].values = self.axis + 50 / 400
        self.dataset.metadata.experiment.spectrometer_frequency.from_string(
            "400.0 MHz"
        )
        nucleus = nmraspecds.metadata.Nucleus()
        nucleus.base_frequency.from_string("400.00005 MHz")
        nucleus.type = "13C"
        self.dataset.metadata.experiment.add_nucleus(nucleus)
        self.calibration.parameters["standard"] = "adamantane"
        analysis = self.dataset.analyse(self.calibration)
        self.assertAlmostEqual(analysis.parameters["chemical_shift"], 37.77)

    def test_chooses_correct_standard(self):
        self._import_dataset()
        self.calibration.parameters["standard"] = "adamantane"
        analysis = self.dataset.analyse(self.calibration)
        self.assertAlmostEqual(analysis.parameters["chemical_shift"], 1.8)

    def test_analysis_has_return_type_and_defaults_to_value(self):
        self.assertIn("return_type", self.calibration.parameters)
        self.assertEqual(self.calibration.parameters["return_type"], "value")

    def test_return_type_is_dict(self):
        self._import_dataset()
        self.calibration.parameters["standard"] = "adamantane"
        self.calibration.parameters["return_type"] = "dict"
        analysis = self.dataset.analyse(self.calibration)
        self.assertIsInstance(analysis.result, dict)

    def test_return_dict_contains_nucleus(self):
        self._import_dataset()
        self.calibration.parameters["standard"] = "adamantane"
        self.calibration.parameters["return_type"] = "dict"
        analysis = self.dataset.analyse(self.calibration)
        self.assertEqual(analysis.result["nucleus"], "1H")

    def test_deals_with_standard_with_three_peaks(self):
        importer = nmraspecds.io.BrukerImporter()
        importer.source = (
            "/home/mirjam/Daten/NMR/230508_Referencing_1p3mm_Alanine/10"
        )
        self.dataset.import_from(importer)
        self.calibration.parameters["standard"] = "alanine"
        analysis = self.dataset.analyse(self.calibration)
        self.assertAlmostEqual(analysis.parameters["chemical_shift"], 178, -2)
        self.assertAlmostEqual(analysis.result, 51.92, -1)
