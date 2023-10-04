# XDF-to-CSV
This is a simple program for converting an XDF file, often used with programs like Lab-Streaming-Layer, to a CSV file.

## Executable
Included in the [Releases](https://github.com/HCI-UD/XDF-to-CSV/releases) tab and *dist* folder in the project is an exe
file that you can download and run.

## Application Use
When run through the executable or through the project itself, a window will show up, allowing you to select multiple 
XDF files.  You can also specify an output directory, though if left blank it will default to the same directory as the 
input files  When selected, you can click the *Convert* button to start converting the files.  At the moment, the output
CSV files have the same name as the XDF files and are put in the same folder.

Additionally, the *Use relative timestamps* checkbox allows you to standardize the timestamps for the files with the 
first timestamp, so they are in a more reasonable range.

## Planned Changes
Currently the timestamps are standardized for each strean, but in the future, this will be changed to standardize across 
all streams in each file.