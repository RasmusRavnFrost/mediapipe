# Mediapipe & YouTube8M install guide for ubuntu 18.04
# Copying this script to the terminal should work, but probably a good idea to take in a few step to ensure everyhing
# ran properly and read the comments (you might want to change some things)...
# Asume that command python and pip refers to python v3.6 if thats is the version you want to use
# FIRST: GOTO directory where mediapipe repository will be located. (for instance Home/documents/Kaspar/mediapipe

# MediaPipe uses bazel to run everything, so we first install it.

sudo apt-get update
sudo apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        wget \
        unzip \
        libopencv-core-dev \
        libopencv-highgui-dev \
        libopencv-imgproc-dev \
        libopencv-video-dev \
        libopencv-calib3d-dev \
        libopencv-features2d-dev \
        software-properties-common
sudo apt-get install mesa-common-dev libegl1-mesa-dev libgles2-mesa-dev -y # requirements for gpu with bazel
sudo add-apt-repository -y ppa:openjdk-r/ppa
sudo apt-get update && apt-get install -y openjdk-8-jdk
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*

sudo pip install --upgrade setuptools
sudo pip install future
sudo pip install --upgrade six


curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
sudo apt update
sudo apt install bazel-1.1.0


# You may want to add the following alias at the end of ~/.bashrc
alias bazel=bazel-1.1.0



git clone https://github.com/google/mediapipe.git
cd mediapipe


# Following the guides-and-resources of https://github.com/google/mediapipe/tree/master/mediapipe/examples/desktop/youtube8m
# BUT i changed some directories


mkdir  data && mkdir data/youtube8m/
cd data/youtube8m/
curl -O http://data.yt8m.org/pca_matrix_data/inception3_mean_matrix_data.pb
curl -O http://data.yt8m.org/pca_matrix_data/inception3_projection_matrix_data.pb
curl -O http://data.yt8m.org/pca_matrix_data/vggish_mean_matrix_data.pb
curl -O http://data.yt8m.org/pca_matrix_data/vggish_projection_matrix_data.pb
curl -O http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz
tar -xvf inception-2015-12-05.tgz
rm inception-2015-12-05.tgz

# Before we can run python we need to install packages for vggish
pip install --upgrade pip
pip install tensorflow==1.15
pip install numpy resampy  tf_slim six soundfile

# Go back to mediapipe directory....
cd ../..


# Change one line for compatability reason with tensorflow version (not needed if pulled from https://github.com/RasmusRavnFrost/mediapipe)
#sudo apt-get update -y
#sudo apt-get install gedit nano -y
#sed -i -e 's/from tensorflow.compat.v1.python.tools import freeze_graph/from tensorflow.python.tools import freeze_graph/g' mediapipe/examples/desktop/youtube8m/generate_vggish_frozen_graph.py

mkdir /tmp/mediapipe
python -m mediapipe.examples.desktop.youtube8m.generate_vggish_frozen_graph
cp /tmp/mediapipe/vggish_new.pb data/youtube8m

# Compile bazel builds

# This will take a while and might freeze your pc due to ram limitation (I ran on pc with 16 GB ram). You can probably limit ram usage with some some bazel build settings
# Though after looking i
bazel build -c opt --copt -DMESA_EGL_NO_X11_HEADERS --define no_aws_support=true mediapipe/examples/desktop/youtube8m:extract_yt8m_features
# RUN bazel build -c opt --copt -DMESA_EGL_NO_X11_HEADERS mediapipe/examples/desktop/youtube8m:model_inference


# TEST INSTALLATION
# To test run following command and see if it generates a features.pb file. Replace /mnt/hdd/kaspar-data... with your own paths

python -m mediapipe.examples.desktop.youtube8m.generate_input_sequence_example \
  --path_to_input_video=/mnt/hdd/kaspar-data/videos/test-videos/A-Millennial-Job-Interview.mp4 \
  --clip_end_time_sec=120
 # generate_input_sequence_example targets /tmp/mediapipe so we copy the data there.
mkdir /tmp/mediapipe
cp /home/kaspar1/Documents/mediapipe/data/youtube8m/* /tmp/mediapipe
GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/youtube8m/extract_yt8m_features \
  --calculator_graph_config_file=mediapipe/graphs/youtube8m/feature_extraction.pbtxt \
  --input_side_packets=input_sequence_example=/tmp/mediapipe/metadata.pb  \
  --output_side_packets=output_sequence_example=/tmp/mediapipe/features.pb
