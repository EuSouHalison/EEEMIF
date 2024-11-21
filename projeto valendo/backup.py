import os
import shutil
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QWidget, QFileDialog
from PyQt5.QtGui import QFont

class Backup(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('Backup de Dados', self)
        self.label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(self.label)

        self.btnCriarBackup = QPushButton('Criar Backup', self)
        self.btnCriarBackup.clicked.connect(self.criar_backup)
        layout.addWidget(self.btnCriarBackup)

        self.setLayout(layout)

    def criar_backup(self):
        destino = QFileDialog.getExistingDirectory(self, "Selecionar Diretório de Backup")
        if destino:
            if not os.path.exists(destino):
                os.makedirs(destino)
            shutil.copy("escalas.db", os.path.join(destino, "backup"))
