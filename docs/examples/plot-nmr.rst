===============================
First overview of a measurement
===============================

Measuring NMR spectra of samples often results in a series of measurements, and one of the first tasks is to get an overview what has been measured and how the results look like.

Classes used:

* Processing

  * :class:`nmraspecds.processing.Normalisation`

* Plotting

  * :class:`nmraspecds.plotting.SinglePlotter1D`
  * :class:`nmraspecds.plotting.MultiPlotter1D`


Recipe
======

.. literalinclude:: plot-nmr.yaml
    :language: yaml
    :linenos:
    :caption: Complete recipe for getting an overview and compare two spectra.


Comments
========

* The recipe starts with information about its version, the default package and the source path of the datasets.

* At the import, the second processing number is called for the 1H dataset, indicated by the `importer_parameter` keyword.

* The 13C data is imported without any further parameters, meaning, that the first processing number is imported

* Both datasets get an ID with which they are called later.

* Directly after the import, both spectra are plotted separately with the `SinglePlotter1D`.

* Then, they are normalized, without further parameters, this is done using the maximum.

* Both spectra are plotted into one figure (ignoring that plotting a 1H spectrum over a 13C spectrum physically makes nearly no sense).


Result
======

.. figure:: ./ProtonSpectrum.png

    1H spectrum

.. figure:: ./CarbonSpectrum.png

    13C spectrum


.. figure:: ./BothSpectra.png

    Both spectra in one figure.