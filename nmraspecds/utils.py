"""
utils module of the nmraspecds package.
"""


def convert_ppm_to_delta_kHz(values, reference_frequency=None):  # noqa
    """
    convert chemical shift values to delta frequency values with the center
    frequency being 0 kHz.

    .. important::

        The chemical shift is given in ppm and the delta frequency is given
        in kHz


    Parameters
    ----------
    values : :class:`np.asarray` | :class:`float`
        chemical shift values to be converted into frequency (kHz)

    reference_frequency : :class:`float`
        reference frequency (spectrometer frequency)

    Returns
    -------
    values : :class:`np.asarray` | :class:`float`
        converted values in kHz.

    """
    return (values * 1e-6 * reference_frequency * 1e6) / 1e3


def convert_delta_kHz_to_ppm(values, reference_frequency=None):  # noqa
    """
    Convert delta frequency values to ppm values with 0 kHz being the
    spectrometer's frequency.

    .. important::

        The chemical shift is given in ppm and delta frequency is given
        in kHz


    Parameters
    ----------
    values : :class:`np.asarray` | :class:`float`
        frequency values (kHz) to be converted into chemical shift (ppm)

    reference_frequency : :class:`float`
        reference frequency (spectrometer frequency)

    Returns
    -------
    values : :class:`np.asarray` | :class:`float`
        converted values in ppm.

    """
    return (values * 1e3 / reference_frequency * 1e6) / 1e6
