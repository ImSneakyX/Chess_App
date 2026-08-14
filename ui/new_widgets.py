from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import QRectF, pyqtProperty, QPropertyAnimation, Qt, QPointF
import sys

class ToggleSwitch(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFixedSize(60, 32)

        self._checked = False
        self._x_circle = 3
        self.anim = QPropertyAnimation(self, b'x_circle')
        self.anim.setDuration(180)

    def get_x(self):
        return self._x_circle
    
    def set_x(self, x):

        self._x_circle = x
        self.update()

    x_circle = pyqtProperty(float, get_x, set_x)

    
    def mousePressEvent(self, event):

        self._checked = not self._checked
        self.anim.stop()

        self.anim.setStartValue(self._x_circle)

        if self._checked:
            self.anim.setEndValue(31)
        else: 
            self.anim.setEndValue(3)

        self.anim.start()

        
    def paintEvent(self, event):

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self._checked:
            bg = '#00c853'
        else: 
            bg = '#4a4a4a'

        brush = QBrush(QColor(bg))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(brush)
        rec = QRectF(0, 0, self.width(), self.height())
        p.drawRoundedRect(rec, 16, 16)
        p.setBrush(QBrush(QColor('white')))
        p.drawEllipse(QPointF(self._x_circle + 13, 16), 13, 13)


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