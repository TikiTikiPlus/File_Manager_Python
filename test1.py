import PySimpleGUI as sg
import os

def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        sg.popup(f'Successfully renamed: {old_name} to {new_name}')
    except Exception as e:
        sg.popup_error(f'Error renaming {old_name}: {e}')

def main():
    layout = [
        [sg.Text('Select a file to rename:')],
        [sg.InputText(key='old_name', disabled=True), sg.FileBrowse(key='file_browse')],
        [sg.Text('Enter new name:')],
        [sg.InputText(key='new_name'), sg.Button('Rename', key='rename_button')],
    ]

    window = sg.Window('File Renaming Tool', layout, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'file_browse':
            selected_file = values['file_browse']
            window['old_name'].update(value=selected_file)
            window['new_name'].update(value=os.path.basename(selected_file))

        elif event == 'rename_button':
            old_name = values['old_name']
            new_name = values['new_name']
            if not old_name or not new_name:
                sg.popup_error('Please select a file and enter a new name.')
            else:
                rename_file(old_name, new_name)
                window['old_name'].update(value='')
                window['new_name'].update(value='')
                window['file_browse'].update(value='')

    window.close()

if __name__ == "__main__":
    main()
