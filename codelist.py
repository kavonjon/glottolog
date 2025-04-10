import os,re,csv
from collections import defaultdict

rows = []
stats = {
    'both_matching': 0,
    'both_mismatched': [],  # Will store glottocodes of mismatched cases
    'only_link': [],        # Will store glottocodes with only links
    'only_identifier': [],  # Will store glottocodes with only identifiers
    'neither': 0
}

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
                iso_search = re.search(r"iso639-3 = (.*)", text)
                if iso_search:
                    iso = iso_search[1]
                else:
                    iso = ""
                elcat_name_search = re.search(r"\[altnames\].*?\nelcat = \s*(.*?)(?:\n|$)", text, re.DOTALL)
                if elcat_name_search:
                    elcat_name = elcat_name_search[1]
                else:
                    elcat_name = ""
                
                # First check for the link
                elcat_link_search = re.search(r"links = .*?endangeredlanguages\.com/lang/(\d+)", text, re.DOTALL)
                
                # Then check for the identifier
                elcat_id_search = re.search(r"\[identifier\].*?\nendangeredlanguages = \s*(.*?)(?:\n|$)", text, re.DOTALL)
                
                # If we have no identifier but we have a link, use the link's ID
                if not elcat_id_search and elcat_link_search:
                    elcat_id = elcat_link_search[1]
                elif elcat_id_search:
                    elcat_id = elcat_id_search[1]
                else:
                    elcat_id = ""
                
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
                
                # Statistics collection
                has_link = bool(elcat_link_search)
                has_original_id = bool(elcat_id_search)
                
                if has_link and has_original_id:
                    link_number = elcat_link_search[1]
                    original_id = elcat_id_search[1]
                    if link_number == original_id:
                        stats['both_matching'] += 1
                    else:
                        stats['both_mismatched'].append({
                            'glottocode': glottocode,
                            'link_id': link_number,
                            'identifier_id': original_id
                        })
                elif has_link and not has_original_id:
                    stats['only_link'].append(glottocode)
                elif not has_link and has_original_id:
                    stats['only_identifier'].append(glottocode)
                else:
                    stats['neither'] += 1
                
                rows.append({"glottocode" : glottocode, "name" : name, "level" : level, "iso" : iso, "elcat_name" : elcat_name, "elcat_id" : elcat_id, "latitude" : latitude, "longitude" : longitude})
                # print(rows)
                # input("Press 'Enter'")

# Print statistics
print("\nEndangered Languages Reference Statistics:")
print(f"Cases with matching link and identifier: {stats['both_matching']}")
print(f"Cases with neither link nor identifier: {stats['neither']}")
print(f"\nCases with only link (no identifier): {len(stats['only_link'])}")
if stats['only_link']:
    print("Example glottocodes:", stats['only_link'][:3])
    
print(f"\nCases with only identifier (no link): {len(stats['only_identifier'])}")
if stats['only_identifier']:
    print("Example glottocodes:", stats['only_identifier'][:3])

print(f"\nCases with mismatched link and identifier: {len(stats['both_mismatched'])}")
if stats['both_mismatched']:
    print("Mismatched cases:")
    for case in stats['both_mismatched'][:10]:  # Show first 10 mismatches
        print(f"  Glottocode: {case['glottocode']}")
        print(f"  Link ID: {case['link_id']}")
        print(f"  Identifier: {case['identifier_id']}")

# csv header
fieldnames = ['glottocode', 'name', 'level', 'iso', 'elcat_name', 'elcat_id', 'latitude', 'longitude']

with open('codelist.csv', 'w', encoding='UTF8', newline='') as codelist:
    writer = csv.DictWriter(codelist, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
