# About 
This repo is a fork of https://github.com/RasmusRavnFrost/mediapipe-youtube8m-fork with the aim of running 
youtube8m feature extraction easier.  
It fixes a few bugs and problems encountered and contains batch script for generating embeddings 
for multiple videos.
I haven't fully figured out how to load that generated vectors properly yep, but I believe there is 
come code that we can steal from https://github.com/ceshine/yt8m-2019/, which runs pytorch models
on the excat type of data.

### Installation
Follow the commands and instructions of ```mediapipe+youtube8m-ubuntu-install-guide.sh``` located in 
the root of this repo.
(If you're considering to use docker, I tried that, but it was rather messy since Bazel takes 
so long to compile, and some of the paths are hardcoded, and then you resk losing all your work 
every time your docker container restarts, at least it needs to compile bazel again. 
So I found, at least on linux, it was easier to install directly)

### Genertate file with films using bash command
Go to folder containing films
```ls -d $PWD/* > ~/Documents/mediapipe/data/longley-films.txt ```
replace ~/Documents/mediapipe/data/longley-films.txt with full path to output file 

### Run
The scripts folder contains bash scripts to extract feature vectors 

```
python scripts/extract-metadata.py   /data/herzog-films.txt
```
Replace "/data/herzog-films.txt" with path to film list 

 