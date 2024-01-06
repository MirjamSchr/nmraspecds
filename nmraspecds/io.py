"""
io module of the nmraspecds package.
"""
import aspecd.io
import nmrglue


class BrukerImporter(aspecd.io.DatasetImporter):
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

        obj = BrukerImporter()
        ...

    

    """

    def _import(self):
        parameters, data = nmrglue.bruker.read(self.source)
        self.dataset.data.data = data
