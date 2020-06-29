import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QMainWindow, QCheckBox, QStylePainter
from PyQt5.QtGui import QIcon, QBrush
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QAbstractTableModel, Qt, QModelIndex, QVariant

from PostgreSQLHelper import PostgreSQLHelper

qt_creator_file = "ws.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class TableModel(QAbstractTableModel):
    def __init__(self, data_from_db=None, headers=None):
        super(TableModel, self).__init__()
        self.data_from_db = data_from_db or []
        self.headers = headers

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        col = index.column()
        if role == Qt.DisplayRole:
            return self.data_from_db[row][col]
        elif role == Qt.CheckStateRole:
            if self.headers[col] == 'Available':
                if self.data_from_db[row][col]:
                    return Qt.Checked
                else:
                    return Qt.Unchecked
        elif role == Qt.BackgroundColorRole:
            if self.headers[col] == 'Available':
                if self.data_from_db[row][col]:
                    return QBrush(Qt.green)
                else:
                    return QBrush(Qt.red)

    def rowCount(self, index):
        if isinstance(self.data_from_db, list):
            if len(self.data_from_db) == 0:
                return 0
            else:
                if isinstance(self.data_from_db[0], list):
                    return len(self.data_from_db)
                else:
                    return len([self.data_from_db]) - 1

    def columnCount(self, index):
        if len(self.data_from_db) == 0:
            return 0
        else:
            if isinstance(self.data_from_db[0], list):
                return len(self.data_from_db[0])
            else:
                return len(self.data_from_db) - 1

    def headerData(self, section: int, orientation: Qt.Orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]

    def flags(self, index: QModelIndex):
        row = index.row()
        col = index.column()
        original_flags = super(TableModel, self).flags(index)
        if self.headers[col] == 'Available':
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index: QModelIndex, value, role):
        row = index.row()
        col = index.column()
        if role == Qt.CheckStateRole and self.headers[col] == 'Available':
            if value == Qt.Checked:
                self.data_from_db[row][col] = True
            elif value == Qt.Unchecked:
                self.data_from_db[row][col] = False
        return True


class Manager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Manager, self).__init__()
        self.setupUi(self)
        self.model = TableModel()

        self.table_data = [list(record) for record in PostgreSQLHelper.get_table('equipment')]
        self.headers = PostgreSQLHelper.get_columns('equipment')

        self.model.data_from_db = self.table_data
        self.model.headers = self.headers

        self.wsView.setModel(self.model)
        self.interface()

    def interface(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))

        self.setWindowTitle('WS Equipment Managment System')
        self.show()


def window():
    app = QApplication(sys.argv)
    window = Manager()
    app.setWindowIcon(QIcon('windsurfing-icon.png'))
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
