import pyxdf
import matplotlib.pyplot as plt
import numpy as np

import csv
# using the command 'pyinstaller --onefile --specpath ./specs --noconsole ./gui.py' to generate the exe

def convert_file(filepath, relative_timestamps, outfolder=""):
    if (filepath[-3:] != "xdf"):
        return [-1, "Specified file is not XDF"]

    data, header = [0, 0]

    try:
        data, header = pyxdf.load_xdf(filepath)
    except:
        return [-2, "Could not open file"]
    for i in range(len(data)):
        channels_desc = data[i]['info']['desc']
        """
         * Sometimes there doesn't exist a channel_desc, so we need to check, and create new channel names
        """
        if channels_desc is not None and channels_desc[0] is not None:
            channels_dict = channels_desc[0]['channels'][0]['channel']
            channels = [c['label'][0] for c in channels_dict]
        else:
            channels = [("channel_"+str(c)) for c in range(int(data[i]['info']['channel_count'][0]))]

        outdata = []
        full_data = data[i]
        """
         * Convert the data to the proper format, but only if there actually is data in the file
        """
        if full_data['time_stamps'].shape[0] > 0:
            if relative_timestamps:
                time_stamps = full_data['time_stamps'] - full_data['time_stamps'][0]
                time_stamps = np.reshape(time_stamps, (time_stamps.shape[0], 1))
            else:
                time_stamps = np.reshape(full_data['time_stamps'], (full_data['time_stamps'].shape[0], 1))
            timed_data = full_data['time_series']

            outdata = np.concatenate((time_stamps, timed_data), axis=1)

        """
         * Get name of file, without file extension or full path
        """
        path_parts = filepath.split("/")
        filename = path_parts[-1][:-4]

        """
         * Save new file, with the name of the stream
        """
        if outfolder != "":
            outfile = outfolder + "/" + filename
        else:
            outfile = filepath[:-4]

        if data[i]['info']['name'] is not None and data[i]['info']['name'][0] is not None:
            outfile = outfile + "_" + data[i]['info']['name'][0] + '.csv'
        else:
            outfile = outfile + '_' + str(i) + '.csv'

        with open(outfile, 'w', newline='') as file:
            writer = csv.writer(file)
            out_header = ["timestamp"] + channels
            writer.writerow(out_header)
            writer.writerows(outdata)
            file.flush()
            file.close()

    return [0, "File converted successfully"]


"""for stream in data:
    y = stream['time_series']

    if isinstance(y, list):
        # list of strings, draw one vertical line for each marker
        for timestamp, marker in zip(stream['time_stamps'], y):
            plt.axvline(x=timestamp)
    elif isinstance(y, np.ndarray):
        # numeric data, draw as lines
        plt.plot(stream['time_stamps'], y)
    else:
        raise RuntimeError('Unknown stream format')

plt.show()"""
