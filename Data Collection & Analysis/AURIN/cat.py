import pandas as pd
import numpy as np
import os
import sys

if __name__ == "__main__":
    folder = sys.argv[1]
    for root, dirs, files in os.walk(folder):
        for file in files:
            os.rename(os.path.join(root, file), os.path.join(folder, file))
    dir_list = [file for file in os.listdir(folder) if os.path.isdir(os.path.join(folder, file))]
    for each_dir in dir_list:
        os.rmdir(os.path.join(folder, each_dir))
    csv_list = [file for file in os.listdir(folder) if file.endswith("csv") ]
    df_list = [pd.read_csv(os.path.join(folder, file)) for file in csv_list]
    df = pd.concat(df_list)
    df.index = np.arange(len(df.index)) + 1
    df.to_csv(os.path.join(folder, "all.csv"), index=False)
    for file in csv_list:
        os.remove(os.path.join(folder, file))
    json_list = [file for file in os.listdir(folder) if file.endswith("json") ]
    count = 1
    for json in json_list:
        if count == 1:
            os.rename(os.path.join(folder, json), os.path.join(folder, "meta.json"))
        else:
            os.remove(os.path.join(folder, json))
        count += 1
