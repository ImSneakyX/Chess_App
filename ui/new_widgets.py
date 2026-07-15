from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import QRectF
import sys

class ToggleSwitch(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFixedSize(60, 32)


    


    def paintEvent(self, event):

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        color  = QColor("#000000")

        brush = QBrush(color)
        pen = QPen(color)

        p.setPen(pen)
        #p.setBrush(brush)
        rec = QRectF(0, 0, self.width() - 2, self.height() - 2)
        p.drawRoundedRect(rec, 50, 50)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Test Window')
        self.setGeometry(500, 500, 200, 200)

        self.toggle= ToggleSwitch(self)
        self.toggle.move(50, 50)




if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())