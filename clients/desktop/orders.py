import base64
import sys, json
import uuid
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QByteArray, QModelIndex, Qt, QDate, QUuid
from PySide6.QtWidgets import QDialog, QHeaderView, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout,QDateEdit,QLineEdit,QTextEdit, QMessageBox, QComboBox
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl

#local for test
credentials = "admin:impimp13"
strBaseUrl = "http://127.0.0.1:8000/orders-api/" 
# strBaseUrl = "https://orders.python1c.ru/orders-api/"

class ItemDialog(QDialog):
    def __init__(self, parent=None, network_manager=None, id=""):
        super().__init__(parent)
        self.setWindowTitle("Пословица")
        self.network_manager = network_manager
        self.id = id
        
        # Create a layout to hold widgets
        layout = QVBoxLayout()
        
        self.data_number = QLineEdit("")
        self.data_number.setMaximumWidth(100)
        self.data_date = QDateEdit()
        self.data_date.setCalendarPopup(True)
        self.data_date.setDisplayFormat("dd.MM.yyyy")

        layoutNumberDate = QHBoxLayout()
        layoutNumberDate.addWidget(QLabel("Номер:"), 0, alignment=Qt.AlignmentFlag.AlignLeft)
        layoutNumberDate.addStretch()
        layoutNumberDate.addWidget(self.data_number)#, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layoutNumberDate.addWidget(QLabel("Дата:"), 0, alignment=Qt.AlignmentFlag.AlignLeft)
        layoutNumberDate.addWidget(self.data_date, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(layoutNumberDate)

        #organization
        layoutOrg = QHBoxLayout()
        layoutOrg.addWidget( QLabel("Организация"), 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.data_org = QComboBox()
        self.data_org.setMinimumWidth(300)
        layoutOrg.addWidget( self.data_org, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(layoutOrg)

        #comment
        layout.addWidget( QLabel("Комментарий"))
        self.data_comment = QTextEdit("")
        self.data_comment.setPlaceholderText("Введите многострочный текст здесь...")
        self.data_comment.setMaximumHeight(48)
        layout.addWidget( self.data_comment)
        
        self.table = QtWidgets.QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(["Ассортимент", "Количество","Цена","Сумма"])
        header = self.table.horizontalHeader()    
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        layout.addWidget(self.table)

        #buttons       
        layoutButtons = QHBoxLayout()
        self.write_btn = QPushButton("Записать")
        layoutButtons.addWidget(self.write_btn, alignment= Qt.AlignmentFlag.AlignLeft)
        self.write_btn.clicked.connect(self.write)
        self.close_btn = QPushButton("Закрыть")
        layoutButtons.addWidget(self.close_btn, alignment= Qt.AlignmentFlag.AlignRight)
        self.close_btn.clicked.connect(self.close)
        self.del_btn = QPushButton("Удалить")
        layoutButtons.addWidget(self.del_btn, alignment= Qt.AlignmentFlag.AlignRight)
        self.del_btn.clicked.connect(self.delete)
        layout.addLayout(layoutButtons)

        self.setLayout(layout)
        if id != "":
            self.start_request(id)
        self.setMinimumWidth(600)

    # def closeEvent(self, event):
    #     parent = self.parentWidget()
    #     if parent:
    #         parent.start_request()
            
    #     # Allow the dialog to close normally
    #     event.accept()    

    def start_request(self, id):

        url = QUrl(strBaseUrl+id+"/?format=json")      
        request = QNetworkRequest(url)
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        request.setRawHeader(b"Authorization", f"Basic {encoded_credentials}".encode('utf-8'))
        self.reply = self.network_manager.get(request)
        self.reply.finished.connect(self.handle_response)

    def handle_response(self):
        if self.reply.error() == QNetworkReply.NetworkError.NoError:
            # Читаем данные
            text = self.reply.readAll().data().decode("utf-8")
            data = json.loads(text);
            self.data_number.setText(data["number"])
            self.data_date.setDate(QDate.fromString(data["date"], "yyyy-MM-dd"))
            for item in data["all_organizations"]:
                self.data_org.addItem(item['name'], userData=QUuid(item['uuid']))
            if data["organization"]:    
                org_uuid = QUuid("{"+data["organization"]+"}")
                index = self.data_org.findData(org_uuid)
                if index != -1:
                    self.data_org.setCurrentIndex(index)
    
            self.data_comment.setText(data["comment"])
            table = data["table"]
            self.table.setRowCount(len(table))
            index = 0
            for item in table:
                asrt_combo = QComboBox()
                for asrt in data["all_assortment"]:
                    asrt_combo.addItem(asrt['name'], userData=QUuid(asrt['uuid']))
                asrt_uuid = QUuid("{"+item["assortment"]+"}")
                index_asrt = asrt_combo.findData(asrt_uuid)
                if index_asrt != -1:
                    asrt_combo.setCurrentIndex(index_asrt)
                self.table.setCellWidget(index, 0, asrt_combo)

                itemCount = QtWidgets.QTableWidgetItem(item["count"])
                itemCount.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
                self.table.setItem(index, 1, itemCount)
                itemPrice = QtWidgets.QTableWidgetItem(item["price"])
                itemPrice.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
                self.table.setItem(index, 2, itemPrice)
                itemCount = QtWidgets.QTableWidgetItem(item["summa"])
                itemCount.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
                self.table.setItem(index, 3, itemCount)
                index = index + 1

            self.table.resizeColumnToContents(0)
        else:
            # Обработка ошибки
            error_str = self.reply.errorString()
            self.layout().addWidget(QLabel(error_str))   

        self.reply.deleteLater()

    def write(self):
        if self.id == "":
            url = QUrl(strBaseUrl+self.id+"/?format=json") 
        else:    
            url = QUrl(strBaseUrl+self.id+"/?format=json")      
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        request.setRawHeader(b"Authorization", f"Basic {encoded_credentials}".encode('utf-8'))

        #table lines
        table = []
        for index in range(self.table.rowCount()):            
            asrt_combo = self.table.cellWidget(index, 0)
            json_line = {
                "num": 0,
                "assortment": asrt_combo.itemData(self.data_org.currentIndex()).toString(),
                "count": self.table.item(index, 1).text(),
                "price": self.table.item(index, 2).text(),
                "summa": self.table.item(index, 3).text(),    
            }
            table.append(json_line)
            index = index + 1        

        json_data = { "uuid": str(self.id),
          "number": self.data_number.text(), 
          "date": self.data_date.date().toString("yyyy-MM-dd"),
          "organization": self.data_org.itemData(self.data_org.currentIndex()).toString(),
          "comment": self.data_comment.toPlainText(),
          "summa": "0.00",
          "table": table
        }
        json_string = json.dumps(json_data)
        if self.id == "":#do not used
            self.network_manager.post(request, json_string.encode('utf-8'))
        else:       
            self.network_manager.put(request, json_string.encode('utf-8'))
 
        self.close() 
        self.parent().set_item(json_data)        

    def delete(self):   
        url = QUrl(strBaseUrl+self.id+"/?format=json")      
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        request.setRawHeader(b"Authorization", f"Basic {encoded_credentials}".encode('utf-8'))
        self.network_manager.deleteResource(request)
        self.close()
        self.parent().del_item(self.id) 

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

        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.findLayout = QHBoxLayout()
        self.verticalLayout.insertLayout(0, self.findLayout)
        self.findLayout.addWidget(QLabel("Список заказов"), stretch=0, alignment=Qt.AlignmentFlag.AlignBaseline|Qt.AlignmentFlag.AlignLeft)
        self.createButton = QPushButton("Create")
        self.findLayout.addWidget(self.createButton, stretch=0, alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)
        self.createButton.clicked.connect(self.create_item)
        self.findText = QLineEdit()
        self.findText.setPlaceholderText(" Find text in table ")
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
              
        url = QUrl(strBaseUrl+"?format=json&strFind="+self.findText.text())
        request = QNetworkRequest(url)      
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        request.setRawHeader(b"Authorization", f"Basic {encoded_credentials}".encode('utf-8'))

        # Отправляем GET запрос
        self.reply = self.network_manager.get(request) #, jsonString)
        
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
        # findString = self.findText.text()
        self.start_request()
        # dlg = QMessageBox(self)
        # dlg.setWindowTitle(self.tr("Заказ"))
        # dlg.setText(self.tr("text: '"+findString+"' будет найден"))
        # dlg.exec()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setMinimumWidth(800)
window.setMinimumHeight(600)
window.show()
app.exec()    