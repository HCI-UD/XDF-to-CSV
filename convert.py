import pyxdf
import numpy as np

import csv


# using the command 'pyinstaller --onefile --specpath ./specs --noconsole ./gui.py' to generate the exe

def convert_file(filepath, relative_timestamps, out_folder=""):
    if filepath[-3:] != "xdf":
        return [-1, "Specified file is not XDF"]

    try:
        data, header = pyxdf.load_xdf(filepath)
    except Exception:
        return [-2, "Could not open file"]

    """
     * This gets the minimum timestamp from each of the streams for the timestamp standardization
     * The first timestamp is used instead of the footer value of 'first_timestamp' because the actual first value uses
     * the proper timestamp correction/offset
    """
    min_timestamp = 0
    if relative_timestamps:
        min_timestamp = float(-1)
        for i in range(len(data)):
            # temp_time = float(data[i]['footer']['info']['first_timestamp'][0])

            if data[i]['time_stamps'].shape[0] > 0:
                temp_time = data[i]['time_stamps'][0]
                if min_timestamp == -1 or temp_time < min_timestamp:
                    min_timestamp = temp_time

    for i in range(len(data)):
        channels_desc = data[i]['info']['desc']
        """
         * Sometimes there doesn't exist a channel_desc, so we need to check, and create new channel names
        """
        if channels_desc is not None and channels_desc[0] is not None:
            channels_dict = channels_desc[0]['channels'][0]['channel']
            channels = [c['label'][0] for c in channels_dict]
        else:
            channels = [("channel_" + str(c)) for c in range(int(data[i]['info']['channel_count'][0]))]

        out_data = []
        full_data = data[i]
        """
         * Convert the data to the proper format, but only if there actually is data in the file
        """
        if full_data['time_stamps'].shape[0] > 0:
            if relative_timestamps:
                time_stamps = full_data['time_stamps'] - min_timestamp
                time_stamps = np.reshape(time_stamps, (time_stamps.shape[0], 1))
            else:
                time_stamps = np.reshape(full_data['time_stamps'], (full_data['time_stamps'].shape[0], 1))
            timed_data = full_data['time_series']

            out_data = np.concatenate((time_stamps, timed_data), axis=1)

        """
         * Get name of file, without file extension or full path
        """
        path_parts = filepath.split("/")
        filename = path_parts[-1][:-4]

        """
         * Save new file, with the name of the stream
        """
        if out_folder != "":
            outfile = out_folder + "/" + filename
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
            writer.writerows(out_data)
            file.flush()
            file.close()

    return [0, "File converted successfully"]
