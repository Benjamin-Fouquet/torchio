#!/usr/bin/env python

"""Tests for `torchio` package."""


import unittest
import torch
import numpy as np
from torchio import INTENSITY, LABEL

from torchio.transforms import (
    RandomFlip,
    RandomNoise,
    RandomBiasField,
    RandomElasticDeformation,
    RandomAffine,
    RandomMotion,
    Rescale,
    ZNormalization,
    HistogramStandardization,
)


class TestTransforms(unittest.TestCase):
    """Tests for all transforms."""

    def get_sample(self):
        shape = 1, 10, 20, 30
        np.random.seed(42)
        affine = np.diag((1, 2, 3, 1))
        affine[:3, 3] = 40, 50, 60
        sample = {
            't1': dict(
                data=self.getRandomData(shape),
                affine=affine,
                type=INTENSITY,
            ),
            't2': dict(
                data=self.getRandomData(shape),
                affine=affine,
                type=INTENSITY,
            ),
            'label': dict(
                data=(self.getRandomData(shape) > 0.5).float(),
                affine=affine,
                type=LABEL,
            ),
        }
        return sample

    @staticmethod
    def getRandomData(shape):
        return torch.rand(*shape)

    def test_transforms(self):
        random_transforms = (
            RandomFlip,
            RandomNoise,
            RandomBiasField,
            RandomElasticDeformation,
            RandomAffine,
            RandomMotion,
        )
        intensity_transforms = (
            Rescale,
            ZNormalization,
            HistogramStandardization,
        )
        default_kwargs = dict(seed=42)

        for transform in random_transforms:
            sample = self.get_sample()
            kwargs = {}
            kwargs.update(default_kwargs)
            if transform == RandomElasticDeformation:
                kwargs['proportion_to_augment'] = 1
            transformed = transform(**kwargs)(sample)

        for transform in intensity_transforms:
            sample = self.get_sample()
            kwargs = {}
            if transform == HistogramStandardization:
                kwargs['landmarks_dict'] = dict(
                    t1=np.linspace(0, 100, 13),
                    t2=np.linspace(0, 100, 13),
                )
            transformed = transform(**kwargs)(sample)