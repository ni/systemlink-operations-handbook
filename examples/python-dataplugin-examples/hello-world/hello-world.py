import os
from pathlib import Path


class Plugin:

    def read_store(self, parameter):
        file_path = os.path.realpath(parameter["file"])

        tdm_tree = {
            "author": "HelloWorkd test",
            "description": "File containing a json dict read by python plugin",
            "groups": [{
                "name": "Group_1",
                "description": "The first group",
                "channels": [{
                    "name": "Index",
                    "description": "",
                    "info": "Going up",
                    "unit_string": "s",
                    "type": "DataTypeChnFloat64",
                    "values": [1, 2, 3]
                }, {
                    "name": "Vals_1",
                    "description": "",
                    "unit_string": "km/h",
                    "type": "DataTypeChnFloat64",
                    "values": [1.1, 2.1, 3.1]
                }, {
                    "name": "Vals_2",
                    "description": "",
                    "unit_string": "km/h",
                    "type": "DataTypeChnFloat64",
                    "values": [1.2, 2.2, 3.2]
                }, {
                    "name": "Str_1",
                    "description": "",
                    "type": "DataTypeChnString",
                    "values": ["abc", "def", "hij"]
                }]
            }, {
                "name": "Group_2",
                "description": "The first group",
                "channels": [{
                    "name": "Index",
                    "description": "",
                    "info": "Going up",
                    "unit_string": "s",
                    "type": "DataTypeChnFloat64",
                    "values": [1, 2, 3, 4]
                }
                ]
            }]
        }

        return {Path(file_path).stem: tdm_tree}


if __name__ == "__main__":
    print("For testing your plugin first, you can run that python file directly from command line")
    p = Plugin()
    parameter = {
        "file": "C:\\Users\\Public\\Documents\\National Instruments\\DIAdem 2020\\Data\\Example.csv"
    }
    print("\n %s" % p.read_store(parameter))
