import unittest

import numpy as np

from nmraspecds import utils


class TestConvertPpmToDeltakHz(unittest.TestCase):
    def test_values_are_positive(self):
        values = np.linspace(1, 50, 50)
        reference_frequency = 400
        self.assertTrue(
            all(
                utils.convert_ppm_to_delta_kHz(values, reference_frequency)
                > 0
            )
        )

    def test_values_have_correct_range(self):
        values = np.linspace(1, 50, 50)
        reference_frequency = 400
        self.assertAlmostEqual(
            20,
            utils.convert_ppm_to_delta_kHz(values, reference_frequency)[-1],
        )


class TestConvertDeltakHzToPpm(unittest.TestCase):
    def test_values_are_positive(self):
        values = np.linspace(1, 20, 50)
        reference_frequency = 400
        self.assertTrue(
            all(
                utils.convert_delta_kHz_to_ppm(values, reference_frequency)
                > 0
            )
        )

    def test_values_have_correct_range(self):
        values = np.linspace(1, 20, 50)
        reference_frequency = 400
        self.assertAlmostEqual(
            50,
            utils.convert_delta_kHz_to_ppm(values, reference_frequency)[-1],
        )
