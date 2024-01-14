"""
analysis module of the nmraspecds package.
"""
import aspecd.analysis
import numpy as np


class ChemicalShiftCalibration(aspecd.analysis.SingleAnalysisStep):
    """
    Calculate offset between transmitter and current spectrometer frequency.

    As ssNMR is seldom referenced internally, external referencing is
    necessary to determine the correct frequency of the spectrometer.
    This is done on a standard sample whose chemical shift is known and
    can be set manually. From this, the offset from the spectrometer's
    frequency is determined (this step) and has to be transferred to the
    sample of interest (see :class:`nmraspecds.processing.ExternalReferencing
    `). Of
    course,
    the sample has to get measured shortly before or after the reference
    compound to avoid drift of the magnetic field that occurs over time.

    Currently, the following field standards are supported:

    ==================  ==========  =======  ====================  =========
    Substance           Name        Nucleus  chemical shift / ppm  Reference
    ==================  ==========  =======  ====================  =========
    Adamantane          adamantane  1H       1.8                   [0]
    Adamantane          adamantane  13C      37.77 (low field)     [0]
    Ammoniumophosphate  NH4H2PO3    31P      1.33                  [0]
    Alanine             alanine     13C      19.8 (high field)     [0]
    Q8M8                Q8M8        29Si     11.66                 [1]
    Al(H2O)3+           Aluminum    27Al     0                     [0]
    ==================  ==========  =======  ====================  =========

    Q8M8 = Octakis(trimethylsiloxy)silsesquioxane

    The column "name" here refers to the value the parameter ``standard`` can
    take (see below). These names are case-insensitive.

    References
    ----------
    [1] Solid State Nucl. Magn. Res. 1992, 1, 41 - 44

    Attributes
    ----------
    parameters["chemical_shift"]: :class:`float`
        Chemical shift the largest peaks should be shifted to.

    parameters["standard"]: :class:`str`
        Standard substance to take chemical shift from. Either the parameter
        "chemical_shift" or "standard" need to be provided.


    parameters["return_type"]: :class:`str`
        Defines, type of output, can be "value" or "dict". The latter
        contains additional information e.g. Type of nucleus.

        Default: value


    Raises
    ------
    ValueError
        Either Standard sample or chemical shift to reference to needs to be
        provided.

    Examples
    --------
    It is always nice to give some examples how to use the class. Best to do
    that with code examples:

    .. code-block:: yaml

        - kind: singleanalysis
          type: ChemicalShiftCalibration
          properties:
            parameters:
              standard: adamantane
              nucleus: 1H
          result: offset

    """

    def __init__(self):
        super().__init__()
        self.description = (
            "Determine chemical shift offset from a standard " "sample"
        )

        self.parameters["standard"] = ""
        self.parameters["chemical_shift"] = None
        self.parameters["nucleus"] = None
        self.parameters["return_type"] = "value"
        self._peak_index = None
        self._nucleus = None
        self._offset = None
        self._standard_shifts = {
            "adamantane": {"1H": 1.8, "13C": 37.77},
            "nh4h2po3": {
                "31P": 1.33,
            },
            "alanine": {
                "13C": 19.8  # TODO: Is this the signal used for referencing?
            },
            "q8m8": {"29Si": 11.66},
            "aluminum": {"27Al": 0},
        }

    def _sanitise_parameters(self):
        if (
            not self.parameters["standard"]
            and not self.parameters["chemical_shift"]
        ):
            raise ValueError("No standard or chemical shift value provided.")
        if self.parameters["standard"] and (
            len(self.dataset.metadata.experiment.nuclei) == 0
            or not self.dataset.metadata.experiment.nuclei[0].type
            or "nucleus" not in self.parameters.keys()
        ):
            print("Bin in Schleife")
            if (
                len(self._standard_shifts[self.parameters["standard"]].keys())
                == 1
            ):
                self.parameters["nucleus"] = self._standard_shifts[
                    self.parameters["standard"]
                ]

            print("here")
            raise ValueError(
                "Type of nucleus undetermined, cannot assign standard."
            )

    def _perform_task(self):
        self._assign_parameters()
        self._get_offset()
        self._assign_result()

    def _assign_parameters(self):
        if not self.parameters["chemical_shift"]:
            standard = self.parameters["standard"].lower()
            self._nucleus = self.dataset.metadata.experiment.nuclei[0].type
            self.parameters["chemical_shift"] = self._standard_shifts[
                standard
            ][self._nucleus]

    def _get_offset(self):
        self._peak_index = np.argmax(self.dataset.data.data)
        ppm_current = self.dataset.data.axes[0].values[self._peak_index]
        ppm_target = self.parameters["chemical_shift"]
        current_freq = (
            self.dataset.metadata.experiment.spectrometer_frequency.value
        )
        trans_freq = self.dataset.metadata.experiment.nuclei[
            0
        ].transmitter_frequency.value
        nu_current = self.dataset.metadata.experiment.spectrum_reference.value
        assert current_freq == trans_freq + nu_current * 1e-6
        nu_peak_target = ppm_target * current_freq
        nu_peak_current = ppm_current * current_freq
        nu_peak_zero = nu_peak_current + nu_current
        diff_nu = nu_peak_zero - nu_peak_target
        self._offset = diff_nu

    def _assign_result(self):
        if self.parameters["return_type"] == "value":
            self.result = self._offset
        elif self.parameters["return_type"] == "dict":
            self.result = {"offset": self._offset, "nucleus": self._nucleus}
