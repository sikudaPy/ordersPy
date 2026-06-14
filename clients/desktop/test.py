import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLineEdit

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 1. Текстовое поле
        self.line_edit = QLineEdit()
        
        # 2. Выпадающий список
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Элемент 1", "Элемент 2", "Элемент 3"])

        # Связываем выбор из списка с заполнением QLineEdit
        self.combo_box.currentTextChanged.connect(self.line_edit.setText)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.combo_box)
        
        self.setLayout(layout)
        self.setWindowTitle('Выбор из списка')
        self.show()

app = QApplication(sys.argv)
ex = MyApp()
sys.exit(app.exec())
