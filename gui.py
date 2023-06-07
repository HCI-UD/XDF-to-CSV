import PySimpleGUI as sg

import convert

sg.theme('SystemDefaultForReal')   # Add a touch of color
# All the stuff inside your window.
layout = [
            [sg.Text("Choose a file: "), sg.Input(key="-IN2-",change_submits=True), sg.FileBrowse(key="-IN-")],
            [sg.Checkbox("Use relative timestamps", default=True, key='check')],
            [sg.Button('Convert')],
            [sg.Text("Waiting for file selection", key="status")]
            ]

# Create the Window
window = sg.Window('XDF-to-CSV', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    elif event == 'Convert':
        print(values["-IN2-"])
        print(values["check"])
        window["status"].update("Converting file")
        return_status = convert.convert_file(values["-IN2-"], values["check"])
        print(return_status)
        window["status"].update(return_status[1])


window.close()