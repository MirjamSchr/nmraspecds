"""
metadata module of the nmraspecds package.
"""
import aspecd.metadata


class ExperimentalDatasetMetadata(
    aspecd.metadata.ExperimentalDatasetMetadata
):
    """
    Set of all metadata for a dataset object.

    Metadata as a unified structure of information coupled to the dataset are
    necessary for the understanding, analysis and processing of data,
    especially in NMR.
    Some parameters are written automatically by the
    spectrometer's software, others, depending also on the actual setup (that
    may change over time!) are omitted. It is highly recommended those
    parameters should be noted by hand, for example in an *.info-file.*

    ..note ::

        Not all parameters are yet taken into account, only the most
        important ones, that are needed for processing and analysis that are
        already implemented.


    Attributes
    ----------
    spectrometer : :class:`Spectrometer`
        Hardware configuration and details of the setup.

    probehead : :class:`Probehead`
        Details on the probehead used in the experiment

    experiment : :class:`Experiment`
        Experimental details, such as MAS frequency and pulse sequence.

    sample : :class:`Sample`
        Details on the sample used for this experiment as well as its container.


    """

    def __init__(self):
        super().__init__()
        self.spectrometer = Spectrometer()
        self.probehead = Probehead()
        self.experiment = Experiment()
        self.sample = Sample()


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

    container : :class:`SampleContainer`
        Type and dimension of the sample container (tube or rotor) used.

    """

    def __init__(self, dict_=None):
        # public properties
        self.description = ""
        self.solvent = ""
        self.preparation = ""
        self.container = Rotor()
        super().__init__(dict_=dict_)


class SampleContainer(aspecd.metadata.Metadata):
    """Details on the sample containing container."""


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
        Current spectrometer frequency of the dataset.

        Current spectrometer frequency ("SF" in Bruker's Topspin) of the
        dataset. Is different from the transmitter frequency (and independend of
        it) depending on the axis. The value is obtained after referencing
        the measurement.

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
            - self.nuclei[0].base_frequency.value
        )
        quantity = aspecd.metadata.PhysicalQuantity()
        quantity.value = value * 1e6
        quantity.unit = "Hz"
        return quantity


class Nucleus(aspecd.metadata.Metadata):
    """
    Metadata to describe the observed nucleus.

    The here mentioned frequencies are the settings given in the pulse
    program: The base frequency of the nucleus that corresponds to the
    current magnetic field (and that needs to get recalibrated from time to
    time) and the offset if one wants to excite  the nucleus with a certain
    offset and not at 0 ppm.

    Attributes
    ----------
    type : :class:`str`
        Nucleus that is observed, such as 1H or 29Si or 195Pt.

    base_frequency : :class:`aspecd.metadata.PhysicalQuantity`
        Current base frequency of a given nucleus.

    offset_hz : :class:`aspecd.metadata.PhysicalQuantity`
        Offset of the nucleus' frequency, given in Hz. (O1 in Buker's Topspin)


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


class Rotor(SampleContainer):
    """
    Details on the rotor used for the experiment.


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


    """

    def __init__(self, dict_=None):
        self.manufacturer = ""
        self.material = ""
        self.diameter = aspecd.metadata.PhysicalQuantity()
        self.cap_material = ""
        self.plug = ""
        self.insert = ""
        super().__init__(dict_=dict_)
