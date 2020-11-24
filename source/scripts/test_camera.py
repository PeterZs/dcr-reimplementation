from source.algorithm.FengDynamicRelocalizer import FengDynamicRelocalizer
from source.algorithm.CameraRig import CameraRig
from ..camera.CameraBlender import CameraBlender
from ..camera_pose_estimation.FivePointEstimator import FivePointEstimator
from ..utilities import is_rotation_matrix, convert_angles_to_matrix
from scipy.spatial.transform import Rotation
import numpy as np
import cv2

camera = CameraBlender((1200, 1600, 3), "data/blender-scenes/spring.blend")
camera_location = np.array((0, 0, 30), dtype=np.float64)
R = np.eye(3, dtype=np.float64)

# Render the images.
image_original = camera.render_with_pose(R, camera_location)
cv2.imwrite("tmp_original.png", image_original)

tests = [
    (10, 0, 0, "x"),
    (0, 10, 0, "y"),
    (0, 0, 10, "z"),
]

fpe = FivePointEstimator()
for x, y, z, name in tests:
    # Print out the starting location.
    R_test = convert_angles_to_matrix(x, y, z)
    image_test = camera.render_with_pose(R_test, camera_location)
    cv2.imwrite(f"tmp_{name}.png", image_test)

    # Estimate pose.
    R, t = fpe.estimate_pose(image_test, image_original, camera.get_K())

    x, y, z = Rotation.from_matrix(R).as_euler("xyz")
    R = Rotation.from_euler("xyz", (-x, y, z)).as_matrix()

    # Apply the pose estimate.
    R_test_corrected = R @ R_test
    image_test = camera.render_with_pose(R_test_corrected, camera_location)
    cv2.imwrite(f"tmp_{name}_corrected.png", image_test)
