from abc import ABC, abstractmethod
from typing import Tuple
from ..utilities import is_rotation_matrix, is_translation_vector
import numpy as np


class Camera(ABC):
    """Abstract class for a camera. A camera should produce """

    def __init__(self, image_shape: Tuple[int]) -> None:
        self.image_shape = image_shape

    def render_with_pose(self, R: np.ndarray, t: np.ndarray) -> np.ndarray:
        """Wrapper for the camera-specific render function."""
        assert is_rotation_matrix(R) and is_translation_vector(t)
        image = self._render_with_pose(R, t)
        assert isinstance(image, np.ndarray) and image.shape == self.image_shape
        return image

    @abstractmethod
    def _render_with_pose(self, R: np.ndarray, t: np.ndarray) -> np.ndarray:
        raise Exception("Not implemented.")