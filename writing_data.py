import json, csv

def write_to_json(file_path, data_to_write):   
    with open(file_path,"w+", encoding="utf-8") as file:
            json.dump(data_to_write, file)

def write_to_csv(file_path, data_to_write, header):
    with open(file_path,"w+", encoding="utf-8", newline="") as file:
            csv_writer = csv.DictWriter(file, header)
            csv_writer.writeheader()
            csv_writer.writerows(data_to_write)