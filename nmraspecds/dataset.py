"""
dataset module of the nmraspecds package.
"""
import aspecd.dataset
import nmraspecds.metadata
import nmraspecds.io


class DatasetFactory(aspecd.dataset.DatasetFactory):
    """
    Factory for creating dataset objects based on the source provided.

    Particularly in case of recipe-driven data analysis (c.f.
    :mod:`aspecd.tasks`),
    there is a need to automatically retrieve datasets using nothing more
    than a source string that can be, e.g., a path or LOI.

    The DatasetFactory operates in conjunction with a
    :class:`cwepr.io.factory.DatasetImporterFactory` to import the actual
    dataset. See the respective class documentation for more details.


    Attributes
    ----------
    importer_factory : :class:`cwepr.io.factory.DatasetImporterFactory`
        ImporterFactory instance used for importing datasets

    """

    def __init__(self):
        super().__init__()
        self.importer_factory = nmraspecds.io.DatasetImporterFactory()

    @staticmethod
    def _create_dataset(source=""):
        """Return nmraspecds dataset.

        Parameters
        ----------
        source : :class:`str`
            string describing the source of the dataset

            Could be a filename or path, a URL/URI, a LOI, or similar

        Returns
        -------
        dataset : :class:`nmraspecds.dataset.ExperimentalDataset`
            Dataset object for nmraspecds package

        """
        return nmraspecds.dataset.ExperimentalDataset()


class ExperimentalDataset(aspecd.dataset.ExperimentalDataset):
    """
    Set of data uniting all relevant information.

    Core element of the package as all io, processing, analysis ans plotting
    steps are wrapped around a dataset which contains numerical data and
    metadata.

    """

    def __init__(self):
        super().__init__()
        self.metadata = nmraspecds.metadata.ExperimentalDatasetMetadata()


class CalculatedDataset(aspecd.dataset.CalculatedDataset):
    """
    Base class for datasets containing calculated data.


    """

    pass
