import json
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QFileDialog, QListWidget, QComboBox, QInputDialog, QListWidgetItem, QMenu, QToolTip, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CadastroAlunos(QWidget):
    def __init__(self):
        super().__init__()
        self.data = self.load_data()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('Cadastrar Aluno', self)
        font = QFont('Arial', 14, QFont.Bold)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.comboTurmas = QComboBox(self)
        self.comboTurmas.setFont(QFont('Arial', 12))
        self.carregar_turmas()
        layout.addWidget(self.comboTurmas)

        self.nome = QLineEdit(self)
        self.nome.setPlaceholderText('Nome do Aluno')
        self.nome.setFont(QFont('Arial', 12))
        layout.addWidget(self.nome)

        self.btnSalvar = QPushButton('Salvar', self)
        self.btnSalvar.setFont(QFont('Arial', 12))
        self.btnSalvar.clicked.connect(self.salvarAluno)
        layout.addWidget(self.btnSalvar)

        self.btnImportar = QPushButton('Importar Lista de Alunos')
        self.btnImportar.setFont(QFont('Arial', 12))
        self.btnImportar.setToolTip('Permite importar uma lista de alunos')
        self.btnImportar.clicked.connect(self.abrirJanelaImportar)
        layout.addWidget(self.btnImportar)

        self.btnVisualizar = QPushButton('Visualizar Alunos')
        self.btnVisualizar.setFont(QFont('Arial', 12))
        self.btnVisualizar.clicked.connect(self.visualizarAlunos)
        layout.addWidget(self.btnVisualizar)

        self.btnCancelar = QPushButton('Cancelar', self)
        self.btnCancelar.setFont(QFont('Arial', 12))
        self.btnCancelar.clicked.connect(self.close)
        layout.addWidget(self.btnCancelar)

        self.listaAlunos = QListWidget()
        self.listaAlunos.setSelectionMode(QListWidget.MultiSelection)
        self.listaAlunos.setFont(QFont('Arial', 12))
        self.listaAlunos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listaAlunos.customContextMenuRequested.connect(self.mostrarMenuContexto)
        layout.addWidget(self.listaAlunos)

        self.setLayout(layout)

    def carregar_turmas(self):
        for turma in self.data['turmas']:
            self.comboTurmas.addItem(turma['nome'])

    def salvarAluno(self):
        nome = self.nome.text()
        turma_nome = self.comboTurmas.currentText()
        if nome and turma_nome:
            for turma in self.data['turmas']:
                if turma['nome'] == turma_nome:
                    turma['alunos'].append(nome)
                    break
            self.save_data()
            self.nome.clear()
            self.visualizarAlunos()

    def abrirJanelaImportar(self):
        self.janelaImportar = JanelaImportar(self.data)
        self.janelaImportar.exec_()
        self.save_data()  # Salvar dados após importação

    def visualizarAlunos(self):
        self.listaAlunos.clear()
        turma_nome = self.comboTurmas.currentText()
        for turma in self.data['turmas']:
            if turma['nome'] == turma_nome:
                for aluno in turma['alunos']:
                    item = QListWidgetItem(aluno)
                    self.listaAlunos.addItem(item)

    def excluirAlunos(self):
        itens_selecionados = self.listaAlunos.selectedItems()
        turma_nome = self.comboTurmas.currentText()
        if itens_selecionados and turma_nome:
            for item in itens_selecionados:
                aluno_nome = item.text()
                for turma in self.data['turmas']:
                    if turma['nome'] == turma_nome:
                        turma['alunos'] = [aluno for aluno in turma['alunos'] if aluno != aluno_nome]
            self.save_data()
            self.visualizarAlunos()

    def editarAluno(self):
        item = self.listaAlunos.currentItem()
        turma_nome = self.comboTurmas.currentText()
        if item and turma_nome:
            nome_novo, ok = QInputDialog.getText(self, "Editar Aluno", "Novo nome do aluno:", QLineEdit.Normal, item.text())
            if ok and nome_novo:
                for turma in self.data['turmas']:
                    if turma['nome'] == turma_nome:
                        for i, aluno in enumerate(turma['alunos']):
                            if aluno == item.text():
                                turma['alunos'][i] = nome_novo
                                break
            self.save_data()
            self.visualizarAlunos()

    def mostrarMenuContexto(self, pos):
        menu = QMenu(self)
        excluir_action = menu.addAction("Excluir")
        editar_action = menu.addAction("Editar")
        
        action = menu.exec_(self.listaAlunos.mapToGlobal(pos))
        if action == excluir_action:
            self.excluirAlunos()
        elif action == editar_action:
            self.editarAluno()

    def load_data(self):
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {'turmas': []}

    def save_data(self):
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

class JanelaImportar(QDialog):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('Importar Lista de Alunos', self)
        self.label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(self.label)

        self.comboTurmas = QComboBox(self)
        self.comboTurmas.setFont(QFont('Arial', 12))
        self.carregar_turmas()
        layout.addWidget(self.comboTurmas)

        self.btnSelecionarArquivo = QPushButton('Selecionar Arquivo', self)
        self.btnSelecionarArquivo.setFont(QFont('Arial', 12))
        self.btnSelecionarArquivo.clicked.connect(self.selecionarArquivo)
        layout.addWidget(self.btnSelecionarArquivo)

        self.btnSalvar = QPushButton('Salvar', self)
        self.btnSalvar.setFont(QFont('Arial', 12))
        self.btnSalvar.clicked.connect(self.salvar)
        layout.addWidget(self.btnSalvar)

        self.btnCancelar = QPushButton('Cancelar', self)
        self.btnCancelar.setFont(QFont('Arial', 12))
        self.btnCancelar.clicked.connect(self.close)
        layout.addWidget(self.btnCancelar)

        self.setLayout(layout)

    def carregar_turmas(self):
        for turma in self.data['turmas']:
            self.comboTurmas.addItem(turma['nome'])

    def selecionarArquivo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Selecionar Arquivo', '', 'Text Files (*.txt);;PDF Files (*.pdf);;Doc Files (*.doc *.docx)')
        self.file_path = file_path

    def salvar(self):
        turma_nome = self.comboTurmas.currentText()
        if self.file_path and turma_nome:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    aluno_nome = line.strip()
                    if aluno_nome:
                        for turma in self.data['turmas']:
                            if turma['nome'] == turma_nome:
                                turma['alunos'].append(aluno_nome)
                                break
        self.close()
