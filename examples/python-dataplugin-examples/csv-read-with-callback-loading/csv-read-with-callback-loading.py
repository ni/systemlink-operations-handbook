import csv
import datetime
import os
from pathlib import Path


class Plugin:

    channelNames = []
    data = []
    tdm_tree = {}

    def read_store(self, parameter):
        file_path = os.path.realpath(parameter["file"])

        with open(file_path, newline="") as csvfile:
            tab_delimiter = "\t"
            reader = csv.DictReader(csvfile, delimiter=tab_delimiter)
            self.data = list(reader)
            self.channelNames = reader.fieldnames

        ###
        # possible data types:
        # DataTypeChnFloat32, DataTypeChnFloat64, DataTypeChnString, DataTypeChnDate, DataTypeChnUInt8, DataTypeChnInt16, DataTypeChnInt32, DataTypeChnInt64
        ###

        self.tdm_tree = {
            "author": "National Instruments",
            "description": "Example file",
            "groups": [{
                "name": "Example",
                "description": "The first group",
                "time": datetime.datetime(2020, 2, 11, 15, 31, 59, 342380),
                "channels": [{
                    "name": self.channelNames[0],
                    "description": "",
                    "values": [],
                    "info": "Time in seconds",
                    "type": "DataTypeChnFloat64"
                }, {
                    "name": self.channelNames[1],
                    "description": "",
                    "values": [],
                    "unit_string": "km/h",
                    "type": "DataTypeChnFloat64"
                }, {
                    "name": self.channelNames[2],
                    "description": "",
                    "values": [],
                    "type": "DataTypeChnFloat64"
                }, {
                    "name": self.channelNames[3],
                    "description": "",
                    "values": [],
                    "type": "DataTypeChnFloat64"
                }, {
                    "name": self.channelNames[4],
                    "description": "",
                    "values": [],
                    "type": "DataTypeChnFloat64"
                }, {
                    "name": self.channelNames[5],
                    "description": "",
                    "values": [],
                    "type": "DataTypeChnString"
                }]
            }]
        }

        return {Path(file_path).stem: self.tdm_tree}

    def read_channel_length(self, grp_index, chn_index):
        return len(self.data)

    def read_channel_values(self, grp_index, chn_index, numberToSkip, numberToTake):
        dataType = self.tdm_tree["groups"][grp_index]["channels"][chn_index]["type"]
        values = []
        for row in self.data:
            value = row[self.channelNames[chn_index]]
            if value != "":
                if dataType == "DataTypeChnFloat64":
                    value = float(row[self.channelNames[chn_index]])
            else:
                value = None
            values.append(value)
        return values[numberToSkip:numberToTake+numberToSkip]


if __name__ == "__main__":
    print("For testing your plugin first, you can run that python file directly from command line")
    p = Plugin()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parameter = {
        "file": dir_path + "\\Example.csv"
    }
    print("\n %s" % p.read_store(parameter))
    print("\nChannel length: %s" % p.read_channel_length(0, 0))
    print("\nChannel values: %s" % p.read_channel_values(0, 0, 0, 1024))
