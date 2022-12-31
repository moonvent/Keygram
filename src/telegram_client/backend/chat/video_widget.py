import os
import subprocess
import math


def generate_new_path(path: str, speed: float) -> str:
    return os.path.sep + path[:path.rfind('.')] + f'_{speed}' + path[path.rfind('.'):]


def fastify_video(path: str, speed: float):
    
    new_file_path = generate_new_path(path=path, speed=speed)

    reverse_speed = round(1/speed, 2)

    filepath_for_new_file = os.path.abspath('.') +  new_file_path

    os.system(f'ffmpeg -i {path} -filter_complex "[0:v]setpts={reverse_speed}*PTS[v];[0:a]atempo={speed}[a]" -map "[v]" -map "[a]" {filepath_for_new_file}')
    
def get_length(path: str) -> float:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", path],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
    return math.ceil(float(result.stdout))

