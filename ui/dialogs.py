import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QDialog, QFrame
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from ui.drag_drop import ChessSquare
from chessboard.pieces import Knight, Queen, Bishop, Rook


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('test')
        self.setGeometry(750, 450, 300, 300)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        button1 = QPushButton('Mate')
        button2 = QPushButton('Stalemate')
        layout = QHBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        centralWidget.setLayout(layout)
        button1.clicked.connect(self.show_dialog)
        button2.clicked.connect(self.show_dialog)


    def show_dialog(self):
        #d = DialogLoseTime(self)
        d = Promote('w', self)
        d.exec_()

class PromotionSquares(QPushButton):
    def __init__(self, piece = None, parent = None):
        super().__init__(parent)
        self.piece = piece

        self.setFixedSize(64, 64)
        self.setIconSize(QSize(60, 60))
        self.setAcceptDrops(True)
   

        self.setStyleSheet('background-color: white; border: none;')

        self.set_piece()

        

    def set_piece(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if self.piece is None or self.piece.value == 0:
            self.setIcon(QIcon())
            return
        image_path = os.path.join(base_path, 'Images', f'{self.piece.name}_{self.piece.color}.png')
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(120, 120, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        pixmap.setDevicePixelRatio(2.0)
        icon = QIcon(pixmap)
        self.setIcon(icon)



class Promote(QDialog):
    selected_piece = pyqtSignal(object)
    def __init__(self, color, parent = None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        promote_knight = PromotionSquares(Knight(color), self) 
        promote_knight.setGeometry(0, 64, 64, 64)
        promote_bishop = PromotionSquares(Bishop(color), self) 
        promote_bishop.setGeometry(0, 128, 64, 64)
        promote_rook = PromotionSquares(Rook(color, 'l'), self)
        promote_rook.setGeometry(0, 192, 64, 64) 
        promote_queen = PromotionSquares(Queen(color), self)
        promote_queen.setGeometry(0, 0, 64, 64) 

        promote_knight.clicked.connect(lambda: self.signal_piece_to_main(promote_knight.piece))
        promote_bishop.clicked.connect(lambda: self.signal_piece_to_main(promote_bishop.piece))
        promote_rook.clicked.connect(lambda: self.signal_piece_to_main(promote_rook.piece))
        promote_queen.clicked.connect(lambda: self.signal_piece_to_main(promote_queen.piece))

    def signal_piece_to_main(self, object):

        self.selected_piece.emit(object)
        self.accept()














class Dialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 400)
        bg_color = '#2b2b2b'
        bg_color_hover = "#3E3D3D"

        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 400, 400)
        self.frame.setStyleSheet('background-color: #1e1e1f; border-radius: 20px;')

        self.label_top = QLabel(self)
        self.label_top.setStyleSheet(f'background-color: {bg_color}; border-top-right-radius: 20px; border-top-left-radius: 20px;')
        self.label_top.setGeometry(0, 0, 400, 100)
        

        self.button_close = QPushButton(self)
        self.button_close.setGeometry(self.label_top.width() - 40, 0, 40, 40)
        cross = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Images', 'cross.png')
        cross_hover = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Images', 'cross_hover.png')
        self.button_close.setStyleSheet(f'''
                QPushButton {{background-color: transparent; border-top-right-radius: 20px; border: none; 
                            image: url({cross}); padding: 5px}}
                QPushButton:hover {{image: url({cross_hover});
                }}''')
        self.button_close.clicked.connect(self.close)

        self.button_new = QPushButton(self)
        self.button_new.setGeometry(self.frame.x() + 20, self.frame.y() + ((5 * self.frame.height()) // 8)-15, self.frame.width() - 40, (self.frame.height() // 4)- 20)
        self.button_new.setText('Play Again')
        self.button_new.setStyleSheet(f'''
                                    QPushButton {{
                                      font-family: Arial; font-weight: bold; font-size: 26px; background-color: #327535; border-radius: 20px;}}
                                    QPushButton:hover {{background-color: #519654;}}
                                      ''')
        self.button_new.clicked.connect(self.play_again)

        self.button_review = QPushButton(self)
        self.button_review.setGeometry(self.button_new.x(), self.frame.y() + (1 * self.frame.height()) // 3, self.button_new.width(), (self.button_new.height()))
        self.button_review.setText('Game Review')
        self.button_review.setStyleSheet(f'''
                                         QPushButton {{font-family: Arial; font-weight: bold; font-size: 26px; border-radius: 20px; background-color: #41316e;}}
                                         QPushButton:hover {{background-color: #564094;}}
                                         ''')
        self.button_review.clicked.connect(self.review)

        self.button_menu = QPushButton(self)
        self.button_menu.setGeometry(self.button_new.x(), self.frame.y() + ((7 * self.frame.height()) // 8)-13, self.button_new.width(), (self.button_new.height()//2))
        self.button_menu.setText('Back to Menu')
        self.button_menu.setStyleSheet(f'''
                                         QPushButton {{font-family: Arial; font-size: 18px; border-radius: 5px; background-color: {bg_color}; border-radius: 5px;}}
                                         QPushButton:hover {{background-color: {bg_color_hover};}}
                                         ''')
        self.button_menu.clicked.connect(self.menu)

    def showEvent(self, event):
        self.button_close.raise_()
        super().showEvent(event)
    
    def close(self):
        self.accept()


    def play_again(self):
        pass

    def review(self):
        pass

    def menu(self):
        pass


class DialogWin(Dialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.label_text_top = QLabel(self)
        self.label_text_top.setGeometry(self.label_top.x() + self.label_top.width() // 4, self.label_top.y() + 10, self.label_top.width() // 2, (3 * self.label_top.height()) // 5)
        self.label_text_top.setStyleSheet('font-family: Arial; font-weight: bold; font-size: 26px;')
        self.label_text_top.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.label_text_top.setText('Du hast gewonnen!')
        self.label_text_top.setWordWrap(True)

        self.label_trophy = QLabel(self)
        self.label_trophy.setGeometry(self.label_top.x(), self.label_top.y(), self.label_top.width() // 4, self.label_top.height())
        pixmap = QPixmap(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Images', 'trophy.png'))
        pixmap = pixmap.scaled(self.label_top.width() // 4, self.label_top.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_trophy.setPixmap(pixmap)


class DialogWinMate(DialogWin):
    def __init__(self, parent = None):
        super().__init__(parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('durch Schachmatt')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogWinTime(DialogWin):
    def __init__(self, parent = None):
        super().__init__(parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('auf Zeit')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogWinResignation(DialogWin):
    def __init__(self, parent = None):
        super().__init__(parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('durch Aufgabe')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogLose(Dialog):
    def __init__(self, player_color, parent = None):
        super().__init__(parent)
        self.label_text_top = QLabel(self)
        self.label_text_top.setGeometry(self.label_top.x(), self.label_top.y() + 10, self.label_top.width(), (3 * self.label_top.height()) // 5)
        self.label_text_top.setStyleSheet('font-family: Arial; font-weight: bold; font-size: 26px;')
        self.label_text_top.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if player_color == 'w':
            self.label_text_top.setText('Schwarz hat gewonnen')
        else: 
            self.label_text_top.setText('Weiß hat gewonnen')
        self.label_text_top.setWordWrap(True)

class DialogLoseMate(DialogLose):
    def __init__(self, player_color, parent = None):
        super().__init__(player_color, parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('durch Schachmatt')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogLoseTime(DialogLose):
    def __init__(self, player_color, parent = None):
        super().__init__(player_color, parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('auf Zeit')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogLoseResignation(DialogLose):
    def __init__(self, player_color, parent = None):
        super().__init__(player_color, parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('durch Aufgabe')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogRemis(Dialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.label_text_top = QLabel(self)
        self.label_text_top.setGeometry(self.label_top.x(), self.label_top.y() + 10, self.label_top.width(), (3 * self.label_top.height()) // 5)
        self.label_text_top.setStyleSheet('font-family: Arial; font-weight: bold; font-size: 26px;')
        self.label_text_top.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_text_top.setText('Remis')
        self.label_text_top.setWordWrap(True)

class DialogRemisRepetition(DialogRemis):
    def __init__(self, player_color, parent = None):
        super().__init__(player_color, parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('durch Stellungswiederholung')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogRemisRepetition(DialogRemis):
    def __init__(self, player_color, parent = None):
        super().__init__(player_color, parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('durch Stellungswiederholung')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogRemisMaterialTime(DialogRemis):
    def __init__(self, parent = None):
        super().__init__(parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('Zeitüberschreitung bei unzureichendem Material')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogRemisMaterial(DialogRemis):
    def __init__(self, parent = None):
        super().__init__(parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('wegen unzureichendem Material')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogRemisPatt(DialogRemis):
    def __init__(self, parent = None):
        super().__init__(parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('wegen Patt')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogRemisAgreement(DialogRemis):
    def __init__(self, parent = None):
        super().__init__(parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('durch Einigung')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

class DialogRemisFiftyMoves(DialogRemis):
    def __init__(self, parent = None):
        super().__init__(parent)
        label = QLabel(self)
        label.setGeometry(self.label_text_top.x(), self.label_text_top.y() + self.label_text_top.height(), self.label_text_top.width(), self.label_top.height() - self.label_text_top.height())
        label.setText('wegen 50 Zug-Regel')
        label.setStyleSheet('font-family: Arial; font-size: 12px; color: #9e9493;')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
    
    
    
        


        





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())