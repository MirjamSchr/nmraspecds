import copy
import unittest

import aspecd.plotting
import matplotlib
import matplotlib.pyplot
from docutils.nodes import figure

import nmraspecds.io
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
        data = np.append(data, gaussian(50, 5, 25)(xvalues))
        data = np.append(data, gaussian(50, 5, 25)(xvalues))
        self.dataset.data.data = data.reshape(3, 200).T
        self.dataset.data.axes[0].values = xvalues
        self.dataset.data.axes[0].quantity = "chemical shift"
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.data.axes[1].quantity = "Peak No"
        self.dataset.data.axes[1].unit = None
        self.dataset.data.axes[2].quantity = "intensity"
        self.dataset.data.axes[2].unit = "a.u."

    def create_test_dataset_without_noise(self):
        def gaussian(amp, fwhm, mean):
            return lambda x: amp * np.exp(
                -4.0 * np.log(2) * (x - mean) ** 2 / fwhm**2
            )

        xvalues = np.flip(np.linspace(1, 50, num=200))
        data = gaussian(50, 5, 25)(xvalues) + gaussian(15, 3, 15)(xvalues)
        data = np.append(data, gaussian(50, 5, 25)(xvalues))
        data = np.append(data, gaussian(50, 5, 25)(xvalues))
        self.dataset.data.data = data.reshape(3, 200).T
        self.dataset.data.axes[0].values = xvalues
        self.dataset.data.axes[0].quantity = "chemical shift"
        self.dataset.data.axes[0].unit = "ppm"
        self.dataset.data.axes[1].quantity = "Peak No"
        self.dataset.data.axes[1].unit = None
        self.dataset.data.axes[2].quantity = "intensity"
        self.dataset.data.axes[2].unit = "a.u."

    def test_instantiate_class(self):
        self.create_test_dataset()
        self.plotter.dataset = self.dataset
        self.plotter.plot()
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        # self.plotter.save(saver)

    def test_get_rmsd_in_range(self):
        source = "testdata/fitting-data.asc"
        importer = nmraspecds.io.FittingImporter(source=source)
        self.dataset.import_from(importer)
        self.plotter.dataset = self.dataset
        self.plotter.plot()
        # self.plotter.rms
        # self.plotter.save(saver)

    def test_residues_have_senseful_offset(self):
        source = "testdata/fitting-data.asc"
        importer = nmraspecds.io.FittingImporter(source=source)
        self.dataset.import_from(importer)
        self.plotter.dataset = self.dataset
        self.plotter.plot()
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        # self.plotter.save(saver)

    def test_residues_offset_range_settable(self):
        source = "testdata/fitting-data.asc"
        importer = nmraspecds.io.FittingImporter(source=source)
        self.dataset.import_from(importer)
        self.plotter.parameters["range_residues"] = [-200, -300]
        self.plotter.dataset = self.dataset
        self.plotter.plot()
        # self.assertTrue(min(self.plotter.residues > 5))
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        # self.plotter.save(saver)

    def test_residues_offset_range_gives_full_range(self):
        source = "testdata/fitting-data.asc"
        importer = nmraspecds.io.FittingImporter(source=source)
        self.dataset.import_from(importer)
        self.plotter.parameters["range_residues"] = [0, 0]
        self.plotter.dataset = self.dataset
        self.plotter.plot()
        # self.assertTrue(min(self.plotter.residues > 5))
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        # self.plotter.save(saver)

    def test_no_residue_parameter_given_runs(self):
        self.create_test_dataset()
        self.plotter.dataset = self.dataset
        offset = self.dataset.data.data[:, 0].max() * 0.07
        self.plotter.plot()
        self.assertAlmostEqual(self.plotter._offset, offset, delta=0.2)
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        # self.plotter.save(saver)

    def test_maxima_with_annotation_object(self):
        source = "testdata/fitting-data.asc"
        importer = nmraspecds.io.FittingImporter(source=source)
        self.dataset.import_from(importer)
        self.plotter.dataset = self.dataset
        self.plotter.plot()
        # self.assertTrue(min(self.plotter.residues > 5))
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        # self.plotter.save(saver)

    def test_set_offset(self):
        self.create_test_dataset()
        self.plotter.dataset = self.dataset
        self.plotter.parameters["offset_residues"] = 25
        self.plotter.plot()
        self.assertAlmostEqual(
            self.plotter.parameters["offset_residues"], self.plotter._offset
        )
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        # self.plotter.save(saver)

    def test_raw_offset_with_percent(self):
        self.create_test_dataset()
        amp = self.dataset.data.data[:, 0].max()
        self.plotter.dataset = self.dataset
        self.plotter.parameters["offset_residues"] = "10%"
        self.plotter.plot()
        self.assertAlmostEqual(self.plotter._offset, amp * 0.1, delta=1)

    def test_range_and_percentage_settable(self):
        self.create_test_dataset_without_noise()
        self.plotter.dataset = self.dataset
        self.plotter.parameters["offset_residues"] = "50%"
        self.plotter.parameters["range_residues"] = [20, 3]
        self.plotter.plot()
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        # self.plotter.save(saver)
        self.assertAlmostEqual(self.plotter._offset, 15 * 0.5, delta=1)

    def test_axis_has_decreasing_values(self):
        self.create_test_dataset()
        xvalues = np.linspace(1, 50, num=200)
        self.dataset.data.axes[0].values = xvalues
        self.plotter.dataset = self.dataset
        data = copy.deepcopy(self.dataset.data.data)
        self.plotter.plot()
        np.testing.assert_array_equal(self.dataset.data.data, data[::-1, :])

    def test_fontsize_changed(self):
        matplotlib.rcParams["font.size"] = 11
        self.create_test_dataset()
        self.plotter.dataset = self.dataset
        self.plotter.plot()
        self.assertEqual(self.plotter._font_size, 11)
        matplotlib.rcParams["font.size"] = 10

    def test_ylim_fits_potition_of_annotation(self):
        self.create_test_dataset_without_noise()
        self.plotter.dataset = self.dataset
        self.plotter.plot()
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        # self.plotter.save(saver)
        ylim = self.plotter.axes.get_ylim()
        self.assertNotAlmostEqual(ylim[0], -6.165, places=2)
        self.assertAlmostEqual(52.597, ylim[1], 2)

    def test_ylim_fits_position_of_annotation2(self):
        self.create_test_dataset_without_noise()

        # for figsize
        # with self.subTest(key=key):
        # self.plotter.properties.figure.size((6,4))
        figure_sizes = ((6, 4), (4, 6), (1, 1))
        for figure_size in figure_sizes:
            with self.subTest(figure_size=figure_size):
                plotter = plotting.FittingPlotter2D()
                plotter.dataset = self.dataset
                plotter.properties.figure.size = figure_size
                plotter.plot()
                # print(plotter.fig.get_figheight())
                saver = aspecd.plotting.Saver()
                saver.filename = "test.pdf"
                # self.plotter.save(saver)
                ylim = plotter.axes.get_ylim()
                self.assertNotAlmostEqual(ylim[0], -6.165, places=2)
                self.assertAlmostEqual(52.597, ylim[1], 2)

                matplotlib.pyplot.close("all")

    def test_offset_depends_on_fontsize(self):
        self.create_test_dataset_without_noise()
        self.plotter.dataset = self.dataset
        self.plotter.plot()
        # print(self.plotter._offset)
        self.assertNotEqual(self.plotter._offset, 5)
        self.assertAlmostEqual(self.plotter._font_offset, 3.1452, 2)
        saver = aspecd.plotting.Saver()
        saver.filename = "test.pdf"
        # self.plotter.save(saver)
