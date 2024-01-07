"""
io module of the nmraspecds package.
"""
import os.path

import aspecd.io
import nmrglue


class DatasetImporterFactory(aspecd.io.DatasetImporterFactory):
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

        obj = DatasetImporterFactory()
        ...



    """

    def _get_importer(self):
        return BrukerImporter(source=self.source)


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

    def __init__(self, source=None):
        super().__init__(source=source)
        self.parameters['type'] = 'proc'
        self.parameters['processing_number'] = 1
        self._parameters = None
        self._data = None

    def _import(self):
        self._check_for_type()
        self._read_data()
        self._create_axes()

    def _create_axes(self):
        unified_dict = nmrglue.bruker.guess_udic(self._parameters, self._data)
        unit_converter = nmrglue.bruker.fileiobase.uc_from_udic(unified_dict)
        self.dataset.data.axes[0].values = unit_converter.ppm_scale()

        self.dataset.data.axes[0].unit = 'ppm'
        self.dataset.data.axes[0].quantity = 'chemical shift'
        self.dataset.data.axes[1].quantity = 'intensity'

    def _read_data(self):
        if 'pdata' in self.source:
            self._parameters, self._data = nmrglue.bruker.read_pdata(
                self.source)
        else:
            self._parameters, self._data = nmrglue.bruker.read(self.source)
        self.dataset.data.data = self._data

    def _check_for_type(self):
        if ('type' in self.parameters and
                self.parameters['type'].startswith('proc') and
                'pdata' not in self.source):
            self.source = os.path.join(self.source, 'pdata',
                                       str(self.parameters[
                                               'processing_number']))
