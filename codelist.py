import os,re,csv

rows = []
# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("languoids/tree"):
    path = root.split(os.sep)
    glottocode = os.path.basename(root)
    for file in files:
        if file == "md.ini":
            with open(root + "/" + file, 'r') as f:
                text = f.read()
                name_search = re.search(r"name = (.*)", text)
                if name_search:
                    name = name_search[1]
                else:
                    name = ""
                level_search = re.search(r"level = (.*)", text)
                if level_search:
                    level = level_search[1]
                else:
                    level = ""
                latitude_search = re.search(r"latitude = (.*)", text)
                if latitude_search:
                    latitude = latitude_search[1]
                else:
                    latitude = ""
                longitude_search = re.search(r"longitude = (.*)", text)
                if longitude_search:
                    longitude = longitude_search[1]
                else:
                    longitude = ""
                rows.append({"glottocode" : glottocode, "name" : name, "level" : level, "latitude" : latitude, "longitude" : longitude})
                # print(rows)
                # input("Press 'Enter'")

# csv header
fieldnames = ['glottocode', 'name', 'level', 'latitude', 'longitude']

with open('codelist.csv', 'w', encoding='UTF8', newline='') as codelist:
    writer = csv.DictWriter(codelist, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
