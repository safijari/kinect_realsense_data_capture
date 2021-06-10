import cv2
from PIL.ImageMath import eval as im_eval
import numpy as np
from freenect2 import Device, FrameType
import json

import sys

device = Device()
with device.running():
    with open("output_calib.json", "w") as fobj:
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
    for frame_type, frame in device:
        i += 1
        im = np.asarray(frame.to_image())
        by_type[str(frame_type)] = im

        if i > 30 and len(by_type):
            break

        if i > 100:
            raise Exception("something went wrong")

for t, im in by_type.items():
    fmt = "png"
    if "Depth" in t:
        fmt = "exr"
        im = im.astype("float32")
    cv2.imwrite("captures/{}_kinect_{}.{}".format(sys.argv[1], t, fmt), im)