import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, 
                             QVBoxLayout, 
                             QGroupBox, QLineEdit, QLabel, QRadioButton, QPushButton)
from PyQt5.QtCore import Qt # for AlignCenter
from PyQt5.QtGui import QFont # for Font

import base64

ceasorHash_path = os.path.abspath("C:/Users/Computer/Desktop/VS Code/project T")
sys.path.append(ceasorHash_path)
import CeasorHash

import importlib.util
print(importlib.util.find_spec("CeasorHash"))

# Generate application Object
app = QApplication(sys.argv)


# Generate Widget
class TestWindow(QWidget):
    __encode_modeList = [ "Base64", "CeasorHash", "Hint" ]
    small_font = QFont('Arial', 8)
    __ceasorHash = CeasorHash.EncryptWithFNV1A()

    def __init__(self):
        super().__init__()
        self.AddUI()
        self.SetUIFeature()
        self.SetUIStyle()

    def AddUI(self):
        radioBox = QGroupBox("[Menu]")
        self.menu0 = QRadioButton(self.__encode_modeList[0])
        self.menu1 = QRadioButton(self.__encode_modeList[1])
        self.menu2 = QRadioButton(self.__encode_modeList[2])

        radioBox_layout = QVBoxLayout()
        radioBox_widgets = [
            self.menu0,
            self.menu1,
            #self.menu2,
        ]
        for radioBox_widget in radioBox_widgets:
            radioBox_layout.addWidget(radioBox_widget)
        radioBox.setLayout(radioBox_layout)


        encodeBox = QGroupBox("[Encode/Decode]")
        self.input_text = QLineEdit("")
        self.input_password = QLineEdit("pw")
        self.encode_btn = QPushButton("🔒Encode")
        self.decode_btn = QPushButton("🔑Decode")
        self.output_text = QLabel("")
        self.output_status_text = QLabel("Idle")

        encodeBox_layout = QVBoxLayout()
        encodeBox_widgets = [
            self.input_text,
            self.input_password,
            self.encode_btn,
            self.decode_btn,
            self.output_text,
            #self.output_status_text
        ]
        for encodeBox_widget in encodeBox_widgets:
            encodeBox_layout.addWidget(encodeBox_widget)
        encodeBox.setLayout(encodeBox_layout)


        self.debug_text = QLabel("")

        mainBox_layout = QVBoxLayout()
        mainBox_widgets = [
            radioBox,
            encodeBox,
            self.debug_text
        ]
        for mainBox_widget in mainBox_widgets:
            mainBox_layout.addWidget(mainBox_widget)

        self.setLayout(mainBox_layout)


    def SetUIFeature(self):
        self.menu0.setChecked(True)
        self.menu0.toggled.connect(self.TogglePasswordInput)
        self.menu1.toggled.connect(self.TogglePasswordInput)
        self.menu2.toggled.connect(self.TogglePasswordInput)
        
        self.input_password.setEnabled(False)

        self.encode_btn.clicked.connect(self.EncodeNavigator)
        self.decode_btn.clicked.connect(self.DecodeNavigator)

        self.output_text.setTextInteractionFlags(Qt.TextSelectableByMouse)


    def SetUIStyle(self):
        self.setWindowTitle("test")
        self.resize(504, 504)

        self.output_text.setFixedHeight(30)
        self.output_text.setAlignment(Qt.AlignCenter)
        self.output_text.setStyleSheet("background: rgb(255, 255, 255)")
        self.debug_text.setFont(self.small_font)



    def EncodeNavigator(self):
        self.ClearDebugText()

        encodedMode = -1
        if(self.menu0.isChecked()): 
            self.Encode_Base64(1)
            encodedMode = 0
        elif(self.menu1.isChecked()):
            self.Encode_CeasorHash(1)
            encodedMode = 1
        elif(self.menu2.isChecked()):
            self.Encode_Hint(1)
            encodedMode = 2
        #self.output_status_text.setText("Encoded: " + self.__encode_modeList[encodedMode])

    def DecodeNavigator(self):
        self.ClearDebugText()

        decodedMode = -1
        if(self.menu0.isChecked()): 
            self.Encode_Base64(0)
            decodedMode = 0
        elif(self.menu1.isChecked()):
            self.Encode_CeasorHash(0)
            decodedMode = 1
        elif(self.menu2.isChecked()):
            self.Encode_Hint(0)
            decodedMode = 2
        #self.output_status_text.setText("Decoded: " + self.__encode_modeList[decodedMode])


    # Encode/Decode methods. mode=1(Encode), mode=0(Decode)
    def Encode_Base64(self, mode: bool):
        raw_data = self.input_text.text()
        if(mode):
            coded_data = base64.b64encode(raw_data.encode("utf-8"))
            coded_data = coded_data.decode("utf-8")
        else:
            coded_data = raw_data.encode("utf-8")
            try:
                coded_data = base64.b64decode(coded_data)
            except base64.binascii.Error as e:
                coded_data = "[Enter Correct base64-encoded string.😠]"
                self.RaiseDebugTextErr(str(e))
            else:
                coded_data = coded_data.decode("utf-8")
                self.RaiseDebugTextErr("Unknown Error in Encode_Bade64()")

        self.output_text.setText(coded_data)

    def Encode_CeasorHash(self, mode: bool):
        raw_data = self.input_text.text()
        coded_data = list(raw_data.encode("utf-8"))
        print(coded_data)
        #self.RaiseDebugTextErr(str(coded_data).encode("utf-8"))
        coded_data = self.__ceasorHash.EncryptUTF8Data(coded_data)
        # seed는 같은데 다른 result 가 나옴. PCG에서.
        print(coded_data)
        #self.output_text.setText(bytes(coded_data).decode("utf-8"))
    def Encode_Hint(self, mode: bool):
        self.output_text.setText(self.input_text.text())

    

    def TogglePasswordInput(self):
        if(self.menu1.isChecked()):
            self.input_password.setEnabled(True)
        else:
            self.input_password.setEnabled(False)



    def RaiseDebugTextErr(self, s: str):
        self.debug_text.setText("Error: " + s)
    def ClearDebugText(self):
        self.debug_text.setText("")


window = TestWindow()
window.show()
sys.exit(app.exec_()) # wait until app Executed

