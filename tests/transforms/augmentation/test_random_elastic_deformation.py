import warnings
import numpy as np
import torchio
from torchio.transforms import RandomElasticDeformation
from ...utils import TorchioTestCase


class TestRandomElasticDeformation(TorchioTestCase):
    """Tests for `RandomElasticDeformation`."""

    def test_random_elastic_deformation(self):
        transform = RandomElasticDeformation(
            num_control_points=5,
            max_displacement=(2, 3, 5),  # half grid spacing is (3.3, 3.3, 5)
            seed=42,
        )
        keys = ('t1', 't2', 'label')
        fixtures = 2953.9197, 2989.769, 2975
        transformed = transform(self.sample)
        for key, fixture in zip(keys, fixtures):
            sample_data = self.sample[key][torchio.DATA].numpy()
            transformed_data = transformed[key][torchio.DATA].numpy()
            transformed_total = transformed_data.sum()
            # Make sure that intensities have changed
            assert not np.array_equal(sample_data, transformed_data)
            self.assertAlmostEqual(transformed_total, fixture, places=4)

    def test_inputs_pta_gt_one(self):
        with self.assertRaises(ValueError):
            RandomElasticDeformation(proportion_to_augment=1.5)

    def test_inputs_pta_lt_zero(self):
        with self.assertRaises(ValueError):
            RandomElasticDeformation(proportion_to_augment=-1)

    def test_inputs_interpolation_int(self):
        with self.assertRaises(TypeError):
            RandomElasticDeformation(image_interpolation=1)

    def test_inputs_interpolation_string(self):
        with self.assertRaises(TypeError):
            RandomElasticDeformation(image_interpolation='linear')

    def test_deprecation(self):
        with self.assertWarns(DeprecationWarning):
            RandomElasticDeformation(deformation_std=15)

    def test_num_control_points_noint(self):
        with self.assertRaises(ValueError):
            RandomElasticDeformation(num_control_points=2.5)

    def test_num_control_points_small(self):
        with self.assertRaises(ValueError):
            RandomElasticDeformation(num_control_points=3)

    def test_max_displacement_no_num(self):
        with self.assertRaises(ValueError):
            RandomElasticDeformation(max_displacement=None)

    def test_max_displacement_negative(self):
        with self.assertRaises(ValueError):
            RandomElasticDeformation(max_displacement=-1)

    def test_wrong_locked_borders(self):
        with self.assertRaises(ValueError):
            RandomElasticDeformation(locked_borders=-1)

    def test_coarse_grid_removed(self):
        with self.assertRaises(ValueError):
            RandomElasticDeformation(
                num_control_points=(4, 5, 6),
                locked_borders=2,
            )

    def test_folding(self):
        # Assume shape is (10, 20, 30) and spacing is (1, 1, 1)
        # Then grid spacing is (10/(12-2), 20/(5-2), 30/(5-2))
        # or (1, 6.7, 10), and half is (0.5, 3.3, 5)
        transform = RandomElasticDeformation(
            num_control_points=(12, 5, 5),
            max_displacement=6,
        )
        with self.assertWarns(UserWarning):
            transformed = transform(self.sample)

    def test_num_control_points(self):
        RandomElasticDeformation(num_control_points=5)
        RandomElasticDeformation(num_control_points=(5, 6, 7))

    def test_max_displacement(self):
        RandomElasticDeformation(max_displacement=5)
        RandomElasticDeformation(max_displacement=(5, 6, 7))

    def test_deformation_std(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # This test is to be deleted with the parameter
            RandomElasticDeformation(deformation_std=5)
            RandomElasticDeformation(deformation_std=(5, 6, 7))
