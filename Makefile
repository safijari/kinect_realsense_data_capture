build:
	sudo docker build -t safijari/kinect_realsense .
run:
	xhost + && sudo docker run --rm -it --privileged --net=host -v /dev/:/dev/ -e DISPLAY -v /tmp/.X11-unix -v `pwd`:/code safijari/kinect_realsense bash