import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QDialog
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPen, QPainter
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPoint, QSize, QObject, QThread
from ui.board_gui import ChessBoard, ArrowOverlay, EvalBar
from ui.dialogs import Promote, DialogWinMate, DialogLoseMate, DialogRemisPatt, Confirmation
from chessboard.game_controller import GameController
import time
import copy


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Launcher')
        self.setGeometry(750, 450, 300, 300)
        self.game_launcher()

    def game_launcher(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        button1 = QPushButton('Freies-Spiel starten', self)
        button1.setMinimumHeight(100)
        button2 = QPushButton('Spiel gegen Computer starten', self)
        button2.setMinimumHeight(100)
        button3 = QPushButton('Eröffnungsdatenbank', self)
        button3.setMinimumHeight(100)

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        button1.clicked.connect(self.game)
        central_widget.setLayout(layout)

    def game(self):
        self.window = ChessGame()
        self.window.show()
        self.hide()

class EngineWorker(QObject):
    finished = pyqtSignal(float)
    def __init__(self, engine, position):
        super().__init__()

        self.engine = engine
        self.position = position

    def run(self):
        value = self.engine.minimax(self.position, 3,-100000, 100000)
        self.finished.emit(value)



class ChessGame(QMainWindow):
    def __init__(self):
        self.arrows = []
        super().__init__()
                
        self.resign_button_pressed = False
        self.setWindowTitle('Schach')
        self.setGeometry(350, 450, 1024, 683)
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(f'background-color: #28292b;')
        self.setCentralWidget(self.central_widget)
        self.setMinimumSize(600, 350)


        self.GameController = GameController()

        self.board_widget = ChessBoard(self.GameController.gameEngine, self)
        self.board_widget.arrow_signal.connect(self.get_arrow_signal)
        self.board_widget.delete_signal.connect(self.delete_arrows)
        self.board_widget.move_signal.connect(self.update_evalbar)
        self.board_widget.setGeometry(20, 20, self.width() // 2, 3 * self.height() // 4)

        self.overlay = ArrowOverlay(self.arrows, self.board_widget)
        self.overlay.setGeometry(0, 0, self.board_widget.width(), self.board_widget.height())

        self.resign_button = QPushButton(self)
        self.resign_button.setGeometry(40+ self.board_widget.width(), 40+ self.board_widget.height(), self.board_widget.width()//4, self.board_widget.width()//16)
        self.resign_button.setText('RESIGN')
        self.resign_button.setStyleSheet(f''' QPushButton {{border: none; font-family: Arial; font-weight: bold; font-size: 15px; color: white; background-color: #f54242;}}
                                         QPushButton:hover {{background-color: #ff7a7a}}''')
        self.resign_button.clicked.connect(self.resign)


        self.eval_bar = EvalBar(self.board_widget.width() // 24, self.board_widget.height(), self)
        self.eval_bar.move(7*self.width() // 8, 20)
        self.eval_bar.resize(self.board_widget.width() // 24, self.board_widget.height())




    def resign(self):

        self.resign_button_pressed = True
        width = 256
        height = 130
        self.confirmation = Confirmation(width, height, self)
        self.confirmation.setGeometry(self.resign_button.x(), self.resign_button.y() - 150 , width, height)
        self.confirmation.show()

    def analysis_finished(self, value):

        print(self.GameController.ultimate.calculations)
        self.GameController.ultimate.calculations = 0
        self.eval_bar.setEval(value)



    def update_evalbar(self, position):

        self.thread = QThread()
        self.worker = EngineWorker(self.GameController.ultimate, copy.deepcopy(position))
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.analysis_finished)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()



    def get_arrow_signal(self, arrows):
        self.arrows.append(arrows[0])
        self.overlay.update()

    def delete_arrows(self):
        self.arrows.clear()
        self.overlay.update()


    def resizeEvent(self, e):

        super().resizeEvent(e)

        size = min(self.width() // 2, 3 * self.height() // 4)
        self.board_widget.resize(size, size)

        self.overlay.resize(self.board_widget.size())
        self.overlay.show()

        self.resign_button.setGeometry(40+ self.board_widget.width(), 40+ self.board_widget.height(), self.board_widget.width()//4, self.board_widget.width()//16)


        self.eval_bar.resize(self.board_widget.width() // 24, self.board_widget.height())

        if self.resign_button_pressed == True:

            self.confirmation.close()
            self.resign_button_pressed = False

        








        




def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = Launcher()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
