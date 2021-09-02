import os
import datetime
import pathlib
import time

model_files = [os.path.splitext(l) for l in os.listdir(".")]
model_files = [f + e for f, e in model_files if "model" in f and e == ".dat"]

model_files_by_time = [(datetime.datetime.fromtimestamp(pathlib.Path(f).stat().st_mtime), f) for f in model_files]

after_time = datetime.datetime(2021, 8, 31, 0, 0, 0)

models_after_time = [m for d, m in model_files_by_time if d >= after_time]

dir_path = "temp_" + time.strftime("%Y%m%d-%H%M%S")
os.mkdir(dir_path)

for model in models_after_time:
    os.rename(model, os.path.join(dir_path, model))

print("here")