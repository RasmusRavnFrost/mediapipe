"""
Author: Rasmus
Given a list of video files, this script generates vector embeddings similar to those in the YouTube8M dataset
and saves them in the corresponding video-embeddings data folders, by replaceing "/videos/" in its
"/video-embeddings/" path.
"""

import os
import subprocess
import sys
from pathlib import Path
from pprint import pprint
from typing import List

from tqdm import tqdm
from mediapipe.examples.desktop.youtube8m import generate_input_sequence_example

tmp_output_folder = Path("/tmp/yt8m-metadata")


def extract_yt8m_embeddings(video_files: List[Path]):
    """Given a list of video files, this method generates vector embeddings similar to those in the YouTube8M dataset
    and saves them in the corresponding video-embeddings data folders, by replaceing "/videos/" in its
    "/video-embeddings/" path.
    """
    copy_data_to_tmp()
    if extract_metadata(video_files, tmp_output_folder):
        target_files = [path_to_embedding_data(film_path) for film_path in video_files]
        zipped = list([(p, f) for p, f in zip(video_files, target_files) if not f.exists()])
        pbar = tqdm(list(zipped))
        for film_path, target_file in pbar:
            pbar.set_description(film_path.name)
            if not target_file.parent.exists():
                os.makedirs(target_file.parent, exist_ok=True)
            cmd = [
                f"GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/youtube8m/extract_yt8m_features",
                "--calculator_graph_config_file=mediapipe/graphs/youtube8m/feature_extraction.pbtxt",
                f"--input_side_packets=input_sequence_example=\"{_get_metadata_path(path=film_path)}\"",
                f"--output_side_packets=output_sequence_example=\"{target_file}\""
            ]

            result = subprocess.run(" ".join(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if result.returncode != 0:
                print(f"Error in {film_path}")
                print(" ".join(result.args))
                print(result.stdout.decode("utf-8"))
                print("-----------------------------------------")


def copy_data_to_tmp(source_folder="/home/kaspar1/Documents/mediapipe/data/youtube8m/"):
    """This method copyies all data files such as the projection_matrix to a temporary linux folder.
    (The path to the temp folder is pretty hard coded so this was the easiest option)"""
    from distutils.dir_util import copy_tree
    target = "/tmp/mediapipe"
    os.makedirs(target, exist_ok=True)
    return copy_tree(source_folder, target)


def extract_metadata(film_paths: List[Path], output_folder: Path):
    """This method generate metadata files for each film given as input.
    These metadata files are needed for mediapipe to extract metadata files later on.
    The output folder is where all the meta data files will be located"""
    os.makedirs(str(output_folder), exist_ok=True)
    missing_films = list(filter(lambda p: not p.exists(), film_paths))
    if missing_films:
        print(f"Failed to find the following {len(missing_films)} films. aborting")
        pprint(missing_films[:5])
        print("...")
        return False
    else:
        for film_path in tqdm(film_paths, "Extrating metadata..."):
            path_in_datadir = None
            if str(Path(film_path).as_posix()).__contains__("/kaspar-data/"):
                path_in_datadir = str(Path(film_path).as_posix()).split("/kaspar-data/")[-1]
            generate_input_sequence_example.generate(film_path, _get_metadata_path(path=film_path),
                                                     extra_data=dict(path_in_datadir=str(path_in_datadir)))
    return True


def _get_metadata_path(path: Path):
    return tmp_output_folder / path.with_suffix(".pb").name


def path_to_embedding_data(path: Path):
    """Given a film path return a path to the file where the embbeding file should be saved"""
    if str(path.as_posix()).__contains__("/videos/"):
        replaced = Path(str(path.as_posix()).replace("/videos/", "/video-embeddings/"))
        return replaced.parent / replaced.stem / "yt8m-features.pb"
    return tmp_output_folder / ("metadata-" + path.with_suffix(".pb").name)


if __name__ == '__main__':
    r = copy_data_to_tmp()
    film_list_file = Path(sys.argv[1])
    with open(film_list_file) as fp:
        video_files = [Path(s.strip("\n")) for s in fp.readlines() if s.strip("\n")]
    extract_yt8m_embeddings(video_files)