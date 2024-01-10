"""
io module of the nmraspecds package.
"""
import os.path

import aspecd.io
import nmrglue
import numpy as np

import nmraspecds.metadata


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
        self._get_spectrometer_frequency()
        self._add_nuclei()

    def _add_nuclei(self):

        nuclei = dict()
        for key, value in self._parameters['acqus'].items():
            if key.startswith('NUC') and value != 'off':
                nuclei[key] = value
        for key in sorted(nuclei.keys()):
            self._add_nucleus(key)

    def _get_spectrometer_frequency(self):
        self.dataset.metadata.experiment.spectrometer_frequency.value = (
            self._parameters)['procs']['SF']

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

    def _add_nucleus(self, nuc='', ):
        nr = nuc[-1]
        nucleus = nmraspecds.metadata.Nucleus()
        nucleus.type = self._parameters['acqus'][nuc]
        nucleus.base_frequency.value = self._parameters['acqus'][f'BF{nr}']
        nucleus.base_frequency.unit = 'MHz'
        nucleus.offset_hz.value = float(self._parameters['acqus'][f'O{nr}'])
        nucleus.offset_hz.unit = 'Hz'
        self.dataset.metadata.experiment.add_nucleus(nucleus)


class ScreamImporter(aspecd.io.DatasetImporter):
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

        obj = ScreamImporter()
        ...

    """

    def __init__(self, source=None):
        super().__init__(source=source)
        self.parameters['number_of_experiments'] = 1
        self._tmp_data = None

    def _import(self):
        base_path, last_element = os.path.split(self.source)
        for count, variable_element in (
                enumerate(np.arange(int(last_element), int(last_element) +
                                    self.parameters['number_of_experiments']))):
            self.source = os.path.join(base_path, str(variable_element),
                                       'pdata', '103')
            self._parameters, self._data = \
                nmrglue.bruker.read_pdata(self.source)
            if self._tmp_data is None:
                self._tmp_data = np.ndarray((len(self._data), self.parameters[
                    'number_of_experiments']))
            self._tmp_data[:, count] = self._data
        self.dataset.data.data = self._tmp_data
