import pandas as pd
import numpy as np
import os
import sys

if __name__ == "__main__":
    folder = sys.argv[1]
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith("csv"):
                os.rename(os.path.join(root, file), os.path.join(root, "all.csv"))
            if file.endswith("json"):
                os.rename(os.path.join(root, file), os.path.join(root, "meta.json"))

