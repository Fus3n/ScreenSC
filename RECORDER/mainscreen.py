import os
import sys
import threading
import time
from datetime import datetime

import cv2 as cv
import numpy as np
import pyautogui as pgi
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from rec import Ui_ScreenSC

# get Screen Res
width, height = pgi.size()
# get time
now = datetime.now()


# Main class
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        self.tic = 0.0
        self.toc = 0.0
        self.n = 0
        self.savepaths = os.path.join(os.path.expandvars("%userprofile%"), "Videos\\")
        self.stop_recc = False
        super(Ui, self).__init__()
        # uic.loadUi('Ui/rec.ui', self)
        self.ui = Ui_ScreenSC()
        self.ui.setupUi(self)
        self.show()
        self.ui.startB.pressed.connect(self.start_func)
        self.ui.StopB.pressed.connect(self.stop_Rec)
        self.ui.StopB.setEnabled(False)
        self.setWindowTitle("ScreenSC")
        self.ui.pathText.setText(self.savepaths)  # path of current folder

    # start Record Thread
    def start_func(self):
        af = threading.Thread(target=self.start_Rec)
        af.start()

    # start recording
    def start_Rec(self):
        self.pathsave = self.ui.pathText.text()
        if self.pathsave == self.savepaths:
            self.dt_string = now.strftime("%d.%m.%Y %H.%M.%S", )
            self.formatname = f"{self.savepaths}{self.dt_string}.mp4"
        else:
            self.formatname = self.pathsave + ".mp4"
        self.ui.startB.setEnabled(False)
        self.ui.StopB.setEnabled(True)
        self.fourcc = cv.VideoWriter_fourcc('F', 'M', 'P', '4')
        self.screensize = (width, height)
        self.out = cv.VideoWriter(
            self.formatname, self.fourcc, 15.0, (self.screensize))
        cl = threading.Thread(target=self.changeLabel)
        cl.start()
        while True:
            # capture frame with pyautogui
            img = pgi.screenshot()
            frame = np.array(img)  # convert screenshot into array
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            self.out.write(frame)  # writing frames in openv
            if self.stop_recc == True:
                cv.destroyAllWindows()
                self.out.release()
                break

    def changeLabel(self):
        while True:
            # Update Recorded seconds
            QtGui.QGuiApplication.processEvents()  # force gui to update
            self.ui.timerText.setText(str(self.n) + " Seconds")
            QtGui.QGuiApplication.processEvents()
            self.n += 1
            time.sleep(1)
            if self.stop_recc == True:
                self.n = 0
                self.stop_recc = False
                break

    # stop recording
    def stop_Rec(self):
        self.stop_recc = True
        self.ui.startB.setEnabled(True)
        self.ui.StopB.setEnabled(False)
        self.ui.timerText.setText(str(self.n) + " Seconds" + "\n Not Recording")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
