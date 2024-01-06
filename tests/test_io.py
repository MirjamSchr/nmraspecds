import unittest

import nmraspecds.dataset
from nmraspecds import io


class TestBrukerImporter(unittest.TestCase):
    def setUp(self):
        self.bruker_importer = io.BrukerImporter()

    def test_instantiate_class(self):
        pass

    def test_import_data_to_dataset(self):
        dataset = nmraspecds.dataset.ExperimentalDataset()
        self.bruker_importer.source = 'testdata/Adamantane/1'
        dataset.import_from(self.bruker_importer)
        self.assertTrue(dataset.data.data.any())