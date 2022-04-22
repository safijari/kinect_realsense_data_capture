build:
	sudo docker build -t safijari/kinect_realsense .
run:
	sudo docker run --rm -it --privileged --net=host -v /dev/:/dev/ -v `pwd`:/code safijari/kinect_realsense bash
