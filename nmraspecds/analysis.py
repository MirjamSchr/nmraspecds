"""
analysis module of the nmraspecds package.
"""
import aspecd.analysis
import numpy as np


class ChemicalShiftCalibration(aspecd.analysis.SingleAnalysisStep):
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

        obj = ChemicalShiftCalibration()
        ...

    

    """

    def __init__(self):
        super().__init__()
        self.description = ('Determine chemical shift offset from a standard '
                            'sample')
        self.parameters['spectrometer_frequency'] = None
        self.parameters['standard'] = ''
        self.parameters['chemical_shift'] = None
        self._peak_index = None

    def _sanitise_parameters(self):
        if (not self.dataset.metadata.experiment.spectrometer_frequency.value
                and not self.parameters['spectrometer_frequency']):
            raise ValueError('No spectrometer frequency provided, aborting.')
        if (not self.parameters['standard']
                and not self.parameters['chemical_shift']):
            raise ValueError('No standard or chemical shift value provided.')

    def _perform_task(self):
        self._calculate_new_frequency()
        self.result = self._update_axis_and_return_offset()

    def _update_axis_and_return_offset(self):
        offset_ppm = (self.parameters['chemical_shift'] -
                      self.dataset.data.axes[0].values[self._peak_index])
        self.dataset.data.axes[0].values += offset_ppm
        return offset_ppm

    def _calculate_new_frequency(self):
        self._peak_index = np.argmax(self.dataset.data.data)
        ppm_current = self.dataset.data.axes[0].values[self._peak_index]
        ppm_target = self.parameters['chemical_shift']
        initial_frequency = (
            self.dataset.metadata.experiment.spectrometer_frequency.value)
        nu_current = ppm_current * initial_frequency
        nu_target = ppm_target * initial_frequency
        delta_nu = nu_target - nu_current
        new_frequency = (initial_frequency * 1e6 - delta_nu) * 1e-6  # in MHz
        self.dataset.metadata.experiment.spectrometer_frequency.value = (
            new_frequency)
