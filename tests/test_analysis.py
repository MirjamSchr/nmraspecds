import copy
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
        importer.source = "testdata/Adamantane/1"
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

    def test_with_no_standard_and_chemical_shift_is_zero_does_not_raise(self):
        self._create_dataset()
        self.calibration.parameters["spectrometer_frequency"] = 400.1
        self.calibration.parameters["chemical_shift"] = 0
        nucleus = nmraspecds.metadata.Nucleus()
        nucleus.base_frequency.from_string("400.00000 MHz")
        self.dataset.metadata.experiment.add_nucleus(nucleus)
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

    def test_nucleus_is_accounted_for_in_dataset(self):
        self._import_dataset()
        self.calibration.parameters["chemical_shift"] = 1.8
        self.calibration.parameters["return_type"] = "dict"
        analysis = self.dataset.analyse(self.calibration)
        self.assertIsInstance(analysis.result, dict)
        self.assertEqual(analysis.result["nucleus"], "1H")

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

    @unittest.skip
    def test_deals_with_standard_with_three_peaks(self):
        importer = nmraspecds.io.BrukerImporter()
        importer.source = "testdata/Alanine/10"
        self.dataset.import_from(importer)
        print(self.dataset.metadata.experiment.nuclei[0].type)
        self.calibration.parameters["standard"] = "alanine"
        analysis = self.dataset.analyse(self.calibration)
        self.assertAlmostEqual(analysis.parameters["chemical_shift"], 178, -2)
        self.assertAlmostEqual(analysis.result, 51.92, -1)


class TestRMSD(unittest.TestCase):
    def setUp(self):
        self.rmsd = nmraspecds.analysis.RMSD()
        self.dataset = nmraspecds.dataset.ExperimentalDataset()
        xvalues = np.linspace(1, 200, num=200)
        yvalues = np.random.random(200)
        self.dataset.data.data = yvalues

    def test_instantiate_class(self):
        pass

    def test_has_appropriate_description(self):
        self.assertIn(
            "rmsd",
            self.rmsd.description.lower(),
        )

    def test_number_is_calculated(self):
        analysis = self.dataset.analyse(self.rmsd)
        self.assertIsInstance(analysis.result, np.float64)


class TestAreaOfSlices(unittest.TestCase):
    def setUp(self):
        self.analysis = nmraspecds.analysis.AreaOfSlices()
        self.dataset = nmraspecds.dataset.ExperimentalDataset()

    def create_test_dataset(self):
        def gaussian(amp, fwhm, mean):
            return lambda x: amp * np.exp(
                -4.0 * np.log(2) * (x - mean) ** 2 / fwhm**2
            )

        xvalues = np.flip(np.linspace(1, 50, num=200))
        noise = np.random.normal(0, 0.5, len(xvalues))
        data = (
            gaussian(50, 5, 25)(xvalues)
            + gaussian(15, 3, 15)(xvalues)
            + noise
        )
        data = np.append(
            data, gaussian(50, 5, 25)(xvalues) + gaussian(15, 3, 15)(xvalues)
        )
        data = np.append(data, gaussian(50, 5, 25)(xvalues))
        data = np.append(data, gaussian(15, 3, 15)(xvalues))
        self.dataset.data.data = data.reshape(4, 200).T
        self.dataset.data.axes[0].values = xvalues
        self.dataset.data.axes[0].quantity = "chemical shift"
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.data.axes[1].quantity = "Peak No"
        self.dataset.data.axes[1].unit = None
        self.dataset.data.axes[2].quantity = "intensity"
        self.dataset.data.axes[2].unit = "a.u."

    def test_instantiate_class(self):
        pass

    @unittest.skip
    def test_show_test_dataset(self):
        self.create_test_dataset()
        plt.plot(self.dataset.data.data)
        plt.show()

    def test_has_appropriate_description(self):
        self.assertIn("area", self.analysis.description.lower())

    def test_return_number(self):
        self.create_test_dataset()
        analysis = self.dataset.analyse(self.analysis)
        self.assertTrue(analysis.result.all())

    def test_result_is_on_second_axis(self):
        self.create_test_dataset()
        analysis = self.dataset.analyse(self.analysis)
        self.assertEqual(4, len(analysis.result))


class TestAggregatedAnalysisStep(unittest.TestCase):
    def setUp(self):
        self.analysis = nmraspecds.analysis.AggregatedAnalysisStep()
        self.analysis.analysis_step = "nmraspecds.analysis.AreaOfSlices"

    def create_test_dataset(self):
        self.dataset = nmraspecds.dataset.ExperimentalDataset()

        def gaussian(amp, fwhm, mean):
            return lambda x: amp * np.exp(
                -4.0 * np.log(2) * (x - mean) ** 2 / fwhm**2
            )

        xvalues = np.flip(np.linspace(1, 50, num=200))
        noise = np.random.normal(0, 0.5, len(xvalues))
        data = (
            gaussian(50, 5, 25)(xvalues)
            + gaussian(15, 3, 15)(xvalues)
            + noise
        )
        data = np.append(
            data, gaussian(50, 5, 25)(xvalues) + gaussian(15, 3, 15)(xvalues)
        )
        data = np.append(data, gaussian(50, 5, 25)(xvalues))
        data = np.append(data, gaussian(15, 3, 15)(xvalues))
        self.dataset.data.data = data.reshape(4, 200).T
        self.dataset.data.axes[0].values = xvalues
        self.dataset.data.axes[0].quantity = "chemical shift"
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.data.axes[1].quantity = "Peak No"
        self.dataset.data.axes[1].unit = None
        self.dataset.data.axes[2].quantity = "intensity"
        self.dataset.data.axes[2].unit = "a.u."

    def test_instantiate_class(self):
        pass

    def test_results_with_different_lengths_are_filled_with_zeroes(self):
        self.create_test_dataset()
        self.analysis.datasets.append(copy.deepcopy(self.dataset))
        xvalues = np.flip(np.linspace(1, 2, num=200))
        self.dataset.data.data = np.vstack(
            [self.dataset.data.data.T, xvalues]
        ).T
        self.analysis.datasets.append(self.dataset)
        self.analysis.analyse()
        self.assertEqual(0, self.analysis.result.data.data[0, -1])
