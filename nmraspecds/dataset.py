"""
dataset module of the nmraspecds package.
"""
import aspecd.dataset
import nmraspecds.metadata


class ExperimentalDataset(aspecd.dataset.ExperimentalDataset):
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

        obj = ExperimentalDataset()
        ...

    

    """

    def __init__(self):
        super().__init__()
        self.metadata = nmraspecds.metadata.ExperimentalDatasetMetadata()


class CalculatedDataset(aspecd.dataset.CalculatedDataset):
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

        obj = CalculatedDataset()
        ...

    

    """

    pass


class DatasetFactory(aspecd.dataset.DatasetFactory):
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

        obj = DatasetFactory()
        ...

    

    """

    pass
