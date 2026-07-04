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
        d = DialogLoseTime(self)
        d.exec_()

class PromotionSquares(QPushButton):
    def __init__(self, square_size, piece = None, parent = None):
        super().__init__(parent)
        self.piece = piece
        self.setFixedSize(square_size, square_size)
        self.setIconSize(QSize(int(self.width() * (15/16)), int(self.height() * (15/16))))
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
    selected_piece = pyqtSignal(str)
    def __init__(self, color, square_size, parent = None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.grid = QVBoxLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)

        if color == 'w':
            promote_queen = PromotionSquares(square_size, Queen(color), self)
            self.grid.addWidget(promote_queen)
            promote_rook = PromotionSquares(square_size, Rook(color, 'l'), self)
            self.grid.addWidget(promote_rook) 
            promote_bishop = PromotionSquares(square_size, Bishop(color), self) 
            self.grid.addWidget(promote_bishop)
            promote_knight = PromotionSquares(square_size, Knight(color), self) 
            self.grid.addWidget(promote_knight)

        else:
            promote_knight = PromotionSquares(square_size, Knight(color), self) 
            self.grid.addWidget(promote_knight)
            promote_bishop = PromotionSquares(square_size, Bishop(color), self) 
            self.grid.addWidget(promote_bishop)
            promote_rook = PromotionSquares(square_size, Rook(color, 'l'), self)
            self.grid.addWidget(promote_rook)
            promote_queen = PromotionSquares(square_size, Queen(color), self)
            self.grid.addWidget(promote_queen)


        self.setLayout(self.grid)

        promote_knight.clicked.connect(lambda: self.signal_piece_to_main('K'))
        promote_bishop.clicked.connect(lambda: self.signal_piece_to_main('B'))
        promote_rook.clicked.connect(lambda: self.signal_piece_to_main('R'))
        promote_queen.clicked.connect(lambda: self.signal_piece_to_main('Q'))

    def signal_piece_to_main(self, piece):

        self.selected_piece.emit(piece)
        self.accept()














class Dialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 400)
        bg_color = '#2b2b2b'
        bg_color_hover = "#3E3D3D"
        self.action = None

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
        cross = cross.replace('\\', '/')
        cross_hover = cross_hover.replace('\\', '/')
        self.button_close.setStyleSheet(f'''
                QPushButton {{background-color: transparent; border-top-right-radius: 20px; border: none; 
                            image: url({cross}); padding: 5px;}}
                QPushButton:hover {{image: url({cross_hover});
                }}''')
        self.button_close.clicked.connect(self.close)

        self.button_new = QPushButton(self)
        self.button_new.setGeometry(self.frame.x() + 20, self.frame.y() + ((5 * self.frame.height()) // 8)-15, self.frame.width() - 40, (self.frame.height() // 4)- 20)
        self.button_new.setText('Play Again')
        self.button_new.setStyleSheet(f'''
                                    QPushButton {{
                                      font-family: Arial; font-weight: bold; font-size: 26px; background-color: #327535; border-radius: 20px; color: white;}}
                                    QPushButton:hover {{background-color: #519654;}}
                                      ''')
        self.button_new.clicked.connect(self.play_again)

        self.button_review = QPushButton(self)
        self.button_review.setGeometry(self.button_new.x(), self.frame.y() + (1 * self.frame.height()) // 3, self.button_new.width(), (self.button_new.height()))
        self.button_review.setText('Game Review')
        self.button_review.setStyleSheet(f'''
                                         QPushButton {{font-family: Arial; font-weight: bold; font-size: 26px; border-radius: 20px; background-color: #41316e; color: white;}}
                                         QPushButton:hover {{background-color: #564094;}}
                                         ''')
        self.button_review.clicked.connect(self.review)

        self.button_menu = QPushButton(self)
        self.button_menu.setGeometry(self.button_new.x(), self.frame.y() + ((7 * self.frame.height()) // 8)-13, self.button_new.width(), (self.button_new.height()//2))
        self.button_menu.setText('Back to Menu')
        self.button_menu.setStyleSheet(f'''
                                         QPushButton {{font-family: Arial; font-size: 18px; border-radius: 5px; background-color: {bg_color}; border-radius: 5px; color: white;}}
                                         QPushButton:hover {{background-color: {bg_color_hover};}}
                                         ''')
        self.button_menu.clicked.connect(self.menu)

    def showEvent(self, event):
        self.button_close.raise_()
        super().showEvent(event)
    
    def close(self):
        self.accept()


    def play_again(self):

        self.action = 'play again'
        self.accept()
        
        

    def review(self):
        pass

    def menu(self):
        self.action = 'menu'
        self.accept()


class DialogWin(Dialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.label_text_top = QLabel(self)
        self.label_text_top.setGeometry(self.label_top.x() + self.label_top.width() // 4, self.label_top.y() + 10, self.label_top.width() // 2, (3 * self.label_top.height()) // 5)
        self.label_text_top.setStyleSheet('font-family: Arial; font-weight: bold; font-size: 26px; color: white')
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
        self.label_text_top.setStyleSheet('font-family: Arial; font-weight: bold; font-size: 26px; color: white')
        self.label_text_top.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if player_color == 'w':
            self.label_text_top.setText('Schwarz hat gewonnen')
        elif player_color == 'b': 
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
        self.label_text_top.setStyleSheet('font-family: Arial; font-weight: bold; font-size: 26px; color: white')
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

class Confirmation(QWidget):
    new_game_signal = pyqtSignal()
    menu_signal = pyqtSignal()
    def __init__(self, width, height, parent = None):
        super().__init__(parent)


        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, width, height)
        background_color = '#1e1e1f'
        self.frame.setStyleSheet(f'background-color: {background_color}; border-radius: 10px;')


        self.label = QLabel(self)
        self.label.setGeometry(5, 5, width, height//2)
        self.label.setText('Do you really want to resgin?')
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.label.setStyleSheet(f'color: white;')
        self.label.setWordWrap(True)

        self.resign = QPushButton(self)
        self.resign.setGeometry(5, height//2 + 10, (width-15) // 2, height//3)
        self.resign.setText('RESIGN')
        self.resign.setStyleSheet(f'''QPushButton {{border: none; font-family: Arial; font-weight: bold; font-size: 15px; color: white; background-color: #f54242; border-radius: 5px;}}
                                         QPushButton:hover {{background-color: #ff7a7a}}''')
        self.resign.clicked.connect(self.resign_dialog)

        self.cancel = QPushButton(self)
        self.cancel.setGeometry(10 + (width-15) // 2 , height//2 + 10, (width-15) // 2, height//3)
        self.cancel.setText('Cancel')
        self.cancel.setStyleSheet(f''' QPushButton {{border: none; font-family: Arial; font-size: 15px; color: white; background-color: #615d5d; border-radius: 5px;}}
                                         QPushButton:hover {{background-color: #948a8a}}''')
        self.cancel.clicked.connect(lambda: self.close())

    def resign_dialog(self):

        resign_dialog = DialogLoseResignation('w')
        self.close()
        resign_dialog.exec_()

        match resign_dialog.action:
            case 'play again':
                self.new_game_signal.emit()

            case 'menu':
                self.menu_signal.emit()







    
    
    
        


        





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())