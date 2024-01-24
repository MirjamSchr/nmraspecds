"""
processing module of the nmraspecds package.
"""
import logging

import aspecd.processing
import spindata

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ExternalReferencing(aspecd.processing.SingleProcessingStep):
    """
    Referencing of the dataset to a given offset (in Hz).

    Following the analysis step
    :class:`nmraspecds:analysis:ChemicalShiftCalibration`, in this processing
    step, the axis of the dataset is adapted using the provided offset to
    reference the spectrum.

    Often it is necessary to reference to a chemical shift of a different
    type of nucleus. This is accounted for with adapting the offset to the
    dataset's nucleus in the case, both types of nuclei are given. The
    gyromagnetic ratios (γ/10^7 rad s^–1 T^–1) [1] are used via spindata by
    Benno Meier.

    References
    ----------

    [1] https://doi.org/10.1351/pac200173111795

    Attributes
    ----------
    parameters["offset"] : :class:`float` or :class:`dict`
        Offset (in Hz) to add to the base frequency to obtain correct axis.

    Raises
    ------
    exception
        Short description when and why raised


    Examples
    --------
    In the simplest case, the offset is known and can just be inserted here:

    .. code-block:: yaml

        - kind: processing
          type: ExternalReferencing
          properties:
            parameters:
              offset: 532

    More sophisticatedly, the type of nucleus is also given to automatically
    account for the gyromagnetic ratios of the nuclei:

    .. code-block:: yaml

        - kind: processing
          type: ExternalReferencing
          properties:
            parameters:
              offset: 532
              offset_nucleus: 13C


    In reality, the combination of the analysis step with the corresponding
    processing step is powerful to use and could look as follows:

    .. code-block:: yaml

        - kind: singleanalysis
          type: ChemicalShiftCalibration
          properties:
            parameters:
              standard: adamantane
              nucleus: 1H
          result: my_offset

        - kind: processing
          type: ExternalReferencing
          properties:
            parameters:
              offset: my_offset


    """

    def __init__(self):
        super().__init__()
        self.parameters["offset"] = None
        self.parameters["offset_nucleus"] = None
        self._target_spectrometer_frequency_value = float
        self._delta = None

    def _sanitise_parameters(self):
        if (
            "offset" not in self.parameters.keys()
            or self.parameters["offset"] is None
        ):
            raise ValueError("No offset provided")
        if (
            len(self.dataset.metadata.experiment.nuclei) == 0
            or not self.dataset.metadata.experiment.nuclei[0].type
        ):
            logger.warning(
                "No nucleus given in current dataset. Values are "
                "taken as they come, no guarantee for correct "
                "results."
            )

    def _perform_task(self):
        if isinstance(self.parameters["offset"], dict):
            self._rewrite_parameters()
        self._offset = self.parameters["offset"]
        if self._nuclei_differ():
            self._calcuate_offset_for_different_nucleus()
        self._update_axis_with_correct_offset()
        self._update_spectrometer_frequency()

    def _rewrite_parameters(self):
        # nucleus is nucleus to which offset was obtained!
        self.parameters["offset_nucleus"] = self.parameters["offset"][
            "nucleus"
        ]
        self.parameters["offset"] = self.parameters["offset"]["offset"]

    def _nuclei_differ(self):
        if (
            "offset_nucleus" not in self.parameters.keys()
            or not self.dataset.metadata.experiment.nuclei[0].type
        ):
            logger.info(
                "Nucleus is supposed to be of the same type as in "
                "the dataset."
            )
            return False
        return (
            self.parameters["offset_nucleus"]
            != self.dataset.metadata.experiment.nuclei[0].type
        )

    def _calcuate_offset_for_different_nucleus(self):
        self._offset = self.parameters["offset"]
        self._offset /= spindata.gamma(self.parameters["offset_nucleus"])
        self._offset *= spindata.gamma(
            self.dataset.metadata.experiment.nuclei[0].type
        )

    def _update_axis_with_correct_offset(self):
        target_delta_nu = self._offset
        current_sr_hz = (
            self.dataset.metadata.experiment.spectrum_reference.value
        )
        delta_sr_hz = target_delta_nu - current_sr_hz  # Additional offset
        self._delta = delta_sr_hz
        self._target_spectrometer_frequency_value = (
            self.dataset.metadata.experiment.nuclei[0].base_frequency.value
            + target_delta_nu / 1e6
        )
        # ppm_to_add = delta_sr_hz / self._target_spectrometer_frequency_value
        # ppm_to_add = delta_sr_hz / self.dataset.metadata.experiment.nuclei[
        #   0].base_frequency.value
        # TODO: Frequency did not make a difference on the axis yet. Don't
        #  know why.
        ppm_to_add = (
            delta_sr_hz
            / self.dataset.metadata.experiment.nuclei[
                0
            ].transmitter_frequency.value
        )
        self.dataset.data.axes[0].values -= ppm_to_add

    def _update_spectrometer_frequency(self):
        self.dataset.metadata.experiment.spectrometer_frequency.value = (
            self._target_spectrometer_frequency_value
        )


class NormalisationToNumberOfScans(aspecd.processing.SingleProcessingStep):
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

        obj = NormalisationToNumberOfScans()
        ...



    """

    def _perform_task(self):
        self.dataset.data.data /= self.dataset.metadata.experiment.runs
