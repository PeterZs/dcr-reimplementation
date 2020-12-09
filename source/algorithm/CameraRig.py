import numpy as np
from typing import List
from ..camera.Camera import Camera
from ..utilities import is_rotation_matrix, is_translation_vector


class CameraRig:
    # This is the camera the rig is holding.
    camera: Camera

    # These hold the unknown transformation from hand to eye.
    hand_eye_R: np.ndarray
    hand_eye_t: np.ndarray

    # These hold the hand's (robot's) current position.
    hand_R: np.ndarray
    hand_t: np.ndarray

    rotation_log: List[np.ndarray]
    translation_log: List[np.ndarray]

    oracle_target: np.ndarray

    def __init__(
        self, camera: Camera, hand_eye_R: np.ndarray, hand_eye_t: np.ndarray
    ) -> None:
        assert isinstance(camera, Camera)
        assert is_rotation_matrix(hand_eye_R)
        assert is_translation_vector(hand_eye_t)
        self.camera = camera
        self.hand_eye_R = hand_eye_R
        self.hand_eye_t = hand_eye_t
        self.rotation_log = []
        self.translation_log = []

    def set_up_oracle(self, oracle_target):
        self.oracle_target = oracle_target

    def oracle(self, delta):
        positive = np.linalg.norm(self.get_eye_t() + delta - self.oracle_target)
        negative = np.linalg.norm(self.get_eye_t() - delta - self.oracle_target)
        return -delta if positive > negative else delta

    def set_position(self, hand_R: np.ndarray, hand_t: np.ndarray) -> None:
        assert is_rotation_matrix(hand_R)
        assert is_translation_vector(hand_t)
        self.hand_R = hand_R
        self.hand_t = hand_t
        self.rotation_log = []
        self.translation_log = []

    def get_eye_R(self) -> np.ndarray:
        return self.hand_R @ self.hand_eye_R

    def get_eye_t(self) -> np.ndarray:
        return self.hand_eye_R @ self.hand_eye_t + self.hand_t

    def apply_R_and_t(self, R: np.ndarray, t: np.ndarray) -> None:
        assert is_rotation_matrix(R)
        assert is_translation_vector(t)
        self.hand_t += self.hand_R @ t  # self.oracle(self.hand_R @ t)
        self.hand_R = self.hand_R @ R
        # self.rotation_log.append(self.get_eye_R())
        # self.translation_log.append(self.get_eye_t())
        self.rotation_log.append(R)
        self.translation_log.append(t)

    def capture_image(self) -> np.ndarray:
        return self.camera.render_with_pose(self.get_eye_R(), self.get_eye_t())
