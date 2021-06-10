build:
	sudo docker build -t kinect_realsense .
run:
	xhost + && sudo docker run --rm -it --privileged --net=host -v /dev/:/dev/ -e DISPLAY -v /tmp/.X11-unix -v `pwd`:/code kinect_realsense bash