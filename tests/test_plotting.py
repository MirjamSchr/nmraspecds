import unittest

import aspecd.plotting
import matplotlib
import scipy.signal.windows

from nmraspecds import plotting, dataset
import numpy as np


class TestSinglePlotter1D(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.SinglePlotter1D()
        self.dataset = dataset.ExperimentalDataset()
        self.dataset.data.data = np.random.random(5)
        self.dataset.data.axes[0].quantity = "chemical shift"
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.data.axes[1].quantity = "intensity"
        self.dataset.data.axes[1].unit = "a.u."
        self.plotter.dataset = self.dataset

    def test_axis_is_inverted(self):
        self.plotter.plot()
        self.assertTrue(self.plotter.axes.xaxis_inverted())

    def test_has_g_axis_parameter(self):
        self.assertTrue("frequency-axis" in self.plotter.parameters)

    def test_g_axis_adds_secondary_axis(self):
        self.plotter.parameters["frequency-axis"] = True
        self.plotter.plot()
        secondary_axes = [
            child
            for child in self.plotter.ax.get_children()
            if isinstance(
                child, matplotlib.axes._secondary_axes.SecondaryAxis
            )
        ]
        self.assertTrue(secondary_axes)


class TestSinglePlotter2D(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.SinglePlotter2D()
        self.dataset = dataset.ExperimentalDataset()
        self.dataset.data.data = np.random.random((5, 3))
        self.dataset.data.axes[0].quantity = "chemical shift"
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.data.axes[1].quantity = "chemical shift"
        self.dataset.data.axes[1].unit = "ppm"
        self.dataset.data.axes[2].quantity = "intensity"
        self.dataset.data.axes[2].unit = "a.u."
        self.plotter.dataset = self.dataset

    def test_axis_is_inverted(self):
        self.plotter.plot()
        self.assertTrue(self.plotter.axes.xaxis_inverted())

    def test_has_g_axis_parameter(self):
        self.assertTrue("frequency-axis" in self.plotter.parameters)

    def test_g_axis_adds_secondary_axis(self):
        self.plotter.parameters["frequency-axis"] = True
        self.plotter.plot()
        secondary_axes = [
            child
            for child in self.plotter.ax.get_children()
            if isinstance(
                child, matplotlib.axes._secondary_axes.SecondaryAxis
            )
        ]
        self.assertTrue(secondary_axes)


class TestSinglePlotter2DStacked(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.SinglePlotter2DStacked()
        self.dataset = dataset.ExperimentalDataset()
        self.dataset.data.data = np.random.random((5, 3))
        self.dataset.data.axes[0].quantity = "chemical shift"
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.data.axes[1].quantity = "chemical shift"
        self.dataset.data.axes[1].unit = "ppm"
        self.dataset.data.axes[2].quantity = "intensity"
        self.dataset.data.axes[2].unit = "a.u."
        self.plotter.dataset = self.dataset

    def test_axis_is_inverted(self):
        self.plotter.plot()
        self.assertTrue(self.plotter.axes.xaxis_inverted())

    def test_has_g_axis_parameter(self):
        self.assertTrue("frequency-axis" in self.plotter.parameters)

    def test_g_axis_adds_secondary_axis(self):
        self.plotter.parameters["frequency-axis"] = True
        self.plotter.plot()
        secondary_axes = [
            child
            for child in self.plotter.ax.get_children()
            if isinstance(
                child, matplotlib.axes._secondary_axes.SecondaryAxis
            )
        ]
        self.assertTrue(secondary_axes)

    def test_g_axis_has_correct_label(self):
        self.plotter.parameters["frequency-axis"] = True
        self.plotter.plot()
        secondary_axes = [
            child
            for child in self.plotter.ax.get_children()
            if isinstance(
                child, matplotlib.axes._secondary_axes.SecondaryAxis
            )
        ]
        self.assertIn(
            r"\Delta \nu",
            secondary_axes[0].get_xaxis().get_label().get_text(),
        )


class TestMultiPlotter1D(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.MultiPlotter1D()
        self.dataset = dataset.ExperimentalDataset()
        self.dataset.data.data = np.random.random(5)
        self.dataset.data.axes[0].quantity = "chemical shift"
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.data.axes[1].quantity = "intensity"
        self.dataset.data.axes[1].unit = "a.u."
        self.plotter.datasets = [self.dataset, self.dataset]

    def test_axis_is_inverted(self):
        self.plotter.plot()
        self.assertTrue(self.plotter.axes.xaxis_inverted())

    def test_has_g_axis_parameter(self):
        self.assertTrue("frequency-axis" in self.plotter.parameters)

    def test_g_axis_adds_secondary_axis(self):
        self.plotter.parameters["frequency-axis"] = True
        self.plotter.plot()
        secondary_axes = [
            child
            for child in self.plotter.ax.get_children()
            if isinstance(
                child, matplotlib.axes._secondary_axes.SecondaryAxis
            )
        ]
        self.assertTrue(secondary_axes)

    def test_g_axis_has_correct_label(self):
        self.plotter.parameters["frequency-axis"] = True
        self.plotter.plot()
        secondary_axes = [
            child
            for child in self.plotter.ax.get_children()
            if isinstance(
                child, matplotlib.axes._secondary_axes.SecondaryAxis
            )
        ]
        self.assertIn(
            r"\Delta \nu",
            secondary_axes[0].get_xaxis().get_label().get_text(),
        )


class TestMultiPlotter1DStacked(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.MultiPlotter1DStacked()
        self.dataset = dataset.ExperimentalDataset()
        self.dataset.data.data = np.random.random(5)
        self.dataset.data.axes[0].quantity = "chemical shift"
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.data.axes[1].quantity = "intensity"
        self.dataset.data.axes[1].unit = "a.u."
        self.plotter.datasets = [self.dataset, self.dataset]

    def test_axis_is_inverted(self):
        self.plotter.plot()
        self.assertTrue(self.plotter.axes.xaxis_inverted())

    def test_has_g_axis_parameter(self):
        self.assertTrue("frequency-axis" in self.plotter.parameters)

    def test_g_axis_adds_secondary_axis(self):
        self.plotter.parameters["frequency-axis"] = True
        self.plotter.plot()
        secondary_axes = [
            child
            for child in self.plotter.ax.get_children()
            if isinstance(
                child, matplotlib.axes._secondary_axes.SecondaryAxis
            )
        ]
        self.assertTrue(secondary_axes)

    def test_g_axis_has_correct_label(self):
        self.plotter.parameters["frequency-axis"] = True
        self.plotter.plot()
        secondary_axes = [
            child
            for child in self.plotter.ax.get_children()
            if isinstance(
                child, matplotlib.axes._secondary_axes.SecondaryAxis
            )
        ]
        self.assertIn(
            r"\Delta \nu",
            secondary_axes[0].get_xaxis().get_label().get_text(),
        )


class TestFittingPlotter2D(unittest.TestCase):
    def setUp(self):
        self.plotter = plotting.FittingPlotter2D()
        self.dataset = dataset.ExperimentalDataset()
        data = np.array([])
        for nr in range(1, 6):
            data = np.append(data, scipy.signal.windows.gaussian(31, std=nr))
        self.dataset.data.data = data.reshape(5, 31).T
        self.dataset.data.axes[0].quantity = "chemical shift"
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.data.axes[1].quantity = "Peak No"
        self.dataset.data.axes[1].unit = None
        self.dataset.data.axes[2].quantity = "intensity"
        self.dataset.data.axes[2].unit = "a.u."
        self.plotter.dataset = self.dataset

    def test_instantiate_class(self):
        self.plotter.plot()
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        self.plotter.save(saver)
