import json
import os
import sys

def renew():
  count = 1
  save = {
      "new_edits": False,
      "docs": []
  }
  return count, save

def save(current_save_folder, file_count, save):
  out_file = open(os.path.join(current_save_folder, str(file_count).zfill(3) + ".json"), "w")
  json.dump(save, out_file)
  out_file.close()

if __name__ == "__main__":
  PATH = sys.argv[1]
  json_files = [file for file in os.listdir(PATH) if file.endswith("json")]
  save_folder = os.path.join(PATH,"couch-data-split")
  os.mkdir(save_folder)
  for file in json_files:
    print(f"processing: {file}")
    file_path = os.path.join(PATH, file)
    current_save_folder = os.path.join(save_folder, file.split(".")[0])
    os.mkdir(current_save_folder)
    with open(file_path) as f:
      line = f.readline()
      count, save_dict = renew()
      file_count = 1
      while line:
        if count > 10000:
            save(current_save_folder, file_count, save_dict)
            file_count += 1
            count, save_dict = renew()
        line = line.rstrip().rstrip(",")
        try:
            data = json.loads(line)
            save_dict["docs"].append(data)
            print(f"file:{str(file_count).zfill(3)}, count:{count} ", end="\r")
            count += 1
        except:
            pass
        line = f.readline()
      save(current_save_folder, file_count, save_dict)