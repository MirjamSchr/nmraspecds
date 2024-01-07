import unittest

import matplotlib.pyplot as plt
import numpy as np

import nmraspecds.dataset
from nmraspecds import io


class TestBrukerImporter(unittest.TestCase):
    def setUp(self):
        self.bruker_importer = io.BrukerImporter()
        self.dataset = nmraspecds.dataset.ExperimentalDataset()

    def test_instantiate_class(self):
        pass

    def test_import_data_to_dataset(self):
        self.bruker_importer.source = 'testdata/Adamantane/1'
        self.dataset.import_from(self.bruker_importer)
        self.assertTrue(self.dataset.data.data.any())

    def test_data_is_fid(self):
        self.bruker_importer.source = 'testdata/Adamantane/1'
        self.dataset.import_from(self.bruker_importer)
        #  Test if index of global max or min is within the first 15% of the
        #  data -> FID
        index_max = np.argmax(self.dataset.data.data)
        index_min = np.argmin(self.dataset.data.data)
        index = min(index_min, index_max)
        self.assertTrue(index < 0.15 * len(self.dataset.data.data))

    def test_data_is_not_processed_data(self):
        self.bruker_importer.source = 'testdata/Adamantane/1'
        self.dataset.import_from(self.bruker_importer)
        #  Test if index of global max or min is *not* between 10 and 90%
        #  of the data -> FID
        index_max = np.argmax(self.dataset.data.data)
        index_min = np.argmin(self.dataset.data.data)
        index = min(index_min, index_max)
        len_data = len(self.dataset.data.data)
        self.assertFalse(0.1 * len_data < index < 0.9 * len_data)

    @unittest.skip  # Time axis not present yet
    def test_import_time_axis(self):
        self.bruker_importer.source = 'testdata/Adamantane/1'
        self.dataset.import_from(self.bruker_importer)
        self.assertLess(self.dataset.data.axes[0].values[-1], 2)

    def test_import_processed_data_to_dataset(self):
        self.bruker_importer.source = 'testdata/Adamantane/1/pdata/1'
        self.dataset.import_from(self.bruker_importer)
        #  Test if index  global max or min is between 10 and 90%  of the
        #  data -> processed data
        index_max = np.argmax(self.dataset.data.data)
        index_min = np.argmin(self.dataset.data.data)
        index = min(index_min, index_max)
        len_data = len(self.dataset.data.data)
        self.assertTrue(0.1 * len_data < index < 0.9 * len_data)

    def test_data_is_not_fid(self):
        self.bruker_importer.source = 'testdata/Adamantane/1/pdata/1'
        self.dataset.import_from(self.bruker_importer)
        #  Test if index of global max or min is *not* within the first
        #  15% of the data -> processed data
        index_max = np.argmax(self.dataset.data.data)
        index_min = np.argmin(self.dataset.data.data)
        index = min(index_min, index_max)
        self.assertFalse(index < 0.15 * len(self.dataset.data.data))
