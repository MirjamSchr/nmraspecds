"""
processing module of the nmraspecds package.
"""
import aspecd.processing


class ExternalReferencing(aspecd.processing.SingleProcessingStep):
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

        obj = ExternalReferencing()
        ...

    

    """

    def _perform_task(self):
        for axis in self.dataset.data.axes:
            if axis.unit in ('ppm', 'Hz'):
                axis.values += self.parameters['offset']

        # correct spectrometer frequency
        initial_frequency = (
            self.dataset.metadata.experiment.spectrometer_frequency.value)
        offset_hz = self.parameters['offset']* initial_frequency
        frequency = (initial_frequency* 1e6 + offset_hz)*1e-6
        self.dataset.metadata.experiment.spectrometer_frequency.value = (
            frequency)
