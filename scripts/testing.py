"""This is a small script to inspect the generated feature vector files."""

import tensorflow as tf

from protobuf_to_dict import protobuf_to_dict

# with open('/hdd/kaspar-data/tmp/mediapipe/features.pb', 'rb') as fp:
# with open('/home/kaspar1/Documents/mediapipe/testdata/metadataA-Millennial-Job-Interview.pb', 'rb') as fp:
with open('/mnt/hdd/kaspar-data/video-embeddings/herzog-movies/Aguirre.the.Wrath.of.God.1972.GERMAN.720p.BluRay.H264.AAC-VXT/yt8m-features.pb', 'rb') as fp:
    t = tf.train.SequenceExample.FromString(fp.read())
d = protobuf_to_dict(t)
l = d["context"]['feature']['clip/start/timestamp']['int64_list']['value']
print(len(l))
print(l[-10:])
# print(list(d["context"]['feature']['clip/start/timestamp']['int64_list']['value'].keys()))
# print(d.keys())
