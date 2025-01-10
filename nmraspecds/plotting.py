"""
plotting module of the nmraspecds package.
"""
import re
import aspecd.plotting
import aspecd.annotation
import numpy as np
import matplotlib as mpl

from nmraspecds import utils


class PlotterExtensions:
    """Extensions for plots of NMR data.

    This class is meant as a mixin class for plotters of the nmraspecds package
    and provides functionality specific for NMR-spectroscopic data.

    Hence it can only be used as mixin in addition to a plotter class.

    Attributes
    ----------
    parameters : :class:`dict`
        All parameters necessary for the plot, implicit and explicit

        The following keys exist, in addition to those defined by the actual
        plotter:

        frequency-axis: :class:`bool`
            Whether to show an additional frquency axis opposite of the
            chemical shift axis

            This assumes the chemical shift axis to be the *x* axis and then
            calculates the offset frequency from the frequency of the nucleus.


            .. important::

                If you add a frequency axis to your plot, and at the same time
                specify a figure title, this will result in the figure
                title clashing with the frequency axis. The solution: set an
                *axes* title rather than a *figure* title.

    """

    def __init__(self):
        self.parameters["frequency-axis"] = False

    def _create_frequency_axis(self, reference_frequency=None):
        def forward(values):
            return utils.convert_ppm_to_delta_kHz(
                values, reference_frequency=reference_frequency
            )

        def backward(values):
            return utils.convert_delta_kHz_to_ppm(
                values, reference_frequency=reference_frequency
            )

        freq_axis = self.ax.secondary_xaxis(
            "top", functions=(forward, backward)
        )
        freq_axis.set_xlabel(r"$\Delta \nu\ $ / kHz")


class SinglePlotter1D(aspecd.plotting.SinglePlotter1D, PlotterExtensions):
    """1D plots of single datasets.

    Convenience class taking care of 1D plots of single datasets.

    As the class is fully inherited from ASpecD for simple usage, see the
    ASpecD documentation of the :class:`aspecd.plotting.SinglePlotter1D`
    class for details.

    Furthermore, the class inherits all functionality from
    :class:`PlotterExtensions`. See there for additional details.


    Examples
    --------
    For convenience, a series of examples in recipe style (for details of
    the recipe-driven data analysis, see :mod:`aspecd.tasks`) is given below
    for how to make use of this class. Of course, all parameters settable
    for the superclasses can be set as well. The examples focus each on a
    single aspect.

    In the simplest case, just invoke the plotter with default values:

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter1D
         properties:
           filename: output.pdf


    In case you would like to have a frequency axis plotted as a second *x*
    axis on top:

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter1D
         properties:
           parameters:
             frequency-axis: true
           filename: output.pdf


    .. important::

        If you add a frequency axis to your plot, and at the same time specify a
        figure title, this will result in the figure title clashing with
        the frequency axis. The solution: set an *axes* title rather than a
        *figure* title.

    """

    def __init__(self):
        super().__init__()
        self.properties.axes.invert = "x"

    def _create_plot(self):
        super()._create_plot()
        if (
            self.parameters["frequency-axis"]
            and self.data.axes[0].unit == "ppm"
        ):
            self._create_frequency_axis(
                self.dataset.metadata.experiment.spectrometer_frequency.value
            )


class SinglePlotter2D(aspecd.plotting.SinglePlotter2D, PlotterExtensions):
    """2D plots of single datasets.

    Convenience class taking care of 2D plots of single datasets.

    As the class is fully inherited from ASpecD for simple usage, see the
    ASpecD documentation of the :class:`aspecd.plotting.SinglePlotter2D`
    class for details.

    Furthermore, the class inherits all functionality from
    :class:`PlotterExtensions`. See there for additional details.


    Examples
    --------
    For convenience, a series of examples in recipe style (for details of
    the recipe-driven data analysis, see :mod:`aspecd.tasks`) is given below
    for how to make use of this class. Of course, all parameters settable
    for the superclasses can be set as well. The examples focus each on a
    single aspect.

    In the simplest case, just invoke the plotter with default values:

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter2D
         properties:
           filename: output.pdf

    To change the axes (flip *x* and *y* axis):

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter2D
         properties:
           filename: output.pdf
           parameters:
             switch_axes: True

    To use another type (here: contour):

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter2D
         properties:
           filename: output.pdf
           type: contour

    To set the number of levels of a contour plot to 10:

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter2D
         properties:
           filename: output.pdf
           type: contour
           parameters:
             levels: 10

    To change the colormap (cmap) used:

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter2D
         properties:
           filename: output.pdf
           properties:
             drawing:
               cmap: RdGy

    Make sure to check the documentation of the ASpecD
    :mod:`aspecd.plotting` module for further parameters that can be set.

    In case you would like to have a frequency axis plotted as a second *x* axis on
    top:

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter2D
         properties:
           parameters:
             frequency-axis: true
           filename: output.pdf


    .. important::

        If you add a frequency axis to your plot, and at the same time specify a
        figure title, this will result in the figure title clashing with
        the frequency axis. The solution: set an *axes* title rather than a
        *figure* title.

    """

    def __init__(self):
        super().__init__()
        self.properties.axes.invert = ["x", "y"]
        self.parameters["switch_axes"] = True

    def _create_plot(self):
        super()._create_plot()
        if (
            self.parameters["frequency-axis"]
            and self.data.axes[0].unit == "ppm"
        ):
            self._create_frequency_axis(
                self.dataset.metadata.experiment.spectrometer_frequency.value
            )


class SinglePlotter2DStacked(
    aspecd.plotting.SinglePlotter2DStacked, PlotterExtensions
):
    """Stacked plots of 2D data.

    A stackplot creates a series of lines stacked on top of each other from
    a 2D dataset.

    As the class is fully inherited from ASpecD for simple usage, see the
    ASpecD documentation of the :class:`aspecd.plotting.SinglePlotter2DStacked`
    class for details.

    Furthermore, the class inherits all functionality from
    :class:`PlotterExtensions`. See there for additional details.


    Examples
    --------
    For convenience, a series of examples in recipe style (for details of
    the recipe-driven data analysis, see :mod:`aspecd.tasks`) is given below
    for how to make use of this class. Of course, all parameters settable
    for the superclasses can be set as well. The examples focus each on a
    single aspect.

    In the simplest case, just invoke the plotter with default values:

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter2DStacked
         properties:
           filename: output.pdf

    If you need to more precisely control the formatting of the y tick
    labels, particularly the number of decimals shown, you can set the
    formatting accordingly:

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter2DStacked
         properties:
           filename: output.pdf
           parameters:
             yticklabelformat: '%.2f'

    In this particular case, the y tick labels will appear with only two
    decimals. Note that currently, the "old style" formatting specifications
    are used due to their widespread use in other programming languages and
    hence the familiarity of many users with this particular notation.

    Sometimes you want to have horizontal "zero lines" appear for each
    individual trace of the stacked plot. This can be achieved explicitly
    setting the "show_zero_lines" parameter to "True" that is set to "False"
    by default:

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter2DStacked
         properties:
           filename: output.pdf
           parameters:
             show_zero_lines: True

    In case you would like to have a frequency axis plotted as a second *x* axis on
    top:

    .. code-block:: yaml

       - kind: singleplot
         type: SinglePlotter2DStacked
         properties:
           parameters:
             frequency-axis: true
           filename: output.pdf


    .. important::

        If you add a frequency axis to your plot, and at the same time specify a
        figure title, this will result in the figure title clashing with
        the frequency axis. The solution: set an *axes* title rather than a
        *figure* title.

    """

    def __init__(self):
        super().__init__()
        self.properties.axes.invert = "x"

    def _create_plot(self):
        super()._create_plot()
        if (
            self.parameters["frequency-axis"]
            and self.data.axes[0].unit == "ppm"
        ):
            self._create_frequency_axis(
                self.dataset.metadata.experiment.spectrometer_frequency.value
            )


class MultiPlotter1D(aspecd.plotting.MultiPlotter1D, PlotterExtensions):
    """1D plots of multiple datasets.

    Convenience class taking care of 1D plots of multiple datasets.

    As the class is fully inherited from ASpecD for simple usage, see the
    ASpecD documentation of the :class:`aspecd.plotting.MultiPlotter1D`
    class for details.

    Furthermore, the class inherits all functionality from
    :class:`PlotterExtensions`. See there for additional details.


    Examples
    --------
    For convenience, a series of examples in recipe style (for details of
    the recipe-driven data analysis, see :mod:`aspecd.tasks`) is given below
    for how to make use of this class. Of course, all parameters settable
    for the superclasses can be set as well. The examples focus each on a
    single aspect.

    In the simplest case, just invoke the plotter with default values:

    .. code-block:: yaml

       - kind: multiplot
         type: MultiPlotter1D
         properties:
           filename: output.pdf

    To change the settings of each individual line (here the colour and label),
    supposing you have three lines, you need to specify the properties in a
    list for each of the drawings:

    .. code-block:: yaml

       - kind: multiplot
         type: MultiPlotter1D
         properties:
           filename: output.pdf
           properties:
             drawings:
               - color: '#FF0000'
                 label: foo
               - color: '#00FF00'
                 label: bar
               - color: '#0000FF'
                 label: foobar

    .. important::
        If you set colours using the hexadecimal RGB triple prefixed by
        ``#``, you need to explicitly tell YAML that these are strings,
        surrounding the values by quotation marks.

    In case you would like to have a frequency axis plotted as a second *x* axis on
    top:

    .. code-block:: yaml

       - kind: multiplot
         type: MultiPlotter1D
         properties:
           parameters:
             frequency-axis: true
           filename: output.pdf


    .. important::

        If you add a frequency axis to your plot, and at the same time specify a
        figure title, this will result in the figure title clashing with
        the frequency axis. The solution: set an *axes* title rather than a
        *figure* title.

    """

    def __init__(self):
        super().__init__()
        self.properties.axes.invert = "x"

    def _create_plot(self):
        super()._create_plot()
        if (
            self.parameters["frequency-axis"]
            and self.data[0].axes[0].unit == "ppm"
        ):
            self._create_frequency_axis(
                self.datasets[
                    0
                ].metadata.experiment.spectrometer_frequency.value
            )


class MultiPlotter1DStacked(
    aspecd.plotting.MultiPlotter1DStacked, PlotterExtensions
):
    """Stacked 1D plots of multiple datasets.

    Convenience class taking care of 1D plots of multiple datasets.

    As the class is fully inherited from ASpecD for simple usage, see the
    ASpecD documentation of the :class:`aspecd.plotting.MultiPlotter1DStacked`
    class for details.

    Furthermore, the class inherits all functionality from
    :class:`PlotterExtensions`. See there for additional details.

    Examples
    --------
    For convenience, a series of examples in recipe style (for details of
    the recipe-driven data analysis, see :mod:`aspecd.tasks`) is given below
    for how to make use of this class. Of course, all parameters settable
    for the superclasses can be set as well. The examples focus each on a
    single aspect.

    In the simplest case, just invoke the plotter with default values:

    .. code-block:: yaml

       - kind: multiplot
         type: MultiPlotter1DStacked
         properties:
           filename: output.pdf

    To change the settings of each individual line (here the colour and label),
    supposing you have three lines, you need to specify the properties in a
    list for each of the drawings:

    .. code-block:: yaml

       - kind: multiplot
         type: MultiPlotter1DStacked
         properties:
           filename: output.pdf
           properties:
             drawings:
               - color: '#FF0000'
                 label: foo
               - color: '#00FF00'
                 label: bar
               - color: '#0000FF'
                 label: foobar

    .. important::
        If you set colours using the hexadecimal RGB triple prefixed by
        ``#``, you need to explicitly tell YAML that these are strings,
        surrounding the values by quotation marks.

    Sometimes you want to have horizontal "zero lines" appear for each
    individual trace of the stacked plot. This can be achieved explicitly
    setting the "show_zero_lines" parameter to "True" that is set to "False"
    by default:

    .. code-block:: yaml

       - kind: multiplot
         type: MultiPlotter1DStacked
         properties:
           filename: output.pdf
           parameters:
             show_zero_lines: True

    In case you would like to have a frequency axis plotted as a second *x* axis on
    top:

    .. code-block:: yaml

       - kind: multiplot
         type: MultiPlotter1DStacked
         properties:
           parameters:
             frequency-axis: true
           filename: output.pdf


    .. important::

        If you add a frequency axis to your plot, and at the same time specify a
        figure title, this will result in the figure title clashing with
        the frequency axis. The solution: set an *axes* title rather than a
        *figure* title.

    """

    def __init__(self):
        super().__init__()
        self.properties.axes.invert = "x"

    def _create_plot(self):
        super()._create_plot()
        if (
            self.parameters["frequency-axis"]
            and self.data[0].axes[0].unit == "ppm"
        ):
            self._create_frequency_axis(
                self.datasets[
                    0
                ].metadata.experiment.spectrometer_frequency.value
            )


class FittingPlotter2D(SinglePlotter2DStacked):
    """
    Plotter for fitted data with a special color scheme.

    Creates a special type of plot with the experimental data (black), the sum
    of the single, fitted peaks (red) and all single peaks (grey).
    Experimental data were previously fitted with DMFit, exported (
    experimental dataset with sum and all peaks) are imported with
    `nmraspecds.io.FittingImporter`. See the importer for details to the
    dataset.

    Providing a colormap changes the default colors of the plot.

    The offset of the residues can be defined as absolute value or as
    percentage of the amplitude of the data. If one or both values were not
    given, it is tried to set the values as good as possible.


    Attributes
    ----------
    parameters['range_residues'] : :class: `list`
        The range in which the residuals are accounted for in terms of their
        offset and RMSD calculation.

    parameters['offset_residues'] : :class: `str` or `float`
        Gives the offset of the residues either as number or in terms of
        percentage of the residuals' amplitude. The positive number results
        in a negative offset.

    Raises
    ------
    exception
        Short description when and why raised


    Examples
    --------
    The easiest way to use this Plotter

    .. code-block:: yaml

       - kind: singleplot
         type: FittingPlotter2D
         properties:
           filename: output.pdf
    """

    def __init__(self):
        super().__init__()
        self.description = "2D Stacked Plot for fitted datasets"
        self.parameters["offset"] = 0
        self.parameters["offset_residues"] = None
        self.parameters["range_residues"] = None
        self.residues = None
        self.factor = 0.07
        self.indicator_maxima = False
        self._annotation = None
        self._offset = None
        self._exclude_from_to_dict.append("residues")

    def _create_plot(self):
        self._sanitize_data()
        super()._create_plot()
        self._change_line_properties()

        self._insert_residues()
        self._set_maxima()
        # self.print_rmsd_in_spectrum(residues)

    def _sanitize_data(self):
        if (
            self.dataset.data.axes[0].values[-1]
            > self.dataset.data.axes[0].values[0]
        ):
            self.dataset.data.axes[0].values = self.dataset.data.axes[
                0
            ].values[::-1]
            print()
            self.dataset.data.data = self.dataset.data.data[::-1, :]

    def print_rmsd_in_spectrum(self, residues, x_1, x_2):
        x_1 = np.where(self.dataset.data.axes[0].values > 100)[0][-1]
        x_2 = np.where(self.dataset.data.axes[0].values < 20)[0][0]
        rmsd = np.sqrt(1 / (x_2 - x_1) * np.mean(self.residues[x_1:x_2] ** 2))
        self.axes.text(90, 20, f"RMSD = {rmsd:.3f}")

    def _change_line_properties(self):
        length = self.dataset.data.data.shape[1] - 2
        color_ = ["k", "tab:red", *["tab:gray"] * length]
        linestyle_ = ["-", "--", *["-"] * length]
        alpha_ = [1, 1, *[0.6] * length]
        for nr, line in enumerate(self.properties.drawings):
            setattr(self.properties.drawings[nr], "color", color_[nr])
            setattr(self.properties.drawings[nr], "linestyle", linestyle_[nr])
            setattr(self.properties.drawings[nr], "alpha", alpha_[nr])

    # TODO: Account for stacking _dimension

    def get_maxima(self):
        max_ppm = []
        for row in range(2, self.dataset.data.data.shape[1]):
            arg = np.argmax(self.dataset.data.data[:, row])
            max_ppm.append(self.dataset.data.axes[0].values[arg])
        return max_ppm

    def _create_colormap(self):
        cmaplist = [
            "k",
            "tab:red",
            *["tab:gray"] * (self.dataset.data.data.shape[1] - 2),
        ]
        cmap = mpl.colors.LinearSegmentedColormap.from_list(
            "Custom cmap", cmaplist, len(cmaplist)
        )
        return cmap

    def _insert_residues(self):
        self.residues = (
            self.dataset.data.data[:, 0] - self.dataset.data.data[:, 1]
        )
        data = self.dataset.data.data[:, 0]
        if not self.parameters["range_residues"]:
            self._get_dataset_ranges_in_figure()
        elif self.parameters["range_residues"] == [0, 0]:
            self.parameters["range_residues"] = None
        if self.parameters["range_residues"]:
            upper, lower = self.parameters["range_residues"]
            x_1 = np.where(self.dataset.data.axes[0].values >= upper)[0][-1]
            x_2 = np.where(self.dataset.data.axes[0].values <= lower)[0][0]
            self._offset = abs(max(data[x_1:x_2])) + abs(min(data[x_1:x_2]))
        if self.parameters["offset_residues"]:
            self._residues_offset = self.parameters["offset_residues"]
            if (
                isinstance(self._residues_offset, str)
                and "%" in self._residues_offset
            ):
                percent = (
                    float(
                        re.sub(
                            r"[^0-9.]", "", self.parameters["offset_residues"]
                        )
                    )
                    / 100
                )
                if self._offset:
                    self._offset *= percent
                else:
                    self._offset = (
                        abs(max(self.dataset.data.data[:, 0]))
                        + abs(min(self.dataset.data.data[:, 0]))
                    ) * percent
            else:
                self._offset = self.parameters["offset_residues"]
        elif self.parameters["range_residues"]:
            self._offset *= self.factor
        else:  # (not self.parameters["range_residues"] and not self.parameters["offset_residues"]):
            self._offset = abs(max(data)) + abs(min(data)) * self.factor
        self.parameters["offset_residues"] = self._offset
        self.axes.plot(
            self.dataset.data.axes[0].values,
            self.residues - self._offset,
            color="steelblue",
            alpha=0.6,
        )

    def _get_dataset_ranges_in_figure(self):
        range_figure = sorted(self.axes.get_xlim())[::-1]
        range_data = (
            self.dataset.data.axes[0].values[0],
            self.dataset.data.axes[0].values[-1],
        )
        if range_figure[0] > range_data[0]:
            upper = range_data[0]
        else:
            upper = range_figure[0]
        if range_figure[-1] < range_data[-1]:
            lower = range_data[-1]
        else:
            lower = range_figure[-1]
        self.parameters["range_residues"] = [upper, lower]

    def _set_maxima(self):
        if not self._annotation:
            self._annotation = aspecd.annotation.Text()
        maxima = self.get_maxima()
        print(f"Maxima at {maxima} ppm")
        self._annotation.parameters["xpositions"] = self._get_x_positions(
            maxima
        )
        self._get_font_y_offset()
        annotation_offset = -(self._offset * 1.5 + self._font_offset)
        self._annotation.parameters["ypositions"] = annotation_offset
        self._annotation.parameters["texts"] = [
            f"{max_:.0f}" for max_ in maxima
        ]
        self.axes.set_ylim(bottom=annotation_offset)
        for annotation in self.annotations:
            if (
                annotation.parameters["texts"]
                == self._annotation.parameters["texts"]
            ):
                return
        self.annotate(self._annotation)

    def _get_x_positions(self, maxima):
        raw_positions = [n + 2 for n in maxima]
        # TODO:
        # Check the width of the annotation
        # Compare width with delta x so see if annotation overlaps
        # Move the first position to higher ppm, the second to lower ppm. (
        # each half of the overlap)
        # How to deal with new conflicts? Recursive function?
        positions = raw_positions
        return positions

    def _get_font_y_offset(self):
        self._font_size = mpl.rcParams["font.size"]
        font_size_inch = self._font_size / 72  # pt to inch in matplotlib
        font_size_pixels = self.figure.dpi * font_size_inch
        # if self._residues_offset:
        #   _offset = 2*self._residues_offset

        ax_pixels = self.ax.transAxes.transform([(0, 0), (0, 1)])
        ax_extent_pix = ax_pixels[1][1] - ax_pixels[0][1]
        top_percent = font_size_pixels / ax_extent_pix
        ylim = self.ax.get_ylim()
        font_size_data = (ylim[1] - ylim[0]) * top_percent
        self._font_offset = font_size_data
