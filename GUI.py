import sys
import random

from PyQt5.QtWidgets import (QApplication, QWidget, 
                             QVBoxLayout, QHBoxLayout, QFrame,
                             QGroupBox, QLineEdit, QLabel, QRadioButton, QPushButton,
                             QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer, QRect # Qt for AlignCenter
from PyQt5.QtGui import QFont, QPainter, QColor, QPixmap, QFontMetrics
# QTimer, QRect, QPainter, QPixmap, QColor, QFontMetrics for Glitch Animation  
import base64



# Colors
transparent = "#00000000"

black="#01000A"
eerie_black="#222222"

vermilion="#FF3C38"
brilliant_rose="#FF4FAD"
electric_blue="#00F0FF"
amethyst="#9B5DE5"
green_yellow="#B9FF66"

lilac="#BA9AC3"
eminence="#622279" # 좀 더 어둡게?
federal_blue="#0D0643"
true_blue="#4D70A4"
dark_purple="#080120"

sky_blue = "#64C4E8"
celeste = "#C8FDFD"
heliotrope = "#D375EF"
lavender_blush = "#FEF2FE"

main_font = "sans-serif"


# Custom Title Bar
class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.AddUI()
        self.SetUIStyle()
        self.SetUIFeature()

    def AddUI(self):
        self.titleBox_layout = QHBoxLayout()
        self.title = GlitchLabel(110, 20, QFont(main_font, 10, QFont.Bold),"Glitch Encoder", 1)
        self.titleBox_layout.addWidget(self.title)
        self.titleBox_layout.addStretch()

        self.titleMinBtn = QPushButton("-")
        self.titleMaxBtn = QPushButton("⛶")
        self.titleCloseBtn = QPushButton("✕")
        
        self.titleBox_widgets = [
            self.titleMinBtn,
            self.titleMaxBtn,
            self.titleCloseBtn
        ]
        for titleBox_widget in self.titleBox_widgets:
            self.titleBox_layout.addWidget(titleBox_widget)
        self.setLayout(self.titleBox_layout)

    def SetUIStyle(self):
        self.setFixedHeight(30)
        self.titleBox_layout.setSpacing(25)
        #self.title.setFixedSize(200, 30)
        self.title.setContentsMargins(5, 0, 0, 0)
        
        self.titleMinBtn.setObjectName("titleMinBtn")
        self.titleMaxBtn.setObjectName("titleMaxBtn")
        self.titleCloseBtn.setObjectName("titleCloseBtn")
        for titleBox_btn in self.titleBox_widgets:
            titleBox_btn.setFixedSize(20, 20)
            titleBox_btn.setStyleSheet(f"""
                            QPushButton{{
                                border: none;
                                background-color: {transparent};
                                color: white;
                                font-weight: bold;
                                font-size: 18px;
                            }}
                            QPushButton#titleMinBtn:hover{{ color: {green_yellow}; }}
                            QPushButton#titleMaxBtn:hover{{ color: {green_yellow}; }}
                            QPushButton#titleCloseBtn:hover{{ color: {vermilion}; }}
                            """)

        
    def SetUIFeature(self):
        self.titleMinBtn.clicked.connect(self.window().showMinimized)
        self.titleMaxBtn.clicked.connect(self.ToggleMaxScreen)
        self.titleCloseBtn.clicked.connect(self.window().close)

    def ToggleMaxScreen(self):
        window = self.window()
        if(window.isMaximized()):
            window.showNormal()
        else:
            window.showMaximized()

    def mouseDoubleClickEvent(self, event):
        self.ToggleMaxScreen()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._mouse_pos = event.globalPos()
            self._window_pos = self.window().pos()
            event.accept()

    def mouseMoveEvent(self, event): # move screen with titleBar clicked
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self._mouse_pos
            self.window().move(self._window_pos + delta)
            event.accept()


class GlowGroupBox(QGroupBox):
    def __init__(self, text):
        super().__init__(text)

        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(80)
        glow.setOffset(-2, -2)
        shadowColor = QColor(electric_blue)
        shadowColor.setAlpha(200)
        glow.setColor(shadowColor)
        self.setGraphicsEffect(glow)

        frame = QFrame()
        frameGlow = QGraphicsDropShadowEffect()
        frameGlow.setBlurRadius(0) # No Blur, Border
        frameGlow.setOffset(10, 10)
        shadowColor = QColor(brilliant_rose)
        frameGlow.setColor(shadowColor)
        frame.setGraphicsEffect(frameGlow)
        



class GlitchLabel(QLabel):
    def __init__(self, width, height, font, text, glitch_dist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        self.setMinimumSize(width, height)
        self.setFont(font)
        self.ChangeText(text)
        self.glitch_dist = glitch_dist

    def ChangeText(self, text):
        self.text = text

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.base_x = self.width()//2 - QFontMetrics(self.font()).width(self.text)//2;
        self.base_y = self.height()//2 + self.font().pointSize()//2
        
        # 1. Text, color jitter effect on pixmap
        pixmap = QPixmap(self.width(), self.height())
        pixmap.fill(Qt.transparent)
        inner_painter = QPainter(pixmap)
        inner_painter.setFont(self.font())

        self.glitch_colors = [QColor("red"), QColor("cyan")]
        self.glitch_offsets = [(-1, 1), (2, 0)]

        for color, (dx, dy) in zip(self.glitch_colors, self.glitch_offsets):
            inner_painter.setPen(color)
            jitter_x = dx + random.randint(-1,1)
            jitter_y = dy + random.randint(-1,1)
            inner_painter.drawText(self.base_x + jitter_x, self.base_y + jitter_y, self.text)
        inner_painter.setPen(QColor("white"))
        inner_painter.drawText(self.base_x, self.base_y, self.text)
        inner_painter.end()

        slices = 4 # Pinpoint 멀미날거같아서 4로 줄임
        slice_height = pixmap.height() // slices
        for i in range(slices):
            y = i * slice_height
            offset_x = (random.randint(-1,1) if random.random() > 0.5 else 0) * self.glitch_dist
            source_rect = QRect(self.base_x, y, pixmap.width(), slice_height)
            target_rect = QRect(self.base_x + offset_x, y, pixmap.width(), slice_height)

            painter.drawPixmap(target_rect, pixmap, source_rect)
        
        painter.end()



# Generate Widget
class TestWindow(QWidget):
    __encode_modeList = [ "Base64", "Unnamed", "Hint" ]
    small_font = QFont('Arial', 8)

    def __init__(self):
        super().__init__()
        self.AddUI()
        self.SetUIFeature()
        self.SetUIStyle()

    def AddUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint) # Remove Default Title Bar (cannot change style of it)

        self.titleBar = TitleBar(self)

        radioBox = GlowGroupBox("Menu")
        self.menu0 = QRadioButton(self.__encode_modeList[0])
        self.menu1 = QRadioButton(self.__encode_modeList[1])
        self.menu2 = QRadioButton(self.__encode_modeList[2])
        radioBox_layout = QVBoxLayout(radioBox)
        self.radioBox_widgets = [
            self.menu0,
            self.menu1,
            #self.menu2,
        ]
        for radioBox_widget in self.radioBox_widgets:
            radioBox_layout.addWidget(radioBox_widget)


        encodeBox = GlowGroupBox("Encode/Decode")
        self.input_text = QLineEdit("")
        self.input_password = QLineEdit("pw")
        self.encode_btn = QPushButton("🔒Encode")
        self.decode_btn = QPushButton("🔑Decode")
        self.output_text = GlitchLabel(200, 30, QFont(main_font, 22, QFont.Bold),"Glitch Text", 1) # Pinpoint  멀미날거같아서 1로 줄임
        self.output_status_text = QLabel("Idle")

        encodeBox_layout = QVBoxLayout(encodeBox)
        self.encodeBox_widgets = [
            self.input_text,
            self.input_password,
            self.encode_btn,
            self.decode_btn,
            self.output_text,
            #self.output_status_text
        ]
        for encodeBox_widget in self.encodeBox_widgets:
            encodeBox_layout.addWidget(encodeBox_widget)


        self.debug_text = QLabel("")
        self.mainBox_layout = QVBoxLayout()
        self.mainBox_widgets = [
            self.titleBar,
            radioBox,
            encodeBox,
            self.debug_text
        ]
        for mainBox_widget in self.mainBox_widgets:
            self.mainBox_layout.addWidget(mainBox_widget)

        self.setLayout(self.mainBox_layout)



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
        self.resize(504, 504)
        self.mainBox_layout.setContentsMargins(7, 0, 7, 11)

        self.titleBar.setContentsMargins(0, 0, 0, 15)

        self.output_text.setFixedHeight(60)
        self.output_text.setAlignment(Qt.AlignCenter)

        self.setObjectName("window")
        
        self.input_text.setObjectName("input_text")
        self.output_text.setObjectName("output_text")

        # Concept: glitch, distopia, terminal
        self.setStyleSheet(f"""\
                        #window{{
                           background-color: {black};
                            font-family: sans-serif;

                        }}
                        QGroupBox{{
                            margin: 3px 0 0 0;
                            padding: 20px;
                            background-color: {dark_purple};
                            border: 1px solid {celeste};
                            color: FF4FAD;
                        }}
                        QGroupBox::title{{
                            margin: 5px;
                           color: {brilliant_rose};
                           background-color: {eminence + "64"}; 
                           font-weight: bold;
                           font-size: 12px;
                           
                        }}

                        QRadioButton{{
                            color: {electric_blue};
                        }}

                        QLineEdit{{
                           background-color: {federal_blue};
                           border-radius: 5px;
                           font-family: {main_font};
                           font-size: 15px;
                           color: {electric_blue};
                        }}
                        QLineEdit:disabled{{
                            color: {transparent};
                        }}

                        QPushButton{{
                            border: 1px solid {electric_blue};
                            border-radius: 5px;
                            background-color: {dark_purple};
                            color: {electric_blue};
                        }}
                        QPushButton:hover{{
                            background-color: {true_blue};
                        }}

                        #output_text{{
                           background-color: {black};
                           border-radius: 5px;
                        }}""")
        self.debug_text.setFont(self.small_font)
        



    def EncodeNavigator(self):
        self.ClearDebugText()

        encodedMode = -1
        if(self.menu0.isChecked()): 
            self.Encode_Base64(1)
            encodedMode = 0
        elif(self.menu1.isChecked()):
            self.Encode_Unnamed(1)
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
            self.Encode_Unnamed(0)
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
            except (base64.binascii.Error, UnicodeDecodeError) as e:
                coded_data = "[Enter Correct base64-encoded string.😠]"
                self.RaiseDebugTextErr(str(e))
            else:
                coded_data = coded_data.decode("utf-8")

        self.output_text.ChangeText(coded_data)

    def Encode_Unnamed(self, mode: bool):
        raw_data = self.input_text.text()
        self.output_text.ChangeText(raw_data)

    def Encode_Hint(self, mode: bool):
        self.output_text.setText(self.input_text.text())

    

    def TogglePasswordInput(self):
        if(self.menu1.isChecked()):
            self.input_password.setEnabled(True)
        else:
            self.input_password.setEnabled(False)

    def VisualizeText(self, beforeText, afterText):
        timeDuration = 20 # > 0
        changeCounts = 20 # r # >= 1 
        changeIntervalMs = int((timeDuration / changeCounts) * 1000)

        self._visualize_step = 0
        self._visualize_timer = QTimer()

        selectionBox = list(range(len(beforeText)))
        selectCount = round(len(beforeText) * (1 - 1/(changeCounts ** (1/changeCounts)))) # 전체 n개중에 m개 선택, r번 -> ((n-m)/n)^r = 1/r
        textList = list(beforeText)
        self.output_text.setText(''.join(textList))

        def update_text():
            if self._visualize_step >= changeCounts:
                self._visualize_timer.stop()
                self.output_text.setText(afterText)
                return

            random.shuffle(selectionBox)
            for j in range(selectCount):
                textList[selectionBox[j]] = afterText[selectionBox[j]]

            self.output_text.setText(''.join(textList))
            self._visualize_step += 1

        self._visualize_timer.timeout.connect(update_text)
        self._visualize_timer.start(changeIntervalMs)
            




    def RaiseDebugTextErr(self, s: str):
        self.debug_text.setText("Error: " + s)
    def ClearDebugText(self):
        self.debug_text.setText("")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_()) # wait until app Executed

