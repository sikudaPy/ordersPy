import base64
import json

from PySide6 import QtWidgets
from PySide6.QtCore import QUrl, Qt, QDate, QUuid
from PySide6.QtWidgets import QDialog, QDoubleSpinBox, QHeaderView, QSpinBox, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,QDateEdit,QLineEdit,QTextEdit, QComboBox
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply

from order_const import strBaseUrl, getRequestAuth

class ItemDialog(QDialog):
    def __init__(self, parent=None, network_manager=None, id=""):
        super().__init__(parent)
        self.setWindowTitle("Заказ")
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
        layoutNumberDate.addWidget(self.data_number)#, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layoutNumberDate.addWidget(QLabel("Дата:"), 0, alignment=Qt.AlignmentFlag.AlignLeft)
        layoutNumberDate.addWidget(self.data_date, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layoutNumberDate.setSpacing(5)
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

        tableLayout = QVBoxLayout()
        commandLayout = QHBoxLayout()
        addButton = QPushButton("+")
        commandLayout.addWidget(addButton,0,alignment=Qt.AlignmentFlag.AlignLeft) 
        addButton.clicked.connect(self.add_line)
        delButton = QPushButton("-")
        commandLayout.addWidget(delButton,0,alignment=Qt.AlignmentFlag.AlignLeft) 
        delButton.clicked.connect(self.del_line)
        # copyButton = QPushButton("++")
        # commandLayout.addWidget(copyButton,0,alignment=Qt.AlignmentFlag.AlignLeft) 
        # #delButton.clicked.connect(self.copy_line)
        tableLayout.addLayout(commandLayout)
        commandLayout.addStretch()
        tableLayout.addWidget(self.table)
        tableLayout.setSpacing(0)
        layout.addLayout(tableLayout)

        #buttons       
        layoutButtons = QHBoxLayout()
        self.write_btn = QPushButton("Записать")
        layoutButtons.addWidget(self.write_btn, alignment= Qt.AlignmentFlag.AlignLeft)
        self.write_btn.clicked.connect(self.write)
        self.close_btn = QPushButton("Закрыть")
        layoutButtons.addWidget(self.close_btn, alignment= Qt.AlignmentFlag.AlignHCenter)
        self.close_btn.clicked.connect(self.close)
        self.del_btn = QPushButton("Удалить")
        layoutButtons.addWidget(self.del_btn, alignment= Qt.AlignmentFlag.AlignRight)
        self.del_btn.clicked.connect(self.delete)
        layout.addLayout(layoutButtons)

        self.setLayout(layout)
        #if id != "":
        self.start_request(id)
        self.setMinimumWidth(600)   

    def start_request(self, id):

        request = getRequestAuth(id+"/?format=json")
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
            self.asrt_list = data["all_assortment"].copy()
            for item in table:
                asrt_combo = QComboBox()
                for asrt in self.asrt_list: #data["all_assortment"]:
                    asrt_combo.addItem(asrt['name'], userData=QUuid(asrt['uuid']))
                asrt_uuid = QUuid("{"+item["assortment"]+"}")
                index_asrt = asrt_combo.findData(asrt_uuid)
                if index_asrt != -1:
                    asrt_combo.setCurrentIndex(index_asrt)
                self.table.setCellWidget(index, 0, asrt_combo)

                itemCount = QSpinBox(minimum=0, maximum=100000000,value=int(item["count"]))
                self.table.setCellWidget(index, 1, itemCount)
                itemCount.setAlignment(Qt.AlignmentFlag.AlignRight)
                itemCount.valueChanged.connect(self.count_change)
                
                itemPrice = QDoubleSpinBox(minimum=0, maximum=100000000,value=float(item["price"]))
                self.table.setCellWidget(index, 2, itemPrice)
                itemPrice.setAlignment(Qt.AlignmentFlag.AlignRight)
                itemPrice.valueChanged.connect(self.price_change)

                itemSumma = QDoubleSpinBox(minimum=0, maximum=100000000,value=float(item["summa"]))
                self.table.setCellWidget(index, 3, itemSumma)
                itemSumma.setAlignment(Qt.AlignmentFlag.AlignRight)
                itemSumma.valueChanged.connect(self.summa_change)
                index = index + 1

            self.table.resizeColumnToContents(0)
        else:
            # Обработка ошибки
            error_str = self.reply.errorString()
            self.layout().addWidget(QLabel(error_str))   

        self.reply.deleteLater()

    #edit line
    def count_change(self, cnt):
        row = self.table.currentRow()
        if row >= 0:
            price = float(self.table.cellWidget(row, 2).text().replace(",", "."))
            self.table.cellWidget(row, 3).setValue(cnt*price)    

    def price_change(self, price):
        row = self.table.currentRow()
        if row >= 0:
            cnt = float(self.table.cellWidget(row, 1).text().replace(",", "."))
            self.table.cellWidget(row, 3).setValue(cnt*price) 

    def summa_change(self, sum):
        row = self.table.currentRow()
        if row >= 0:
            cnt = float(self.table.cellWidget(row, 1).text().replace(",", "."))
            if cnt !=0:
                self.table.cellWidget(row, 2).setValue(sum/cnt)           

    #add line
    def add_line(self):
        index = self.table.rowCount()
        self.table.insertRow(index)
        asrt_combo = QComboBox()
        for asrt in self.asrt_list: 
            asrt_combo.addItem(asrt['name'], userData=QUuid(asrt['uuid']))
        self.table.setCellWidget(index, 0, asrt_combo)

        itemCount = QSpinBox(minimum=0, maximum=100000000,value=0)
        self.table.setCellWidget(index, 1, itemCount)
        itemCount.setAlignment(Qt.AlignmentFlag.AlignRight)
                
        itemPrice = QDoubleSpinBox(minimum=0, maximum=100000000,value=0)
        self.table.setCellWidget(index, 2, itemPrice)
        itemPrice.setAlignment(Qt.AlignmentFlag.AlignRight)

        itemPrice = QDoubleSpinBox(minimum=0, maximum=100000000,value=0)
        self.table.setCellWidget(index, 3, itemPrice)
        itemPrice.setAlignment(Qt.AlignmentFlag.AlignRight)


    def del_line(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)  

    def write(self):
        request = getRequestAuth(self.id+"/?format=json")
        #table lines
        table = []
        summa = 0
        for index in range(self.table.rowCount()):            
            asrt_combo = self.table.cellWidget(index, 0)
            json_line = {
                "num": 0,
                "assortment": asrt_combo.itemData(self.data_org.currentIndex()).toString(),
                "count": self.table.cellWidget(index, 1).text().replace(",", "."),
                "price": self.table.cellWidget(index, 2).text().replace(",", "."),
                "summa": self.table.cellWidget(index, 3).text().replace(",", "."),    
            }
            summa += float(self.table.cellWidget(index, 3).text().replace(",", "."))
            table.append(json_line)
            index = index + 1        

        json_data = { "uuid": str(self.id),
          "number": self.data_number.text(), 
          "date": self.data_date.date().toString("yyyy-MM-dd"),
          "organization": self.data_org.itemData(self.data_org.currentIndex()).toString(),
          "comment": self.data_comment.toPlainText(),
          "summa": str(summa),
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
        request = getRequestAuth(self.id+"/?format=json")  
        self.network_manager.deleteResource(request)
        self.close()
        self.parent().del_item(self.id) 
