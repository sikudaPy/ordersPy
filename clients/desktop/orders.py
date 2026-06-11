import sys, json
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHeaderView, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout,QLineEdit,QTextEdit, QMessageBox
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl

class ItemDialog(QDialog):
    def __init__(self, network_manager, id):
        super().__init__()
        self.setWindowTitle("Пословица")
        self.network_manager = network_manager
        
        # Create a layout to hold widgets
        layout = QVBoxLayout()
        layoutNumber = QHBoxLayout()
        self.data_number = QLineEdit("")
        self.data_date = QLineEdit("")
        layoutNumber.addWidget(QLabel("Номер:"))
        layoutNumber.addWidget(self.data_number)
        layoutNumber.addWidget(QLabel("Дата:"))
        layoutNumber.addWidget(self.data_date)
        layout.addLayout(layoutNumber)

        #organization
        layoutOrg = QHBoxLayout()
        layoutOrg.addWidget( QLabel("Организация"))
        self.data_org = QLineEdit("")
        layoutOrg.addWidget( self.data_org)
        layout.addLayout(layoutOrg)

        #comment
        layout.addWidget( QLabel("Комментарий"))
        self.data_comment = QTextEdit("")
        self.data_comment.setPlaceholderText("Введите многострочный текст здесь...")
        self.data_comment.setMaximumHeight(48)
        layout.addWidget( self.data_comment)
        
        self.table = QtWidgets.QTableView()
        layout.addWidget( self.table)

        #buttons       
        layoutButtons = QHBoxLayout()
        self.close_btn = QPushButton("Закрыть")
        layoutButtons.addWidget(self.close_btn, alignment= Qt.AlignmentFlag.AlignRight)
        self.close_btn.clicked.connect(self.reject)
        layout.addLayout(layoutButtons)

        self.setLayout(layout)
        self.start_request(id)

    def start_request(self, id):
              
        url = QUrl("https://d1.www-1c.ru/orders-api/"+id+"/?format=json")
        request = QNetworkRequest(url)
        self.reply = self.network_manager.get(request)
        self.reply.finished.connect(self.handle_response)

    def handle_response(self):
        if self.reply.error() == QNetworkReply.NetworkError.NoError:
            # Читаем данные
            text = self.reply.readAll().data().decode("utf-8")
            data = json.loads(text);
            self.data_number.setText(data["number"])
            self.data_date.setText(data["date"])
            self.data_org.setText(data["org_name"])
            self.data_comment.setText(data["comment"])
        else:
            # Обработка ошибки
            error_str = self.reply.errorString()
            self.label.setText(error_str)
            
        self.reply.deleteLater()

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
        return 5 #len(self._data)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заказы")
        self._file_menu = self.menuBar().addMenu("&File")

        self.table = QtWidgets.QTableView()

        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.findLayout = QHBoxLayout()
        self.verticalLayout.insertLayout(0, self.findLayout)
        self.findText = QLineEdit()
        self.findText.setPlaceholderText(" Find text in table ")
        self.findLayout.addWidget(self.findText, stretch=100, alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)
        self.findButton = QPushButton(" Find... ")
        self.findLayout.addWidget(self.findButton, stretch=10, alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)
        self.findButton.clicked.connect(self.find)

        self.verticalLayout.addWidget(self.table)
        self.setCentralWidget(self.centralwidget)

        # Инициализация менеджера сети
        self.network_manager = QNetworkAccessManager(self)
        self.start_request()

    def start_request(self):
              
        #url = QUrl("https://python1c.ru/catalogs/api?format=json")
        url = QUrl("https://d1.www-1c.ru/orders-api/?format=json")
        request = QNetworkRequest(url)
                
        # Отправляем GET запрос
        self.reply = self.network_manager.get(request)
        
        # Подключаем сигнал завершения
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
        #self.table.resizeColumnToContents(3)
        self.table.resizeColumnToContents(4)
        #self.table.setColumnWidth(1, 600)
        self.table.clicked.connect(self.show_item)

    def show_item(self, index):

        model = self.table.model()
        indexRec  = model.index(index.row(), 0)
        indexTitle = model.index(index.row(), 1)
        id = model.data(indexRec, Qt.EditRole)
        dialog = ItemDialog(self.network_manager, id)
        dialog.exec()

    # @Slot()
    def find(self):
        findString = self.findText.text()
        dlg = QMessageBox(self)
        dlg.setWindowTitle(self.tr("Заказ"))
        dlg.setText(self.tr("text: '"+findString+"' будет найден"))
        dlg.exec()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setMinimumWidth(1024)
window.setMinimumHeight(768)
window.show()
app.exec()    