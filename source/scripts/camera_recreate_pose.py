from source.algorithm.FengDynamicRelocalizer import FengDynamicRelocalizer
from source.algorithm.CameraRig import CameraRig
from ..camera.CameraBlender import CameraBlender
from ..camera_pose_estimation.FivePointEstimator import FivePointEstimator
from ..plotting.plot_convergence import plot_t_convergence, plot_r_convergence
from ..utilities import make_rotation_matrix, convert_angles_to_matrix
from ..logging.PoseLogger import PoseLogger
import numpy as np
import cv2

# Create the camera.
camera = CameraBlender((1000, 1160, 3), "data/blender-scenes/spring.blend")

camera_location_a = np.array((10, -7, 8), dtype=np.float64)
camera_location_b = np.array((9, -8, 9), dtype=np.float64)
camera_target_a = np.array((0, 0, 0), dtype=np.float64)
camera_target_b = np.array((0, 0, 0), dtype=np.float64)

R_a = make_rotation_matrix(camera_location_a, camera_target_a)
R_b = make_rotation_matrix(camera_location_b, camera_target_b)

# Render the images.
image_a = camera.render_with_pose(R_a, camera_location_a)
image_b = camera.render_with_pose(R_b, camera_location_b)
cv2.imwrite("tmp_target_pose.png", image_a)
cv2.imwrite("tmp_initial_pose.png", image_b)

# Run Feng's algorithm.
fpe = FivePointEstimator()
rig = CameraRig(
    camera,
    convert_angles_to_matrix(3, 3, 3),
    np.array([0.2, 0.1, 0.4], dtype=np.float64),
)
rig.set_up_oracle(camera_location_a)
pose_logger = PoseLogger()
algo = FengDynamicRelocalizer(rig, fpe, 2.0, 0.05, pose_logger)

s_log, recreation = algo.recreate_image(image_a, R_b, camera_location_b)
cv2.imwrite("tmp_recreated_pose.png", recreation)
pose_logger.save("tmp_intermediate_poses.npz", R_a, camera_location_a)
plot_t_convergence(camera_location_a, rig.translation_log, s_log)
plot_r_convergence(R_a, rig.rotation_log)
print("Done!")
