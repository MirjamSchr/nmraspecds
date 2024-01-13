import copy
import unittest

import matplotlib.pyplot as plt
import numpy as np
import scipy
from numpy import testing

import nmraspecds.dataset
import nmraspecds.metadata
from nmraspecds import processing


class TestExternalReferencing(unittest.TestCase):
    def setUp(self):
        self.referencing = processing.ExternalReferencing()
        self.dataset = nmraspecds.dataset.ExperimentalDataset()
        self.data = scipy.signal.windows.gaussian(65, std=2)
        self.axis = np.linspace(0, 30, num=65)

    def test_instantiate_class(self):
        pass

    def test_axis_gets_changed(self):
        self.dataset.data.data = self.data
        self.dataset.data.axes[0].values = self.axis
        self.dataset.data.axes[0].unit = "ppm"
        self.referencing.parameters["offset"] = 520
        nucleus = nmraspecds.metadata.Nucleus()
        nucleus.base_frequency.from_string("400 MHz")
        self.dataset.metadata.experiment.add_nucleus(nucleus)
        self.dataset.metadata.experiment.spectrometer_frequency.from_string(
            "400.0000 MHz"
        )
        axis_before = copy.deepcopy(self.dataset.data.axes[0].values)
        self.dataset.process(self.referencing)
        axis_after = self.dataset.data.axes[0].values
        testing.assert_allclose(
            axis_before + 520 / 400, axis_after, rtol=1e-4
        )

    def test_new_frequency_is_written(self):
        self.dataset.data.data = self.data
        self.dataset.data.axes[0].values = self.axis
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.metadata.experiment.spectrometer_frequency.from_string(
            "400.00000 MHz"
        )
        nucleus = nmraspecds.metadata.Nucleus()
        nucleus.base_frequency.from_string("400 MHz")
        self.dataset.metadata.experiment.add_nucleus(nucleus)
        self.referencing.parameters["offset"] = 500
        spectrometer_frequency_before = copy.deepcopy(
            self.dataset.metadata.experiment.spectrometer_frequency.value
        )
        self.dataset.process(self.referencing)
        spectrometer_frequency_after = (
            self.dataset.metadata.experiment.spectrometer_frequency.value
        )
        self.assertNotEqual(
            spectrometer_frequency_before, spectrometer_frequency_after
        )
        self.assertGreater(
            spectrometer_frequency_after, spectrometer_frequency_before
        )

    def test_without_offset_raises(self):
        self.dataset.data.data = self.data
        self.dataset.data.axes[0].values = self.axis
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.metadata.experiment.spectrometer_frequency.from_string(
            "400 MHz"
        )
        with self.assertRaises(ValueError):
            self.dataset.process(self.referencing)
