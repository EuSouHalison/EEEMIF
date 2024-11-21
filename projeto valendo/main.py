import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QMessageBox
from PyQt5.QtGui import QFont
from cadastro_alunos import CadastroAlunos
from cadastro_turmas import CadastroTurmas
from relatorios import Relatorios
from backup import Backup
from gerar_escalas import GerarEscalas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gerar Escalas')
        self.showMaximized()
        
        layout = QVBoxLayout()

        title_font = QFont('Arial', 20, QFont.Bold)
        normal_font = QFont('Arial', 12)

        label = QLabel('Bem-vindo ao Gerar Escalas', self)
        label.setFont(title_font)
        layout.addWidget(label)

        # Botões existentes
        btnCadastrarAluno = QPushButton('Cadastrar Aluno', self)
        btnCadastrarAluno.setFont(normal_font)
        btnCadastrarAluno.clicked.connect(self.abrir_cadastro_alunos)
        layout.addWidget(btnCadastrarAluno)

        btnCadastrarTurma = QPushButton('Cadastrar Turma', self)
        btnCadastrarTurma.setFont(normal_font)
        btnCadastrarTurma.clicked.connect(self.abrir_cadastro_turmas)
        layout.addWidget(btnCadastrarTurma)

        btnGerarRelatorio = QPushButton('Gerar Relatório', self)
        btnGerarRelatorio.setFont(normal_font)
        btnGerarRelatorio.clicked.connect(self.abrir_relatorios)
        layout.addWidget(btnGerarRelatorio)

        btnBackup = QPushButton('Backup', self)
        btnBackup.setFont(normal_font)
        btnBackup.clicked.connect(self.abrir_backup)
        layout.addWidget(btnBackup)

        btnGerarEscalas = QPushButton('Gerar Escalas', self)
        btnGerarEscalas.setFont(normal_font)
        btnGerarEscalas.clicked.connect(self.abrir_gerar_escalas)
        layout.addWidget(btnGerarEscalas)

        # Novo botão para excluir todos os dados
        btnExcluirDados = QPushButton('Excluir Todos os Dados', self)
        btnExcluirDados.setFont(normal_font)
        btnExcluirDados.clicked.connect(self.excluir_todos_os_dados)
        layout.addWidget(btnExcluirDados)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def abrir_cadastro_alunos(self):
        self.cadastro_alunos = CadastroAlunos()
        self.cadastro_alunos.show()

    def abrir_cadastro_turmas(self):
        self.cadastro_turmas = CadastroTurmas()
        self.cadastro_turmas.show()

    def abrir_relatorios(self):
        self.relatorios = Relatorios()
        self.relatorios.show()

    def abrir_backup(self):
        self.backup = Backup()
        self.backup.show()

    def abrir_gerar_escalas(self):
        self.gerar_escalas = GerarEscalas()
        self.gerar_escalas.show()

    def excluir_todos_os_dados(self):
        reply = QMessageBox.question(self, 'Confirmação', 
                                     "Tem certeza de que deseja excluir todos os dados?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # Lista de arquivos de dados para excluir
                arquivos_dados = ['data.json', 'used_students.json', 'escalas.json']
                for arquivo in arquivos_dados:
                    if os.path.exists(arquivo):
                        os.remove(arquivo)
                
                QMessageBox.information(self, 'Sucesso', "Todos os dados foram excluídos com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, 'Erro', f"Ocorreu um erro ao excluir os dados: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
