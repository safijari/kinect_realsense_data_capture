import pyrealsense2 as rs
import numpy as np
import cv2

import sys

points = rs.points()
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.infrared, 1, 1280, 720, rs.format.y8, 30)
config.enable_stream(rs.stream.infrared, 2, 1280, 720, rs.format.y8, 30)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
profile = pipeline.start(config)

device = profile.get_device()
depth_sensor = device.query_sensors()[0]
depth_sensor.set_option(rs.option.emitter_enabled, 1)

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

cv2.imwrite("/code/captures/{}_rs_emitter_left.jpg".format(sys.argv[1]), nir_lf_image)
cv2.imwrite("/code/captures/{}_rs_emitter_right.ext".format(sys.argv[1]), nir_rg_image.astype("float32"))
cv2.imwrite("/code/captures/{}_rs_emitter_color.jpg".format(sys.argv[1]), col_image)
cv2.imwrite("/code/captures/{}_rs_emitter_depth.exr".format(sys.argv[1]), depth_image.astype("float32"))

points = rs.points()
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.infrared, 1, 1280, 720, rs.format.y8, 30)
config.enable_stream(rs.stream.infrared, 2, 1280, 720, rs.format.y8, 30)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
profile = pipeline.start(config)

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

cv2.imwrite("/code/captures/{}_rs_noemitter_left.jpg".format(sys.argv[1]), nir_lf_image)
cv2.imwrite("/code/captures/{}_rs_noemitter_right.jpg".format(sys.argv[1]), nir_rg_image)
cv2.imwrite("/code/captures/{}_rs_noemitter_color.jpg".format(sys.argv[1]), col_image)
cv2.imwrite("/code/captures/{}_rs_noemitter_depth.png".format(sys.argv[1]), depth_image)