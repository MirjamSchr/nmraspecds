import unittest

import nmraspecds.dataset
from nmraspecds import processing


class TestExternalReferencing(unittest.TestCase):
    def setUp(self):
        self.referencing = processing.ExternalReferencing()
        self.dataset = nmraspecds.dataset.ExperimentalDataset()

    def test_instantiate_class(self):
        pass


