import pyrealsense2 as rs
import numpy as np
import cv2
import imageio

import sys

points = rs.points()
pipeline = rs.pipeline()
config = rs.config()

if len(sys.argv) > 2:
  # If a serial number is provided, select the correct realsense device
  config.enable_device(sys.argv[2])
config.enable_stream(rs.stream.infrared, 1, 1280, 720, rs.format.y8, 30)
config.enable_stream(rs.stream.infrared, 2, 1280, 720, rs.format.y8, 30)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
profile = pipeline.start(config)

device = profile.get_device()
depth_sensor = device.query_sensors()[0]
depth_sensor.set_option(rs.option.emitter_enabled, 1)


def get_extrinsics(src, dst):
    extrinsics = src.get_extrinsics_to(dst)
    R = np.reshape(extrinsics.rotation, [3,3]).T
    T = np.array(extrinsics.translation)
    return (R, T)

def camera_matrix(inT):
    R, T = inT
    return np.vstack((R, T))

"""
Returns the fisheye distortion from librealsense intrinsics
"""
def fisheye_distortion(intrinsics):
    return np.array(intrinsics.coeffs[:4])

try:
    for i in range(10):
        frames = pipeline.wait_for_frames()
        nir_lf_frame = frames.get_infrared_frame(1)
        nir_rg_frame = frames.get_infrared_frame(2)
        col_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        print(col_frame)
        if not nir_lf_frame or not nir_rg_frame:
            continue
        nir_lf_image = np.asanyarray(nir_lf_frame.get_data())
        nir_rg_image = np.asanyarray(nir_rg_frame.get_data())
        col_image = np.asanyarray(col_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        # horizontal stack
        image=np.hstack((nir_lf_image,nir_rg_image))
finally:
    pipeline.stop()

imageio.imwrite("/code/captures/{}_rs_emitter_left.jpg".format(sys.argv[1]), nir_lf_image)
imageio.imwrite("/code/captures/{}_rs_emitter_right.jpg".format(sys.argv[1]), nir_rg_image)
imageio.imwrite("/code/captures/{}_rs_emitter_color.jpg".format(sys.argv[1]), col_image)
cv2.imwrite("/code/captures/{}_rs_emitter_depth.exr".format(sys.argv[1]), depth_image.astype("float32"))

points = rs.points()
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.infrared, 1, 1280, 720, rs.format.y8, 30)
config.enable_stream(rs.stream.infrared, 2, 1280, 720, rs.format.y8, 30)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
profile = pipeline.start(config)

i1_stream = profile.get_stream(rs.stream.infrared, 1)
i2_stream = profile.get_stream(rs.stream.infrared, 2)
color_stream = profile.get_stream(rs.stream.color)
depth_stream = profile.get_stream(rs.stream.depth)

out = ""
out += str(i1_stream.as_video_stream_profile().get_intrinsics()) + "\n"
out += str(i2_stream.as_video_stream_profile().get_intrinsics()) + "\n"
out += str(color_stream.as_video_stream_profile().get_intrinsics()) + "\n"
out += str(depth_stream.as_video_stream_profile().get_intrinsics()) + "\n"
out += str(camera_matrix(get_extrinsics(i1_stream, color_stream)).tolist()) + "\n"
out += str(camera_matrix(get_extrinsics(i2_stream, color_stream)).tolist()) + "\n"
out += str(camera_matrix(get_extrinsics(color_stream, color_stream)).tolist()) + "\n"
out += str(camera_matrix(get_extrinsics(depth_stream, color_stream)).tolist()) + "\n"


device = profile.get_device()
depth_sensor = device.query_sensors()[0]
depth_sensor.set_option(rs.option.emitter_enabled, 0)


try:
    for i in range(10):
        frames = pipeline.wait_for_frames()
        nir_lf_frame = frames.get_infrared_frame(1)
        nir_rg_frame = frames.get_infrared_frame(2)
        col_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        print(col_frame)
        if not nir_lf_frame or not nir_rg_frame:
            continue
        nir_lf_image = np.asanyarray(nir_lf_frame.get_data())
        nir_rg_image = np.asanyarray(nir_rg_frame.get_data())
        col_image = np.asanyarray(col_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        # horizontal stack
        image=np.hstack((nir_lf_image,nir_rg_image))
finally:
    pipeline.stop()

imageio.imwrite("/code/captures/{}_rs_noemitter_left.jpg".format(sys.argv[1]), nir_lf_image)
imageio.imwrite("/code/captures/{}_rs_noemitter_right.jpg".format(sys.argv[1]), nir_rg_image)
imageio.imwrite("/code/captures/{}_rs_noemitter_color.jpg".format(sys.argv[1]), col_image)
cv2.imwrite("/code/captures/{}_rs_noemitter_depth.exr".format(sys.argv[1]), depth_image.astype("float32"))

with open("/code/captures/realsense_params.json", "w") as f:
    f.write(out)
