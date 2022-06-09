build:
	sudo docker build -t safijari/kinect_realsense .
run:
	sudo docker run --rm -it --privileged --net=host -v /dev/:/dev/ -v `pwd`:/code -v ~/kinect_rs_captures/:/captures/ -w /code --name kinect_rs_container safijari/kinect_realsense bash
