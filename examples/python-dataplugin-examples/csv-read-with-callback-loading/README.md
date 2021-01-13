# CSV With Callback Loading Example

This example shows a DataPlugin that can read the DIAdem example csv files using the standard Python `csv.DictReader`. The values are accessed by the callback function `read_channel_values`. Instead of loading all values in one step, it is up to the clients to determine when they need which values.
