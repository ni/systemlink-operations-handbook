# Python DataPlugins

Create a DataPlugin to load, to register, or to search your own file formats in LabVIEW or DIAdem, or to index and to browse your own file formats with SystemLink DataFinder.

DataPlugins can be created by using C++, VBS, LabVIEW or Python.

## Get Started

Python DataPlugins consist of only one python file that contains all the logic. Almost all language features of the official Python 3.5.9 and its base libraries can be used.

### Plugin class

Start writing your DataPlugin by implementing the
```python 
class Plugin:
```
The class name cannot be changed.

### Store read

Every Python DataPlugins needs to implement a read_store method. This method is called by DIAdem, LabVIEW or SystemLink DataFinder when it attempts to open your data file. The applications pass a set of useful parameters that can be accessed by the parameter array.

<details>
<summary>Example Code</summary>
<p>


```python 
import datetime
import os
from pathlib import Path
def read_store(self, parameter):
   """
      Read data file and return a python dictionary
      that contains groups and channels in a TDM-like structure.
   """

   # String: Contains the absolute path to the data file
   file_path = os.path.realpath(parameter["file"])
   # Boolean: Denotes if data file was accessed by SystemLink DataFinder and the bulk data was not touched. 
   is_datafinder_indexer = parameter["datafinder"]

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
```


</p>
</details>

Use the file parameter to access your file using text, csv or binary readers. The data has to be filled into a python dictionary. It represents the [structure of tdm/tdms files](https://www.ni.com/en-us/support/documentation/supplemental/06/the-ni-tdms-file-format.html) that consist of one root, 0...m groups and 0...n channels:

<img alt="TDM structure with file, groups and channels" src="../img/pydp-tdm_structure.png?raw=true" width="500"><br>

<details>
<summary>Example dictionary</summary>
<p>

```python 
self.tdm_tree = {
   "author": "National Instruments",
   "description": "Example file",
   "groups": [{
         "name": "Example",
         "description": "The first group",
         "time": datetime.datetime(2020, 2, 11, 15, 31, 59, 342380),
         "channels": [{
            "name": "Channel_0",
            "description": "",
            "values": [1.2, 1.3, 1.4],
            "info": "Time in seconds",
            "type": "DataTypeChnFloat64"
         }, {
            "name": "Channel_1",
            "description": "",
            "values": [10, 11, 12],
            "unit_string": "km/h",
            "type": "DataTypeChnFloat64"
         }]
   }]
}

file_path = os.path.realpath(parameter["file"])
return {Path(file_path).stem: self.tdm_tree}
```
</p>
</details>

<details>
<summary>Dictionary Schema</summary>
<p>

```python
import datetime
from schema import And, Schema

Schema({
      Optional('author'): str,
      Optional('description'): str,
      'groups': [{
         'name': str,
         Optional('description'): str,
         Optional('time'): datetime.datetime,
         'channels': [{
            'name': str,
            Optional('description'): str,
            'values': list,
            Optional('unit_string'): str,
            'type': And(str, lambda s: s in (
               'DataTypeChnFloat32',
               'DataTypeChnFloat64',
               'DataTypeChnString',
               'DataTypeChnDate',
               'DataTypeChnUInt8',
               'DataTypeChnInt16',
               'DataTypeChnInt32',
               'DataTypeChnInt64'))
            }]
      }]}, ignore_extra_keys=True)
```

</p>
<p>All further extra keys will show up as custom properties in DIAdem, Labview or SystemLink DataFinder.</p>
</details>

See full example: [csv-read-with-direct-loading](../../examples/python-dataplugin-examples/csv-read-with-direct-loading/Readme)

## Callback Loading
When handling big data sets, it can make sense to not load all data at once. Instead, the DataPlugin should return only the values that are requested by the applications. We skip the costs that are needed to fill the value-arrays inside the `read_store` function - and just leave the array empty:

```python
...
'groups': [{
   ...
   'channels': [{
      ...
      'values': [],
   }]
}]
```

We outsource the functionality to load the bulk data values in a different function within the `Plugin` class. The function has the following definition:

```python 
def read_channel_values(self, grp_index, chn_index, numberToSkip, numberToTake):
   """
      Returns a value array of the correct data type specified in the tdm dictionary
   """
```

<details>
<summary>Example Code</summary>
<p>

```python
def read_channel_values(self, grp_index, chn_index, numberToSkip, numberToTake):
   dataType = self.tdm_tree["groups"][grp_index]["channels"][chn_index]["type"]
   values = []
   for row in self.data:
      value = row[self.channelNames[chn_index]]
      values.append(value)
   return values[numberToSkip:numberToTake+numberToSkip]
```

</p>
</details>

The client applications are calling that function to retrieve channel values (or a subset of values). The DataPlugin needs to implement the function to return the values for a given group and channel index. It also needs to ensure only the correct subset of values is returned for a given `numberToSkip` and `numberToTake`.

Additionally, a callback function to retrieve the channel length must be implemented. In the simple case where all channels have the same length, it can simply return a constant.

```python 
def read_channel_length(self, grp_index, chn_index):
   """
      Returns the channel length as an Integer for a given group and channel index
   """
   return 10
```

See full example: [csv-read-with-callback-loading](../../examples/python-dataplugin-examples/csv-read-with-callback-loading/Readme)

## Error Handling
Python DataPlugins can raise errors in all callback functions. The raised error will be transported to DIAdem, LabVIEW or SystemLink DataFinder.

```python
def read_store(self, parameter):
   ...
   raise Exception("Leave read_store with exception")
```

### Not My File
A special case is "Not My File". This error should be raised when the DataPlugin detects that the file to be opened, is not suited for this DataPlugin. This special error can be raised only in the `read_store` function by returning `None`:

```python
def read_store(self, parameter):
   ...
   if notMyFile:
      return None
```

## Export DataPlugin
Export Python DataPlugins to make them available on other systems. Use DIAdem to export a DataPlugin as a URI file.

<img alt="Exporting DataPlugins in DIAdem" src="../img/pydp-diadem_export.png?raw=true" width="600"><br>

## Known Limitations
### Numpy and Pandas
Unfortunately, Numpy and Pandas are not well supported to run in embedded Python environments and, therefore, cannot be used in DataPlugins.

### Single file DataPlugins
Python DataPlugins can only be written in a single python file. Importing sidecar files is not supported. It will fail when exporting the DataPlugin as a URI.

### datetime.strptime
There is an <a href="https://bugs.python.org/issue27400">open issue</a> in Python for `datetime.strptime` that prevents the function to work properly in embedded Python environments. Therefore, this function should be avoided in DataPlugin source code. Instead, the following function can be added to the code and work around the issue:

```python 
def strptime(self, value, format):
   return datetime.datetime(*(time.strptime(value, "%d.%m.%y %H:%M:%S")[0:6]))
```