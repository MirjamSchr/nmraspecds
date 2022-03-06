"""
metadata module of the nmraspecds package.
"""
import aspecd.metadata


class ExperimentalDatasetMetadata(aspecd.metadata.ExperimentalDatasetMetadata):
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

        obj = ExperimentalDatasetMetadata()
        ...

    

    """

    pass


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
        self.description = ''
        self.solvent = ''
        self.preparation = ''
        self.tube = ''
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
        Name and version of the software used.

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

    """

    def __init__(self, dict_=None):
        self.model = ""
        super().__init__(dict_=dict_)


class Experiment:
    """Metadata corresponding to to the experiment.

    More description comes here...


    Attributes
    ----------
    type : :class:`str`

    runs : :class:`int`
        Number of recorded runs.

    nucleus: :class:`str`
        Nucleus on which it was measured.

    mas_frequency: :class:`int`
        Magic Angle Spinning Frequency of the experiment, given in Hz.
    """

    def __init__(self, dict_=None):
        self.type = ""
        self.runs = None
        self.nucleus = None
        self.mas_frequency = None
        super().__init__(dict_=dict_)

