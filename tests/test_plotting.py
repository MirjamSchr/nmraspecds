import unittest

from nmraspecds import plotting, dataset
import numpy as np


class TestSinglePlotter1D(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.SinglePlotter1D()
        self.dataset = dataset.ExperimentalDataset()
        self.dataset.data.data = np.random.random(5)
        self.plotter.dataset = self.dataset

    def test_axis_is_inverted(self):
        self.plotter.plot()
        self.assertTrue(self.plotter.axes.xaxis_inverted())


class TestSinglePlotter2D(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.SinglePlotter2D()
        self.dataset = dataset.ExperimentalDataset()
        self.dataset.data.data = np.random.random((5, 3))
        self.plotter.dataset = self.dataset

    def test_axis_is_inverted(self):
        self.plotter.plot()
        self.assertTrue(self.plotter.axes.xaxis_inverted())


class TestSinglePlotter2DStacked(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.SinglePlotter2DStacked()
        self.dataset = dataset.ExperimentalDataset()
        self.dataset.data.data = np.random.random((5, 3))
        self.plotter.dataset = self.dataset

    def test_axis_is_inverted(self):
        self.plotter.plot()
        self.assertTrue(self.plotter.axes.xaxis_inverted())


class TestMultiPlotter1D(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.MultiPlotter1D()
        self.dataset = dataset.ExperimentalDataset()
        self.dataset.data.data = np.random.random(5)
        self.plotter.datasets = [self.dataset, self.dataset]

    def test_axis_is_inverted(self):
        self.plotter.plot()
        self.assertTrue(self.plotter.axes.xaxis_inverted())


class TestMultiPlotter1DStacked(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.MultiPlotter1DStacked()
        self.dataset = dataset.ExperimentalDataset()
        self.dataset.data.data = np.random.random(5)
        self.plotter.datasets = [self.dataset, self.dataset]

    def test_axis_is_inverted(self):
        self.plotter.plot()
        self.assertTrue(self.plotter.axes.xaxis_inverted())
