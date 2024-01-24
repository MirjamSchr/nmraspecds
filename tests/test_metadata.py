import unittest

import aspecd.metadata

from nmraspecds import metadata


class TestExperimentalDatasetMetadata(unittest.TestCase):
    def setUp(self):
        self.experimental_dataset_metadata = (
            metadata.ExperimentalDatasetMetadata()
        )

    def test_instantiate_class(self):
        pass


class TestSample(unittest.TestCase):
    def setUp(self):
        self.sample = metadata.Sample()

    def test_instantiate_class(self):
        pass


class TestSpectrometer(unittest.TestCase):
    def setUp(self):
        self.spectrometer = metadata.Spectrometer()

    def test_instantiate_class(self):
        pass


class TestProbehead(unittest.TestCase):
    def setUp(self):
        self.probehead = metadata.Probehead()

    def test_instantiate_class(self):
        pass


class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.experiment = metadata.Experiment()

    def test_instantiate_class(self):
        pass

    def test_get_spectrum_reference(self):
        nucleus = metadata.Nucleus()
        nucleus.base_frequency.from_string("400.5 MHz")
        nucleus.offset_hz.from_string("2000 Hz")
        self.experiment.add_nucleus(nucleus)
        self.experiment.spectrometer_frequency.from_string("400.0 MHz")
        spectrum_reference = (
            self.experiment.spectrometer_frequency.value * 1e6
            - self.experiment.nuclei[0].base_frequency.value * 1e6
        )
        self.assertAlmostEqual(
            self.experiment.spectrum_reference.value, spectrum_reference
        )

    def test_spectrum_reference_without_nucleus(self):
        # TODO: What is it expected to do? Is it automatically recalculated
        #  when a nucleus is present?
        pass


class TestNucleus(unittest.TestCase):
    def setUp(self):
        self.nucleus = metadata.Nucleus()

    def test_instantiate_class(self):
        pass

    def test_get_transmitter_frequency(self):
        self.nucleus.base_frequency.from_string("400 MHz")
        self.nucleus.offset_hz.from_string("500 Hz")
        transmitter_freq = (400e6 + 500) / 1e6
        self.assertEqual(
            transmitter_freq, self.nucleus.transmitter_frequency.value
        )

    def test_get_offset_ppm(self):
        self.nucleus.base_frequency.from_string("400.5 MHz")
        self.nucleus.offset_hz.from_string("2000 Hz")
        offset_ppm = (2000 * 1e6) / 400.5e6
        self.assertEqual(offset_ppm, self.nucleus.offset_ppm.value)


class TestRotor(unittest.TestCase):
    def setUp(self):
        self.rotor = metadata.Rotor()

    def test_instantiate_class(self):
        pass
