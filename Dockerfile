FROM ubuntu:18.04

RUN apt update && apt install software-properties-common gnupg -y
RUN apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key
RUN add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo bionic main" -u -y && apt-get install librealsense2* -y

RUN apt install firefox xauth -y

EXPOSE 8887

RUN apt install python3-pip -y

RUN pip3 install opencv-python==4.0.0.21

RUN pip3 install cython

RUN pip3 install pyrealsense2

RUN apt install git build-essential cmake pkg-config -y

RUN apt install libusb-1.0-0-dev libturbojpeg0-dev libglfw3-dev -y

RUN git clone https://github.com/OpenKinect/libfreenect2.git && cd libfreenect2 && cd /libfreenect2 && mkdir build && cd build && cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/freenect2 && make && make install

ENV PKG_CONFIG_PATH /root/freenect2/lib/pkgconfig

RUN pip3 install freenect2

RUN pip3 install pillow

RUN ln -s /root/freenect2/lib/libfreenect2.so.0.2 /usr/lib/libfreenect2.so.0.2

RUN pip3 install numpy imageio