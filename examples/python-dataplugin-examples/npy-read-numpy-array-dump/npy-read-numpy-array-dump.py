import os
import re
from array import array
from pathlib import Path


class Plugin:
    def read_store(self, parameter):
        file_path = os.path.realpath(parameter["file"])
        values = self.load_npy_file(file_path)

        tdm_tree = {
            "author": "NI",
            "description": "This file contains a NumPy array",
            "groups": [
                {
                    "name": "Group_1",
                    "description": "The first group",
                    "channels": [
                        {
                            "name": "Index",
                            "description": "",
                            "type": "DataTypeChnFloat64",
                            "values": values,
                        }
                    ],
                }
            ],
        }

        return {Path(file_path).stem: tdm_tree}

    def load_npy_file(self, file_path):
        f = open(file_path, errors="ignore")
        header = self.__read_npy_header(f)
        f.close()

        f = open(file_path, "rb")
        next(f)  # skip first line

        a = array(self.__map_datatype(header["datatype"]))
        a.frombytes(f.read())
        f.close()

        return a.tolist()

    def __map_datatype(self, npy_data_type):
        if npy_data_type == "i4":
            return "i"
        if npy_data_type == "f8":
            return "d"

    def __read_npy_header(self, file):
        datafile = file.readlines()

        datatype = None
        fortran_order = False
        little_endian = False
        shape = None
        word_size = None

        line = datafile[0]

        loc_1 = line.find("fortran_order")
        loc_2 = line.find("descr")
        loc_3 = line.find("shape")

        # fmt off
        if loc_1 > -1:
            fortran_order = True if line[loc_1 + 16 : loc_1 + 20] == "True" else False
        # fmt on

        # descr
        if loc_2 > -1:
            endian_char = line[loc_2 + 9]
            little_endian = (
                True if (endian_char == "<" or endian_char == "|") else False
            )
            sub_str = line[loc_2 + 11 :]
            loc_tmp = sub_str.find("'")
            word_size = int(line[loc_2 + 11 : loc_2 + 11 + loc_tmp])
            datatype = line[loc_2 + 10 : loc_2 + 11 + loc_tmp]

        # shape
        if loc_3 > -1:
            start_loc = line.find("(")
            end_loc = line.find(")")

            # finding shape value
            shape = []
            sub_str_1 = line[start_loc + 1 : end_loc]
            pattern = re.compile(r"[0-9][0-9]*")
            for number in re.findall(pattern, sub_str_1):
                shape.append(int(number))

        header = {
            "datatype": datatype,
            "fortran_order": fortran_order,
            "little_endian": little_endian,
            "shape": shape,
            "word_size": word_size,
        }

        return header


if __name__ == "__main__":
    print(
        "For testing your plugin first, you can run that python file directly from command line"
    )
    p = Plugin()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parameter = {"file": dir_path + "\\Example.npy"}

    print("\n %s" % p.read_store(parameter))
