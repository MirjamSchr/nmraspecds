"""
analysis module of the nmraspecds package.
"""
import aspecd.analysis
import numpy as np
import scipy.signal


class ChemicalShiftCalibration(aspecd.analysis.SingleAnalysisStep):
    """
    Calculate offset between transmitter and current spectrometer frequency.

    As ssNMR is seldom referenced internally, external referencing is
    necessary to determine the correct frequency of the spectrometer.
    This is done on a standard sample whose chemical shift is known and
    can be set manually. From this, the offset from the spectrometer's
    frequency is determined (this step) and has to be transferred to the
    sample of interest (see :class:`nmraspecds.processing.ExternalReferencing`).
     Of course, the sample has to get measured shortly before or after the
    reference compound to avoid drift of the magnetic field that occurs over
    time.

    Currently, the following standards are supported:

    ==================  ==========  =======  ====================  =========
    Substance           Name        Nucleus  chemical shift / ppm  Reference
    ==================  ==========  =======  ====================  =========
    Adamantane          adamantane  1H       1.8                   [0]
    Adamantane          adamantane  13C      37.77 (low field)     [0]
    Ammoniumophosphate  NH4H2PO3    31P      1.33                  [0]
    Alanine             alanine     13C      176.8 (high field)    [0]
    Q8M8                Q8M8        29Si     11.66                 [1]
    Al(H2O)3+           Aluminum    27Al     0                     [0]
    ==================  ==========  =======  ====================  =========

    Q8M8 = Octakis(trimethylsiloxy)silsesquioxane

    The column "name" here refers to the value the parameter ``standard`` can
    take (see below). These names are case-insensitive. If multiple peaks are
    present, the one indicated in the table above will be considered.

    Eventually, the offset is returned which corresponds to the "SR" value in
    Bruker's TopSpin software.

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
        contains additional information e.g. type of nucleus.

        Default: value

    Returns
    -------
    offset:
        Can be a single number or a dict. The dict additionally contains the
        nucleus that is given in the dataset. With this, in the next step,
        the offset is automatically converted if the dataset is acquired on
        another nucleus.


    Raises
    ------
    ValueError
        Either Standard sample or chemical shift to reference to needs to be
        provided.

    Examples
    --------

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
        self._offset = None
        self._standard_shifts = {
            "adamantane": {
                "1H": 1.8,
                "13C": 37.77,
            },
            "nh4h2po4": {
                "31P": 1.33,
            },
            "alanine": {"13C": 176.8},
            "q8m8": {"29Si": 11.66},
            "aluminum": {"27Al": 0},
        }
        self._peak_list = {
            "adamantane": {"13C": 1},
            "alanine": {"13C": 1},
        }

    def _sanitise_parameters(self):
        if (
            not self.parameters["standard"]
            and self.parameters["chemical_shift"] == None
        ):
            raise ValueError("No standard or chemical shift value provided.")
        if self._standard_given_but_nucleus_not():
            if self._only_one_nucleus_in_standards_list():
                self.parameters["nucleus"] = self._standard_shifts[
                    self.parameters["standard"]
                ]

            raise ValueError(
                "Type of nucleus undetermined, cannot assign standard."
            )

    def _only_one_nucleus_in_standards_list(self):
        return (
            len(self._standard_shifts[self.parameters["standard"]].keys())
            == 1
        )

    def _standard_given_but_nucleus_not(self):
        return self.parameters["standard"] and (
            len(self.dataset.metadata.experiment.nuclei) == 0
            or not self.dataset.metadata.experiment.nuclei[0].type
            or "nucleus" not in self.parameters.keys()
        )

    def _perform_task(self):
        self._assign_parameters()
        self._get_offset()
        self._assign_result()

    def _assign_parameters(self):
        self.parameters["nucleus"] = self.dataset.metadata.experiment.nuclei[
            0
        ].type
        if self.parameters["chemical_shift"] == None:
            standard = self.parameters["standard"].lower()
            self.parameters["chemical_shift"] = self._standard_shifts[
                standard
            ][self.parameters["nucleus"]]

    def _get_offset(self):
        self._get_peak_index()
        ppm_current = self.dataset.data.axes[0].values[self._peak_index]
        ppm_target = self.parameters["chemical_shift"]
        current_freq = (
            self.dataset.metadata.experiment.spectrometer_frequency.value
        )
        trans_freq = self.dataset.metadata.experiment.nuclei[
            0
        ].transmitter_frequency.value
        nu_current = self.dataset.metadata.experiment.spectrum_reference.value
        nu_peak_target = ppm_target * current_freq
        nu_peak_current = ppm_current * current_freq
        nu_peak_zero = nu_peak_current + nu_current
        diff_nu = nu_peak_zero - nu_peak_target
        self._offset = diff_nu

    def _get_peak_index(self):
        peak_indices, _ = scipy.signal.find_peaks(
            self.dataset.data.data,
            height=0.2 * max(self.dataset.data.data),
            distance=0.05 * len(self.dataset.data.data),
        )
        if len(peak_indices) > 1:
            index = (
                self._peak_list[self.parameters["standard"]][
                    self.parameters["nucleus"]
                ]
                - 1
            )
            self._peak_index = peak_indices[-index]
        else:
            self._peak_index = peak_indices[0]

    def _assign_result(self):
        if self.parameters["return_type"] == "value":
            self.result = self._offset
        elif self.parameters["return_type"] == "dict":
            self.result = {
                "offset": self._offset,
                "nucleus": self.parameters["nucleus"],
            }
