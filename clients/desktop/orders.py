import sys, json

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import  QModelIndex, Qt
from PySide6.QtWidgets import QHeaderView, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout,QDateEdit,QLineEdit,QTextEdit, QMessageBox, QComboBox
from PySide6.QtNetwork import QNetworkAccessManager,  QNetworkReply

from order_const import strBaseUrl, getRequestAuth
from order_item import ItemDialog


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.catalogs = json.loads(data)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            match section:
                case 0:
                    return "Номер"
                case 1:
                    return "Дата"
                case 2:
                    return "Организация"
                case 3:
                    return "Комментарий"
                case 4:
                    return "Сумма"
                case _:
                    return ""
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # index.row() индексирует по внешнему списку, index.column() — по подсписку
            match index.column(): 
                case 0:
                    return self.catalogs[index.row()]["number"]
                case 1: 
                    return self.catalogs[index.row()]["date"]
                case 2:
                    return self.catalogs[index.row()]["org_name"]
                case 3:
                    return self.catalogs[index.row()]["comment"]
                case 4:
                    return self.catalogs[index.row()]["summa"]
                case _:
                    return ""
        elif role == Qt. EditRole:
            match index.column(): 
                case 0:
                    return self.catalogs[index.row()]["uuid"]
                case 1:
                    return self.catalogs[index.row()]["number"]
                case 2: 
                    return self.catalogs[index.row()]["date"]
                case 3:
                    return self.catalogs[index.row()]["organization"]
                case 4:
                    return self.catalogs[index.row()]["comment"]
                case 5:
                    return self.catalogs[index.row()]["summa"]
                case _:
                    return "" 

        if role == Qt.ItemDataRole.TextAlignmentRole and index.column() == 4:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter                                      

    def rowCount(self, index):
        return len(self.catalogs)

    def columnCount(self, index):
        return 5 

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заказы")
        self._file_menu = self.menuBar().addMenu("&File")

        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.findLayout = QHBoxLayout()
        self.verticalLayout.insertLayout(0, self.findLayout)
        self.findLayout.addWidget(QLabel("Список заказов"), stretch=0, alignment=Qt.AlignmentFlag.AlignBaseline|Qt.AlignmentFlag.AlignLeft)
        self.createButton = QPushButton("Добавить")
        self.findLayout.addWidget(self.createButton, stretch=0, alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        self.createButton.clicked.connect(self.create_item)
        self.findText = QLineEdit()
        self.findText.setPlaceholderText(" Найти текст в таблице ")
        self.findText.setMinimumWidth(500)
        self.findLayout.addWidget(self.findText, stretch=1, alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)
        self.findText.editingFinished.connect(self.find)

        self.table = QtWidgets.QTableView()
        self.verticalLayout.addWidget(self.table)
        self.setCentralWidget(self.centralwidget)

        # Инициализация менеджера сети
        self.network_manager = QNetworkAccessManager(self)
        self.start_request()

    def start_request(self):

        request = getRequestAuth("?format=json&strFind="+self.findText.text())     
        self.reply = self.network_manager.get(request) #, jsonString)
        self.reply.finished.connect(self.handle_response)

    def handle_response(self):
        if self.reply.error() == QNetworkReply.NetworkError.NoError:
            # Читаем данные
            str_catalog = self.reply.readAll().data().decode("utf-8")
            self.table.setModel(TableModel(str_catalog))
        else:
            # Обработка ошибки
            error_str = self.reply.errorString()
            str_catalog = '[{"id":""7e4a9356-949f-484b-bbdc-51966604afff"","number":"0001","date":"-","organization":"","comment":"","summa"="0.0"}]'
            self.table.setModel(TableModel(str_catalog))
            
        self.reply.deleteLater()
     
        self.table.setAlternatingRowColors(True)
        self.table.resizeColumnToContents(0)
        self.table.resizeColumnToContents(1)
        self.table.resizeColumnToContents(2)
        header = self.table.horizontalHeader()    
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.resizeColumnToContents(4)
        #self.table.setColumnWidth(1, 600)
        self.table.clicked.connect(self.show_item)

    # @Slot()
    def create_item(self):
        dialog = ItemDialog(self, self.network_manager, "new")
        dialog.exec()

    def show_item(self, index):
        model = self.table.model()
        indexRec  = model.index(index.row(), 0)
        #indexTitle = model.index(index.row(), 1)
        id = model.data(indexRec, Qt.EditRole)
        dialog = ItemDialog(self, self.network_manager, id)
        dialog.exec()

    def del_item(self, uuid):        
            model = self.table.model()
            for row, item in enumerate(model.catalogs,start=0):
                if item["uuid"] == uuid:
                    model.beginRemoveRows(QModelIndex(),row,row)
                    model.catalogs.remove(item) 
                    model.endRemoveRows() 
                    break

    def set_item(self, json_data): 
        model = self.table.model()
        for item in model.catalogs:
            if item["uuid"] == json_data["uuid"]:
                item.update(json_data)
                break
        self.table.update               

    # @Slot()
    def find(self):
        self.start_request()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setMinimumWidth(800)
window.setMinimumHeight(600)
window.show()
app.exec()    