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

    def __init__(self):
        super().__init__()
        self.parameters['offset'] = None

    def _sanitise_parameters(self):
        if ('offset' not in self.parameters.keys() or
                self.parameters['offset'] is None):
            raise ValueError('No offset provided')

    def _perform_task(self):
        print(self.parameters['offset'])
        self.parameters
        delta_nu_1 = 1
        #self._change_axis()
        #self._update_spectrometer_frequency()
        print(self.dataset.metadata.experiment.spectrometer_frequency)

    def _update_spectrometer_frequency(self):
       # print(self.dataset.metadata.experiment.spectrometer_frequency,
        #      '\n base frequency',
         #     self.dataset.metadata.experiment.nuclei[0].base_frequency.value)
        initial_frequency = (
            self.dataset.metadata.experiment.nuclei[
                0].transmitter_frequency.value)
        offset_hz = self.parameters['offset'] * initial_frequency
        frequency = (initial_frequency * 1e6 + offset_hz) * 1e-6
        self.dataset.metadata.experiment.spectrometer_frequency.value = (
            frequency)

    def _change_axis(self):
        for axis in self.dataset.data.axes:
            if axis.unit in ('ppm', 'Hz'):
                axis.values += self.parameters['offset']
