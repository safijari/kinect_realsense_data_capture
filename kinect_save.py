import cv2
from PIL.ImageMath import eval as im_eval
import numpy as np
from freenect2 import Device, FrameType, Registration
import freenect2 as freenect
import json

import sys

device = Device()
with device.running():
    rgb_params = device.color_camera_params
    ir_params = device.ir_camera_params
    with open("captures/kinect_calib.json", "w") as fobj:
        json.dump(
            {
                "color": dict(
                    (k, getattr(device.color_camera_params, k))
                    for k in "fx fy cx cy".split()
                ),
                "ir": dict(
                    (k, getattr(device.ir_camera_params, k))
                    for k in "fx fy cx cy k1 k2 k3 p1 p2".split()
                ),
            },
            fobj,
        )

    by_type = {}

    i = 0
    depth_frame = None
    color_frame = None
    for frame_type, frame in device:
        i += 1
        # im = np.asarray(frame.to_image())
        key = str(frame_type)
        by_type[key] = frame
        if key == "FrameType.Depth":
            depth_frame = frame
        if key == "FrameType.Color":
            color_frame = frame

        if i > 30 and len(by_type):
            break

        if i > 100:
            raise Exception("something went wrong")

rgb = color_frame
depth = depth_frame
undistorted, registered, big_depth = device.registration.apply(
    rgb, depth, with_big_depth=True)

# Combine the depth and RGB data together into a single point cloud.
with open('captures/{}_kinect_pc.pcd'.format(sys.argv[1]), 'wb') as fobj:
    device.registration.write_pcd(fobj, undistorted, registered)

with open('captures/{}_kienct_pcbig.pcd'.format(sys.argv[1]), 'wb') as fobj:
   device.registration.write_big_pcd(fobj, big_depth, rgb)

cv2.imwrite("captures/{}_kinect_colorbig.png".format(sys.argv[1]), np.asarray(rgb.to_image())[:, :, ::-1])
import ipdb; ipdb.set_trace()
cv2.imwrite("captures/{}_kinect_color.png".format(sys.argv[1]), np.asarray(registered.to_image()))
cv2.imwrite("captures/{}_kinect_depthbig.exr".format(sys.argv[1]), np.asarray(big_depth.to_image()).astype("float32"))
cv2.imwrite("captures/{}_kinect_depth.exr".format(sys.argv[1]), np.asarray(depth.to_image()).astype("float32"))

# for t, im in by_type.items():
#     fmt = "png"
#     im = np.asarray(im.to_image())
#     if "Depth" in t:
#         fmt = "exr"
#         im = im.astype("float32")
#     cv2.imwrite("captures/{}_kinect_{}.{}".format(sys.argv[1], t, fmt), im)