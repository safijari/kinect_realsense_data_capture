xhost + && sudo docker run --rm -it --privileged --net=host -v /dev/bus/usb:/dev/bus/usb -e DISPLAY -v /tmp/.X11-unix kinect_realsense bash
