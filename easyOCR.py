import easyocr
import os
import pyautogui
import PySimpleGUI as sg
import time
import keyboard

def doOCR(minX=0, minY=0, maxX=0, maxY=0):
    # print max screen
    # print(pyautogui.size())
    if maxX == 0 and maxY == 0:
        minX, minY = 0, 0
        maxX, maxY = pyautogui.size()
    getSS =  pyautogui.screenshot(region=(minX, minY, maxX, maxY))
    getSS.save('MRVlens.PNG')
    path = os.getcwd()
    modelPath = path + '\\model'
    reader = easyocr.Reader(['ch_tra', 'en'], gpu=False, download_enabled=False, model_storage_directory=modelPath)
    result = reader.readtext('MRVlens.PNG')
    final = []
    for i in result:
        print(i[1])
        final.append(i[1])
    
    # delete saved image file.
    if os.path.exists("MRVlens.PNG"):
        os.remove("MRVlens.PNG")
    return final

def pinPoint():
    minX, minY, maxX, maxY = 0, 0, 0, 0
    while True:
        if keyboard.is_pressed('shift'):
            minX, minY = pyautogui.position()
            break
    time.sleep(1)
    while True:
        if keyboard.is_pressed('shift'):
            maxX, maxY = pyautogui.position()
            break
    return minX, minY, maxX, maxY

def main():
    sg.theme('DarkTeal9')
    layout = [
        [sg.Text('Click Start to Start OCR\nPress SHIFT to Pin Point Left Top\nMove to Right Bottom and Press SHIFT again')],
        [sg.Button('Start', key='-start-'), sg.Button('Full Screen', key='-full-'), sg.FileBrowse(disabled=True, key='-file-', file_types=(("*.jpg","*.jpeg", ".png"),))],
        [sg.Input(size=(50, 10), key='-output-')],
    ]
    window = sg.Window('OCR', layout, size=(300, 100), element_justification='center')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-start-':
            minX, minY, maxX, maxY = pinPoint()
            # doOCR(minX, minY, maxX, maxY)
            window['-output-'].update(doOCR(minX, minY, maxX, maxY))
        if event == '-full-':
            window['-output-'].update(doOCR())
    window.close()

if __name__ == '__main__':
    main()