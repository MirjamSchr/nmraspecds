import unittest

from nmraspecds import metadata


class TestExperimentalDatasetMetadata(unittest.TestCase):

    def setUp(self):
        self.experimental_dataset_metadata = metadata.ExperimentalDatasetMetadata()

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
