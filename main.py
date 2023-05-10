import pyxdf
import matplotlib.pyplot as plt
import numpy as np

import csv
relative_timestamps = True

filename = "sub-P001_ses-S001_task-Default_run-001_eeg"

data, header = pyxdf.load_xdf(filename+'.xdf')
channels_dict = data[0]['info']['desc'][0]['channels'][0]['channel']
channels = [c['label'][0] for c in channels_dict]
print(channels)

print(data[0]["time_stamps"])

#outdata = []

full_data = data[0]
if relative_timestamps:
    time_stamps = full_data['time_stamps'] - full_data['time_stamps'][0]
    time_stamps = np.reshape(time_stamps, (time_stamps.shape[0],1))
else:
    time_stamps = np.reshape(full_data['time_stamps'], (full_data['time_stamps'].shape[0], 1))
timed_data = full_data['time_series']

outdata = np.concatenate((time_stamps, timed_data), axis=1)

with open(filename+".csv",'w',newline='') as file:
    writer = csv.writer(file)
    out_header = ["timestamp"] + channels
    writer.writerow(out_header)
    writer.writerows(outdata)
    file.flush()
    file.close()

for stream in data:
    y = stream['time_series']

    if isinstance(y, list):
        # list of strings, draw one vertical line for each marker
        for timestamp, marker in zip(stream['time_stamps'], y):
            plt.axvline(x=timestamp)
            #print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
    elif isinstance(y, np.ndarray):
        # numeric data, draw as lines
        plt.plot(stream['time_stamps'], y)
    else:
        raise RuntimeError('Unknown stream format')

plt.show()