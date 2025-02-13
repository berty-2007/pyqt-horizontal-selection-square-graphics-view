from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem

from pyqt_horizontal_selection_square_graphics_view.selectionSquare import SelectionSquare


class HorizontalSelectionSquareGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__p = 0
        self.__scene = 0
        self.__graphicItem = 0
        self.__sq = 0

    def mousePressEvent(self, e):
        if self.__sq and e.button() == Qt.LeftButton:
            if isinstance(self.__sq, SelectionSquare):
                scene_rect = self.__sq.sceneBoundingRect()
                scene_pos = self.mapToScene(e.pos())
                if scene_rect.contains(scene_pos):
                    rect = self.__sq.rect()
                    scene_pos_x = scene_pos.x()
                    if abs(rect.right()-scene_pos_x) > abs(rect.left()-scene_pos_x):
                        rect.setLeft(scene_pos_x)
                        self.__sq.setRect(rect)
                    else:
                        rect.setRight(scene_pos_x)
                        self.__sq.setRect(rect)
                else:
                    rect = self.__sq.rect()
                    scene_pos_x = scene_pos.x()
                    if scene_pos_x < 0:
                        scene_pos_x = 0
                        rect.setLeft(scene_pos_x)
                        self.__sq.setRect(rect)
                    elif rect.left() > scene_pos_x:
                        rect.setLeft(scene_pos_x)
                        self.__sq.setRect(rect)
                    elif scene_pos_x > self.__scene.sceneRect().right():
                        scene_pos_x = self.__scene.sceneRect().right()-self.__sq.pen().width()//2
                        print(scene_pos_x)
                        rect.setRight(scene_pos_x)
                        self.__sq.setRect(rect)
                    else:
                        rect.setRight(scene_pos_x)
                        self.__sq.setRect(rect)
        return super().mousePressEvent(e)

    def setFile(self, filename):
        self.__p = QPixmap(filename)
        self.__setPixmap(self.__p)

    def __setPixmap(self, p):
        self.__p = p
        self.__scene = QGraphicsScene()
        self.__graphicItem = self.__scene.addPixmap(self.__p)
        self.setScene(self.__scene)
        # fit in view literally
        self.fitInView(self.__graphicItem, Qt.KeepAspectRatio)
        self.show()

        self.__sq = SelectionSquare(view=self)
        self.__sq.setRect(self.sceneRect())
        self.scene().addItem(self.__sq)

    def resizeEvent(self, e):
        if isinstance(self.__graphicItem, QGraphicsItem):
            self.fitInView(self.__graphicItem, Qt.KeepAspectRatio)