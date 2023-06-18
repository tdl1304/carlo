from pathlib import Path
import subprocess
from typing import List, Optional
import sys
from glob import glob


def side_by_side(video_paths: List[Path], output_path: Optional[Path]):
    output_path = output_path or video_paths[0].parent / "custom_side_by_side.mp4"
    cmd = f"ffmpeg -n {' '.join([f'-i {video_path}' for video_path in video_paths])} -filter_complex hstack=inputs={len(video_paths)} {output_path}"
    print(cmd)
    subprocess.run(cmd, shell=True, check=True)

if __name__ == "__main__":
    # The input arg is a Path to a folder containing videos.
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: python side_by_side.py <video_paths>")
        sys.exit(1)
    
    video_paths = [Path(video_path) for video_path in args]
    side_by_side(video_paths=video_paths, output_path=None)