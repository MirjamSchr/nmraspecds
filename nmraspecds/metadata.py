"""
metadata module of the nmraspecds package.
"""
import aspecd.metadata


class ExperimentalDatasetMetadata(
    aspecd.metadata.ExperimentalDatasetMetadata
):
    """
    One sentence (on one line) describing the class.

    More description comes here...


    Attributes
    ----------
    spectrometer : :class:`Spectrometer`
        Hardware configuration and details of the setup.

    probehead : :class:`Probehead`
        Details on the probehead used in the experiment

    experiment : :class:`Experiment`
        Experimental details, such as MAS frequency and pulse sequence.

    rotor : :class:`Rotor`
        Rotor size, material, cap and inserts

    Raises
    ------
    exception
        Short description when and why raised


    Examples
    --------
    It is always nice to give some examples how to use the class. Best to do
    that with code examples:

    .. code-block::

        obj = ExperimentalDatasetMetadata()
        ...



    """

    def __init__(self):
        self.spectrometer = Spectrometer()
        self.probehead = Probehead()
        self.experiment = Experiment()
        self.rotor = Rotor()
        super().__init__()


class Sample(aspecd.metadata.Sample):
    """Metadata corresponding to the sample .

    As this class inherits from :class:`aspecd.metadata.Sample`,
    see the documentation of the parent class for details and the full list
    of inherited attributes.

    Parameters
    ----------
    dict_ : :class:`dict`
        Dictionary containing fields corresponding to attributes of the class

    Attributes
    ----------
    description : :class:`str`
        Description of the measured sample.

    solvent : :class:`str`
        Name of the solvent used.

    preparation : :class:`str`
        Short details of the sample preparation.

    tube : :class:`str`
        Type and dimension of the sample tube used.

    """

    def __init__(self, dict_=None):
        # public properties
        self.description = ""
        self.solvent = ""
        self.preparation = ""
        self.tube = ""
        super().__init__(dict_=dict_)


class Spectrometer(aspecd.metadata.Metadata):
    """Metadata information on what type of spectrometer was used.

    Parameters
    ----------
    dict_ : :class:`dict`
        Dictionary containing properties to set.

    Attributes
    ----------
    model : :class:`str`
        Model of the spectrometer used.

    software : :class:`str`
        Name and version of the measurement software.

    """

    def __init__(self, dict_=None):
        self.model = ""
        self.software = ""
        super().__init__(dict_=dict_)


class Probehead(aspecd.metadata.Metadata):
    """Metadata corresponding to the probehead.

    Parameters
    ----------
    dict_ : :class:`dict`
        Dictionary containing properties to set.


    Attributes
    ----------
    model : :class:`str`
        Model of the probehead used.

        Commercial probeheads come with a distinct model that goes in here.
        In all other cases, use a short, memorisable, and unique name.

    configuration : :class:`str`
        Listing of additional coils and capacitors to change the probes'
        frequency.

    """

    def __init__(self, dict_=None):
        self.model = ""
        self.configuration = ""
        super().__init__(dict_=dict_)


class Experiment(aspecd.metadata.Metadata):
    """Metadata corresponding to the experiment.

    More description comes here...


    Attributes
    ----------
    type : :class:`str`

    runs : :class:`int`
        Number of recorded runs.

    nuclei: :class:`list`
        List of involved nuclei.

        Each nucleus is an object of type :class:`Nucleus`

    mas_frequency: :class:`int`
        Magic Angle Spinning Frequency of the experiment, given in Hz.

    spectrometer_frequency: :class:`aspecd.metadata.PhysicalQuantity`
        Spectrometer frequency of the measured nucleus **after referencing**.

        As ssNMR is seldom referenced internally, external referencing is
        necessary to determine the correct frequency of the spectrometer.
        This is done on a standard sample whose chemical shift is known and
        can be set manually. From this, the spectrometer's frequency is
        determined and has to be copied to the sample of interest. Of course,
        the sample has to get measured shortly before or after the reference
        compound to avoid drift of the magnetic field that occurs over time.

    """

    def __init__(self, dict_=None):
        self.type = ""
        self.runs = None
        self.nuclei = []
        self.mas_frequency = None
        self.spectrometer_frequency = aspecd.metadata.PhysicalQuantity()
        self.loops = list()
        self.delays = list()
        super().__init__(dict_=dict_)

    def add_nucleus(self, nucleus):
        # TODO: is this how it is done properly?
        if not isinstance(nucleus, Nucleus):
            TypeError("argument is not of class nmraspecds.metadata.Nucleus")
        self.nuclei.append(nucleus)

    @property
    def spectrum_reference(self):
        value = (
            self.spectrometer_frequency.value
            - self.nuclei[0].transmitter_frequency.value
        )
        quantity = aspecd.metadata.PhysicalQuantity()
        quantity.value = value * 1e6
        quantity.unit = "Hz"
        return quantity


class Nucleus(aspecd.metadata.Metadata):
    """
    One sentence (on one line) describing the class.

    More description comes here...


    Attributes
    ----------
    type : :class:`str`
        Nucleus that is measured, such as 1H or 29Si or 195Pt.

    base_frequency : :class:`aspecd.metadata.PhysicalQuantity`
        Current base frequency of that nucleus.

    offset_hz : :class:`aspecd.metadata.PhysicalQuantity`
        Offset of the nucleus, given in Hz. (O1 in Buker's Topspin)

    Raises
    ------
    exception
        Short description when and why raised


    Examples
    --------
    It is always nice to give some examples how to use the class. Best to do
    that with code examples:

    .. code-block::

        obj = Nucleus()
        ...



    """

    def __init__(self, dict_=None):
        self.type = ""
        self.base_frequency = aspecd.metadata.PhysicalQuantity()
        self.offset_hz = aspecd.metadata.PhysicalQuantity()
        super().__init__(dict_=dict_)

    @property
    def transmitter_frequency(self):
        """Actual frequency of the pulses of the given nucleus.

        Returns
        -------
        transmitter_frequency : :class:`aspecd.metadata.PhysicalQuantity`
        """
        value = self.base_frequency.value + self.offset_hz.value / 1e6
        quantity = aspecd.metadata.PhysicalQuantity()
        quantity.value = value
        quantity.unit = "MHz"
        return quantity

    @property
    def offset_ppm(self):
        """Offset of the pulse in ppm (O1p in Bruker's Topspin)

        Returns
        -------
        offset_ppm : :class:`aspecd.metadata.PhysicalQuantity`
        """
        value = self.offset_hz.value * 1e6 / (self.base_frequency.value * 1e6)
        quantity = aspecd.metadata.PhysicalQuantity()
        quantity.value = value
        quantity.unit = "ppm"
        return quantity


class Rotor(aspecd.metadata.Metadata):
    """
    One sentence (on one line) describing the class.

    More description comes here...


    Attributes
    ----------
    manufacturer : :class:`str`
        Manufacturer of the rotor

    material : :class:`str`
        material, e.g. ZrO2, sapphire, diamond

    diameter : :class:`aspecd:metadata:PhysicalQuantity`
        Outer diameter of the rotor in mm

    cap_material : :class:`str`
        Material of the sealing cap e.g. ZrO2, Kel-F, Vespel

    plug : :class:`str`
        Declares if plug was used and if yes, which one.

    insert : :class:`str`
        Describes insert if one was used,

    Raises
    ------
    exception
        Short description when and why raised


    Examples
    --------
    It is always nice to give some examples how to use the class. Best to do
    that with code examples:

    .. code-block::

        obj = Rotor()
        ...



    """

    def __init__(self, dict_=None):
        self.manufacturer = ""
        self.material = ""
        self.diameter = aspecd.metadata.PhysicalQuantity()
        self.cap_material = ""
        self.plug = ""
        self.insert = ""
        super().__init__(dict_=dict_)
