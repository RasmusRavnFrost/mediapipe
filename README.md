# About 
This repo is a fork of https://github.com/RasmusRavnFrost/mediapipe-youtube8m-fork with the aim of running 
youtube8m feature extraction easier.  
It fixes a few bugs and problems encountered and contains batch script for generating embeddings 
for multiple videos.

### Installation
Follow the commands and instructions of ```mediapipe+youtube8m-ubuntu-install-guide.sh``` located in 
the root of this repo

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

 