import json
import os
import yaml
from distutils.dir_util import copy_tree
import pathlib

parent_dir = "..\\..\\bot-api\\python\\tankroyale"
new_dir = "schemas"
path = os.path.join(parent_dir, new_dir)
pathlib.Path(path).mkdir(exist_ok=True)
print('Created directory on path:' + path)

copy_tree('..\\schemas\\', path)
for filename in os.listdir(path):
    print(filename)
    with open(os.path.join(path, filename)) as f:
        filename = filename.split(".")[0]
        try:
            doc = yaml.safe_load(f)
            doc['name'] = filename
            try:
                for key, value in list(doc['properties'].items()):
                    for key2, value2 in list(doc['properties'][key].items()):
                        if key2 == '$ref':
                            del doc['properties'][key][key2]
                            doc['properties'][key]['type'] = 'string'
            except KeyError:
                pass

            print({filename : doc})

        except yaml.parser.ParserError:
            print("Oh No! ...Anyway")
            pass
        with open(os.path.join(path, filename)+".json", 'w') as j:
            json.dump(doc, j)


# for jsonfile in os.listdir(path):
#     if ".json" in jsonfile:
#         print(jsonfile)
#         os.system("jsonschema2popo2 -o " + path + "\\" + jsonfile.split(".")[0] + ".py " + path + "\\" + jsonfile)




