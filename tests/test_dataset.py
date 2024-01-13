import unittest

from nmraspecds import dataset


class TestExperimentalDataset(unittest.TestCase):
    def setUp(self):
        self.experimental_dataset = dataset.ExperimentalDataset()

    def test_instantiate_class(self):
        pass


class TestCalculatedDataset(unittest.TestCase):
    def setUp(self):
        self.calculated_dataset = dataset.CalculatedDataset()

    def test_instantiate_class(self):
        pass


class TestDatasetFactory(unittest.TestCase):
    def setUp(self):
        self.dataset_factory = dataset.DatasetFactory()

    def test_instantiate_class(self):
        pass
