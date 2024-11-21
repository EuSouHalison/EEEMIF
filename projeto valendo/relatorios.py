from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget
import matplotlib.pyplot as plt
from database import connect

class Relatorios(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('Relatórios', self)
        self.label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(self.label)

        self.btnGerar = QPushButton('Gerar Relatório', self)
        self.btnGerar.clicked.connect(self.gerarRelatorio)
        layout.addWidget(self.btnGerar)

        self.setLayout(layout)

    def gerarRelatorio(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT turma_id, COUNT(*) FROM alunos GROUP BY turma_id")
        turmas = cursor.fetchall()
        conn.close()

        # Gerar gráfico
        turma_ids = [turma[0] for turma in turmas]
        qtd_alunos = [turma[1] for turma in turmas]

        plt.bar(turma_ids, qtd_alunos)
        plt.xlabel('Turmas')
        plt.ylabel('Número de Alunos')
        plt.title('Distribuição de Alunos por Turma')
        plt.show()
