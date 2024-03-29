import PySimpleGUI as sg

import convert

# using the command 'pyinstaller --onefile --specpath ./specs --noconsole ./gui.py' to generate the exe

sg.theme('SystemDefaultForReal')  # Add a touch of color
# All the stuff inside your window.
layout = [
    [sg.Text("Choose a file: "), sg.Input(key="-IN-", change_submits=True), sg.FilesBrowse(key="-IN2-")],
    [sg.Text("Choose output folder: "), sg.Input(key="-FIN-", change_submits=True), sg.FolderBrowse(key="-FIN2-")],
    [sg.Checkbox("Use relative timestamps", default=True, key='check')],
    [sg.Button('Convert')],
    [sg.Text("Waiting for file selection", key="status")]
]

# Create the Window
window = sg.Window('XDF-to-CSV', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    elif event == 'Convert':
        print(values["-IN-"])  # Input filepath
        print(values["-FIN-"])  # Output folder
        print(values["check"])  # Checkbox for timestamps
        window["status"].update("Converting file")
        filenames = values["-IN-"].split(";")
        for filename in filenames:
            return_status = convert.convert_file(filename, values["check"], out_folder=values["-FIN-"])
            print(return_status)
            window["status"].update(return_status[1])

window.close()
