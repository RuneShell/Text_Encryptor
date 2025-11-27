"""
File: GUI.py
Author: RuneShell
        dlhj09@naver.com
        https://github.com/RuneShell
Locate: https://github.com/RuneShell/Text_Encryptor
License: GPL-3.0 License - Copyright (c) 2025, RuneShell
        Following GPL-3.0 License : [pyqt5] Copyright (c) Riverbank Computing Limited
----------------------------------
Brief: 
"""

import sys
import random
import base64

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, 
                             QGroupBox, QTextEdit, QLineEdit, QLabel, QRadioButton, QPushButton, QSpacerItem,
                             QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint # Qt for AlignCenter
from PyQt5.QtGui import QFont, QPainter, QColor, QPixmap, QFontMetrics
# QTimer, QRect, QPainter, QPixmap, QColor, QFontMetrics for Glitch Animation  

import CeasorHash # CeasorHash.pyd built on "python 3.10"


# Colors
transparent = "#00000000"

black="#01000A" # window background

dark_purple="#080120" # groupBox background
federal_blue="#0D0643" # textBox (disabled)
medium_slate_blue = "#F9F6FF" # textBox "#8C52FF"

celeste = "#C8FDFD" # border
sky_blue = "#64C4E8" # border shadow

electric_blue2 = "#7EE7F9" # first point color
rose_pink = "#FF6EC7" # second point color

cinnabar = "#E94F37" # GUI accent 1
screamin_green = "#73FA79" # GUI accent 2


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
        self.title = GlitchLabel(130, 20, QFont(main_font, 10, QFont.Bold),"Glitch Encoder", 1)
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
                            QPushButton#titleMinBtn:hover{{ color: {screamin_green}; }}
                            QPushButton#titleMaxBtn:hover{{ color: {screamin_green}; }}
                            QPushButton#titleCloseBtn:hover{{ color: {cinnabar}; }}
                            """)

        
    def SetUIFeature(self):
        self.titleMinBtn.clicked.connect(self.window().showMinimized)
        self.titleMaxBtn.clicked.connect(self.ToggleMaxScreen)
        self.titleCloseBtn.clicked.connect(self.window().close)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape: # ESC -> close window
            self.window().close()


    def ToggleMaxScreen(self):
        window = self.window()
        if(window.isMaximized()):
            window.showNormal()
            self.titleMaxBtn.setText("⛶") # MaxScreen Icon
        else:
            window.showMaximized()
            self.titleMaxBtn.setText("🗗") # Restore Icon

    def mouseDoubleClickEvent(self, event):
        self.ToggleMaxScreen()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._mouse_pos = event.globalPos()
            self._window_pos = self.window().pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self._mouse_pos
            self.window().move(self._window_pos + delta)
            event.accept()


# Custom QGroupBox which has 2 shadows
class GlowGroupBoxFrame(QFrame): # QFrame for 2 shadows
    groupBox = None
    def __init__(self, text):
        super().__init__()

        frameGlow = QGraphicsDropShadowEffect() # Right-below shadow on QFrame
        frameGlow.setBlurRadius(10) 
        frameGlow.setOffset(8, 10)
        shadowColor = QColor(rose_pink)
        shadowColor.setAlpha(150)
        frameGlow.setColor(shadowColor)
        self.setGraphicsEffect(frameGlow)
        
        
        groupBox_layout = QVBoxLayout(self)
        self.groupBox = QGroupBox(text)
        groupBox_layout.addWidget(self.groupBox)

        glow = QGraphicsDropShadowEffect(self.groupBox) # Left-upper  on GroupBox
        glow.setBlurRadius(40)
        glow.setOffset(-3, -3)
        shadowColor = QColor(sky_blue)
        shadowColor.setAlpha(220)
        glow.setColor(shadowColor)
        self.groupBox.setGraphicsEffect(glow)
       


# Custom QLabel that shows Glitch text
class GlitchLabel(QLabel):
    def __init__(self, width, height, font, text, glitch_dist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        self.setMinimumSize(width, height)
        self.setFont(font)
        self.ChangeText(text)
        self.fixed_glitch_dist = glitch_dist
        self.fixed_slices = 6
        self.glitch_dist = glitch_dist
        self.slices = self.fixed_slices # 멀미날거같으면 4로 줄임



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.base_x = self.width()//2 - QFontMetrics(self.font()).width(self.text)//2
        self.base_y = self.height()//2 + self.font().pointSize()//2
        self.base_x = 3  if self.base_x < 0 else self.base_x
        
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

        slices = self.slices 
        slice_height = pixmap.height() // slices
        for i in range(slices):
            y = i * slice_height
            offset_x = (random.randint(-1,1) if random.random() > 0.5 else 0) * self.glitch_dist
            source_rect = QRect(self.base_x, y, pixmap.width(), slice_height)
            target_rect = QRect(self.base_x + offset_x, y, pixmap.width(), slice_height)

            painter.drawPixmap(target_rect, pixmap, source_rect)
        
        painter.end()


    def ChangeText(self, text):
        self.text = text  

    def VisualizeText(self, beforeText, afterText):   
        self.glitch_dist = 4
        self.slices = 9

        timeDuration = 2 # > 0
        changeCounts = 20 # r # >= 1 
        changeIntervalMs = int((timeDuration / changeCounts) * 1000)

        self._visualize_step = 0
        self._visualize_timer = QTimer()

        selectionBox = list(range(len(beforeText)))
        selectCount = round(len(beforeText) * (1 - 1/(changeCounts ** (1/changeCounts)))) # 전체 n개중에 m개 선택, r번 -> ((n-m)/n)^r = 1/r.
        textList = list(beforeText)
        self.ChangeText(''.join(textList))

        def update_text():
            if self._visualize_step >= changeCounts:
                self._visualize_timer.stop()
                self.ChangeText(afterText)

                self.glitch_dist = self.fixed_glitch_dist
                self.slices = self.fixed_slices
                return

            random.shuffle(selectionBox)
            for j in range(selectCount):
                textList[selectionBox[j]] = afterText[selectionBox[j]]

            self.ChangeText(''.join(textList))
            self._visualize_step += 1

        self._visualize_timer.timeout.connect(update_text)
        self._visualize_timer.start(changeIntervalMs)





class MainWindow(QWidget):
    __encode_modeList = [ "Base64", "CeasorHash", "Hint" ]
    small_font = QFont('Arial', 8)

    __ceasorHash = CeasorHash.CeasorHash()

    # Window Resize handles
    _resize_handle_size = 10 # 크기 조절 핸들 영역 (px)
    _resizing = False
    _moving = False
    _start_pos = QPoint()
    _start_geometry = QRect()
    _resize_direction = Qt.Edges() # 크기 조절 방향 (초기값 없음)

    def __init__(self):
        super().__init__()
        self.AddUI()
        self.SetUIFeature()
        self.SetUIStyle()

        self.setMouseTracking(True) # For mouseMoveEvent()

    def AddUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint) # Remove Default Title Bar (cannot change style of default title bar)

        self.titleBar = TitleBar(self)

        radioBox = GlowGroupBoxFrame("Menu")
        self.menu0 = QRadioButton(self.__encode_modeList[0])
        self.menu1 = QRadioButton(self.__encode_modeList[1])
        self.menu2 = QRadioButton(self.__encode_modeList[2])
        radioBox_layout = QVBoxLayout(radioBox.groupBox)
        self.radioBox_widgets = [
            self.menu0,
            self.menu1,
            #self.menu2,
        ]
        for radioBox_widget in self.radioBox_widgets:
            radioBox_layout.addWidget(radioBox_widget)


        self.encodeBox = GlowGroupBoxFrame("Encode/Decode")
        self.input_text = QTextEdit("")
        self.input_password = QLineEdit("")
        self.spacer1 = QSpacerItem(10, 20, QSizePolicy.Fixed)
        self.encode_btn = QPushButton("🔒Encode")
        self.decode_btn = QPushButton("🔑Decode")
        self.spacer2 = QSpacerItem(10, 20, QSizePolicy.Fixed)
        self.output_text = GlitchLabel(200, 15, QFont(main_font, 15, QFont.Bold),"Glitch Text", 1) # Pinpoint  멀미날거같아서 1로 줄임
        self.copy_btn = QPushButton("copy")
        self.output_status_text = QLabel("Idle")

        encodeBox_layout = QVBoxLayout(self.encodeBox.groupBox)
        self.encodeBox_widgets = [
            self.input_text,
            self.input_password,
            self.spacer1,
            self.encode_btn,
            self.decode_btn,
            self.spacer2,
            self.output_text,
            self.copy_btn
            #self.output_status_text
        ]
        for encodeBox_widget in self.encodeBox_widgets:
            if isinstance(encodeBox_widget, QSpacerItem):
                encodeBox_layout.addItem(encodeBox_widget) # for Spacer
            else:
                encodeBox_layout.addWidget(encodeBox_widget)

        self.debug_text = QLabel("")
        self.mainBox_layout = QVBoxLayout()
        self.mainBox_widgets = [
            self.titleBar,
            radioBox,
            self.encodeBox,
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
        
        self.input_text.setPlaceholderText("text")
        self.input_text.textChanged.connect(lambda: self.output_text.ChangeText(self.input_text.toPlainText()))

        self.input_password.setPlaceholderText("password disabled")
        self.input_password.setEnabled(False)

        self.encode_btn.clicked.connect(self.EncodeNavigator)
        self.decode_btn.clicked.connect(self.DecodeNavigator)
        self.copy_btn.clicked.connect(lambda: self.CopyToClipboard(self.output_text.text))

        self.output_text.setTextInteractionFlags(Qt.TextSelectableByMouse)


    def SetUIStyle(self):
        self.resize(520, 520)
        self.mainBox_layout.setContentsMargins(7, 0, 7, 11)

        self.titleBar.setContentsMargins(0, 0, 0, 15)

        self.encodeBox.setMaximumHeight(420)

        self.output_text.setFixedHeight(65)
        self.output_text.setAlignment(Qt.AlignCenter)

        self.setObjectName("window")
        
        self.input_text.setObjectName("input_text")
        self.input_password.setObjectName("input_password")
        self.output_text.setObjectName("output_text")
        self.copy_btn.setFixedHeight(25)

        self.input_text.setFixedHeight(60)
        self.input_text.setFrameStyle(0)

        # Concept: glitch
        # QSS
        self.setStyleSheet(f"""\
                        #window{{
                           background-color: {black};       /* background */
                            font-family: sans-serif;

                        }}
                        QGroupBox{{
                            margin: 3px 0 0 0;
                            padding: 20px;
                            background-color: {dark_purple};        /* GroupBox color */
                            border: 1px solid {electric_blue2};        /* GroupBox border */
                            font-weight: bold;
                        }}
                        QGroupBox::title{{
                            margin: 5px;
                           color: {electric_blue2};
                           background-color: {transparent}; 
                        }}

                        QRadioButton{{
                            color: {rose_pink};
                            font-weight: bold;
                        }}


                        QScrollBar:vertical {{
                            border: none;
                            background: #8C3C6D;
                            width: 15px;
                            /*border-radius: 7px;*/
                        }}
                        QScrollBar::add-line:vertical,
                        QScrollBar::sub-line:vertical {{
                            height: 0px;
                        }}
                        QScrollBar::add-page:vertical,
                        QScrollBar::sub-page:vertical {{
                            background: none;
                        }}
                        QScrollBar::handle:vertical {{
                            background: {rose_pink};
                            min-height: 5px;
                            /*border-radius: 7px;*/
                        }}


                        QTextEdit{{
                            background-color: {medium_slate_blue};
                           border-radius: 5px;
                           font-family: {main_font};
                           font-size: 15px;
                        }}

                        #input_text{{
                            color: {electric_blue2};
                        }}

                        #input_password{{
                            color: {cinnabar}; /* OVERWRITE BY #input_password:disabled::placeholder */
                            background-color: {medium_slate_blue};
                           border-radius: 5px;
                           font-family: {main_font};
                           font-size: 15px;
                        }}
                        #input_password::placeholder{{
                            color: {cinnabar}; /* only gray? */
                        }}
                        #input_password:disabled{{
                            /*color: {federal_blue};*/ /* OVERWRITE BY #input_password:disabled::placeholder */
                            background-color: {federal_blue};
                        }}
                        /*
                        #input_password:disabled::placeholder{{
                            color: {cinnabar};
                        }}
                        */


                        QPushButton{{
                            border: 1px solid {electric_blue2};
                            border-radius: 5px;
                            background-color: {transparent};
                            color: {electric_blue2};
                        }}
                        QPushButton:hover{{
                            /*border: 1px solid {medium_slate_blue};*/
                            background-color: {electric_blue2};
                            color: {medium_slate_blue};
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

    def CopyToClipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)



    # Encode/Decode methods. mode=1(Encode), mode=0(Decode)
    def Encode_Base64(self, mode: bool):
        raw_data = self.input_text.toPlainText()
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

        self.__coded_str = coded_data
        self.output_text.ChangeText(coded_data)

    def Encode_CeasorHash(self, mode: bool):
        raw_data = self.input_text.toPlainText()
        raw_pw = self.input_password.text()
        coded_data = list(raw_data.encode("utf-8"))
        coded_pw = list(raw_pw.encode("utf-8"))

        coded_data = self.__ceasorHash.EncryptWithCeasorHash(coded_data, coded_pw, mode, 1)
        
        self.output_text.VisualizeText(raw_data, bytes(coded_data).decode("utf-8"))



    def Encode_Hint(self, mode: bool):
        self.output_text.setText(self.input_text.toPlainTextext())

    

    def TogglePasswordInput(self): # when click Radio Button, called TWICE.
        if(self.menu1.isChecked()):
            self.input_password.setEnabled(True)
            #self.input_password.setText(self.__password_input)
        else:
            #self.__password_input = self.input_password.text()
            self.input_password.setEnabled(False)
            self.input_password.setText("")


            




    def RaiseDebugTextErr(self, s: str):
        self.debug_text.setText("Error: " + s)
    def ClearDebugText(self):
        self.debug_text.setText("")




    # --- 크기 조절 기능 추가 ---
    def _get_resize_direction(self, pos: QPoint) -> Qt.Edges:
        """마우스 위치에 따라 크기 조절 방향을 결정합니다."""
        width = self.width()
        height = self.height()
        handle = self._resize_handle_size
        direction = Qt.Edges()

        # 코너
        if pos.x() <= handle and pos.y() <= handle:
            direction |= Qt.TopEdge | Qt.LeftEdge
        elif pos.x() >= width - handle and pos.y() <= handle:
            direction |= Qt.TopEdge | Qt.RightEdge
        elif pos.x() <= handle and pos.y() >= height - handle:
            direction |= Qt.BottomEdge | Qt.LeftEdge
        elif pos.x() >= width - handle and pos.y() >= height - handle:
            direction |= Qt.BottomEdge | Qt.RightEdge
        # 가장자리
        elif pos.x() <= handle:
            direction |= Qt.LeftEdge
        elif pos.x() >= width - handle:
            direction |= Qt.RightEdge
        elif pos.y() <= handle:
            direction |= Qt.TopEdge
        elif pos.y() >= height - handle:
            direction |= Qt.BottomEdge
        return direction

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._start_pos = event.globalPos()
            self._start_geometry = self.geometry()
            self._resize_direction = self._get_resize_direction(event.pos())

            if self._resize_direction != Qt.Edges():
                self._resizing = True
            else:
                if self.titleBar.geometry().contains(event.pos()):
                    self._moving = True
                else:
                    self._moving = False
            event.accept()

    def mouseMoveEvent(self, event):
        if self._resizing:
            delta = event.globalPos() - self._start_pos
            new_geometry = QRect(self._start_geometry)

            if self._resize_direction & Qt.LeftEdge:
                new_geometry.setLeft(new_geometry.left() + delta.x())
            if self._resize_direction & Qt.RightEdge:
                new_geometry.setRight(new_geometry.right() + delta.x())
            if self._resize_direction & Qt.TopEdge:
                new_geometry.setTop(new_geometry.top() + delta.y())
            if self._resize_direction & Qt.BottomEdge:
                new_geometry.setBottom(new_geometry.bottom() + delta.y())

            min_width = self.minimumWidth()
            min_height = self.minimumHeight()

            if new_geometry.width() < min_width:
                if self._resize_direction & Qt.LeftEdge:
                    new_geometry.setLeft(self._start_geometry.right() - min_width)
                else:
                    new_geometry.setWidth(min_width)
            if new_geometry.height() < min_height:
                if self._resize_direction & Qt.TopEdge:
                    new_geometry.setTop(self._start_geometry.bottom() - min_height)
                else:
                    new_geometry.setHeight(min_height)

            self.setGeometry(new_geometry)

        # 마우스 이동 로직
        elif self._moving and event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self._start_pos
            self.move(self._start_geometry.topLeft() + delta)

        else:
            # 마우스 버튼이 눌리지 않은 상태에서 움직일 때 커서 변경
            direction = self._get_resize_direction(event.pos())
            if direction == (Qt.LeftEdge | Qt.TopEdge) or direction == (Qt.RightEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeFDiagCursor)
            elif direction == (Qt.RightEdge | Qt.TopEdge) or direction == (Qt.LeftEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeBDiagCursor)
            elif direction & (Qt.LeftEdge | Qt.RightEdge):
                self.setCursor(Qt.SizeHorCursor)
            elif direction & (Qt.TopEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeVerCursor)
            else:
                self.setCursor(Qt.ArrowCursor) # 기본 커서로 변경
            event.accept()


    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._moving = False
        self.setCursor(Qt.ArrowCursor)
        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        super().paintEvent(event)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) # wait until app Executed