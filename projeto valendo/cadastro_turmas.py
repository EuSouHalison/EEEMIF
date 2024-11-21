import json
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QFileDialog, QListWidget, QInputDialog, QListWidgetItem, QMenu, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPoint

class CadastroTurmas(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data = self.load_data()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('Cadastrar Turma', self)
        font = QFont('Arial', 14, QFont.Bold)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.nome = QLineEdit(self)
        self.nome.setPlaceholderText('Nome da Turma')
        self.nome.setFont(QFont('Arial', 12))
        layout.addWidget(self.nome)

        self.btnSalvar = QPushButton('Salvar', self)
        self.btnSalvar.setFont(QFont('Arial', 12))
        self.btnSalvar.clicked.connect(self.salvarTurma)
        layout.addWidget(self.btnSalvar)

        self.btnImportar = QPushButton('Importar Lista de Turmas')
        self.btnImportar.setFont(QFont('Arial', 12))
        self.btnImportar.clicked.connect(self.importarTurmas)
        layout.addWidget(self.btnImportar)

        self.btnVisualizar = QPushButton('Visualizar Turmas')
        self.btnVisualizar.setFont(QFont('Arial', 12))
        self.btnVisualizar.clicked.connect(self.visualizarTurmas)
        layout.addWidget(self.btnVisualizar)

        self.btnCancelar = QPushButton('Cancelar', self)
        self.btnCancelar.setFont(QFont('Arial', 12))
        self.btnCancelar.clicked.connect(self.close)
        layout.addWidget(self.btnCancelar)

        self.listaTurmas = QListWidget()
        self.listaTurmas.setSelectionMode(QListWidget.MultiSelection)
        self.listaTurmas.setFont(QFont('Arial', 12))
        self.listaTurmas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listaTurmas.customContextMenuRequested.connect(self.mostrarMenuContexto)
        layout.addWidget(self.listaTurmas)

        self.setLayout(layout)

    def salvarTurma(self):
        nome = self.nome.text()
        if nome:
            self.data['turmas'].append({'nome': nome, 'alunos': []})
            self.save_data()
            self.nome.clear()
            self.visualizarTurmas()

    def importarTurmas(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Selecionar Arquivo', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    nome_turma = line.strip()
                    if nome_turma:
                        self.data['turmas'].append({'nome': nome_turma, 'alunos': []})
            self.save_data()
            self.visualizarTurmas()

    def visualizarTurmas(self):
        self.listaTurmas.clear()
        for turma in self.data['turmas']:
            item = QListWidgetItem(f"{turma['nome']} ({len(turma['alunos'])} alunos)")
            self.listaTurmas.addItem(item)

    def excluirTurmas(self):
        itens_selecionados = self.listaTurmas.selectedItems()
        if itens_selecionados:
            for item in itens_selecionados:
                turma_nome = item.text().split(' (')[0]  # Separar nome da turma da contagem de alunos
                self.data['turmas'] = [turma for turma in self.data['turmas'] if turma['nome'] != turma_nome]
            self.save_data()
            self.visualizarTurmas()

    def editarTurma(self):
        item = self.listaTurmas.currentItem()
        if item:
            nome_novo, ok = QInputDialog.getText(self, "Editar Turma", "Novo nome da turma:", QLineEdit.Normal, item.text().split(' (')[0])
            if ok and nome_novo:
                for turma in self.data['turmas']:
                    if turma['nome'] == item.text().split(' (')[0]:
                        turma['nome'] = nome_novo
                        break
        self.save_data()
        self.visualizarTurmas()

    def mostrarMenuContexto(self, pos):
        menu = QMenu(self)
        excluir_action = menu.addAction("Excluir")
        editar_action = menu.addAction("Editar")
        
        action = menu.exec_(self.listaTurmas.mapToGlobal(pos))
        if action == excluir_action:
            self.excluirTurmas()
        elif action == editar_action:
            self.editarTurma()

    def load_data(self):
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {'turmas': []}

    def save_data(self):
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
