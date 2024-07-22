"""
plotting module of the nmraspecds package.
"""
import aspecd.plotting

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
            "top", functions=(backward, forward)
        )
        freq_axis.set_xlabel(r"$\Delta \nu\ $kHz")


class SinglePlotter1D(aspecd.plotting.SinglePlotter1D, PlotterExtensions):
    """1D plots of single datasets.

    Convenience class taking care of 1D plots of single datasets.

    As the class is fully inherited from ASpecD for simple usage, see the
    ASpecD documentation of the :class:`aspecd.plotting.SinglePlotter1D`
    class for details.

    Furthermore, the class inhertis all functionality from
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
    One sentence (on one line) describing the class.

    More description comes here...


    Attributes
    ----------
    attr : :class:`None`
        Short description

    Raises
    ------
    exception
        Short description when and why raised


    Examples
    --------
    It is always nice to give some examples how to use the class. Best to do
    that with code examples:

    .. code-block::

        obj = FittingPlotter2D()
        ...



    """

    def __init__(self):
        super().__init__()
        self.parameters["offset"] = 0

    def _create_plot(self):
        super()._create_plot()
        props = self.properties.get_properties()
        print(self.properties.drawing.color)
        self.properties.drawing.color = "grey"
        # TODO: Problem: SinglePlotter2DStacked ist nur für eine Farbe
        #  ausgelegt.
        colors = [
            "k",
            "tab:red",
            "tab:gray",
            "tab:gray",
            "tab:gray",
            "tab:gray",
        ]

    # TODO: Account for stacking dimension
