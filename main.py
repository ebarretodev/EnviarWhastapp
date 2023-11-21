# usado para interface gráfica
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QLineEdit, QPlainTextEdit, QSplashScreen, QDesktopWidget, QProgressBar
from PyQt5.uic import loadUi
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
# from PyQt5 import uic

# GUI FILE
from screen import Ui_MainWindow
from splash import Ui_Form

import sys
import file_rc

# usado para controle dos arquivos
import pandas as pd

# usado para fazer pausas no programa
import time

# usado para controlar o navegador
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib

# classe para conectar em paralelo
class WorkerConnectZap(QObject):
    finished = pyqtSignal()

    def __init__(self, navegador):
        super(WorkerConnectZap, self).__init__()
        self.navegador = navegador

    def run(self):
        while len(self.navegador.find_elements(By.ID ,"side")) < 1 :
            time.sleep(1)
        self.finished.emit()

class WorkerEnviarMensagens(QObject):
    finished = pyqtSignal()
    totalOk = pyqtSignal(int)
    totalError = pyqtSignal(int)

    def __init__(self, navegador, contatos_df, mensagem):
        super(WorkerEnviarMensagens, self).__init__()
        self.navegador = navegador
        self.contatos_df = contatos_df
        self.mensagem = mensagem

    def run(self):
        self.totalOk.emit(0)
        self.totalError.emit(0)
        testeTotalOk = 0
        testeTotalError = 0
        for i, pessoa in enumerate(self.contatos_df['Pessoa']):
            try:
                nomePessoa = pessoa.split()[0]
            except:
                nomePessoa = "Aluno(a)"
            numero = self.contatos_df.loc[i, "Número"]
            # defino qual sera o texto e converto para url encode
            texto = urllib.parse.quote(f"Oi {nomePessoa.capitalize()}, tudo bom com você? {self.mensagem}")
            #crio o link de navegação
            link = f"https://web.whatsapp.com/send?phone=5511{numero}&text={texto}"
            # vou até o link de envio
            try:
                self.navegador.get(link)

                # espera aparecer o elemento que tem id de "side"
                while len(self.navegador.find_elements(By.ID ,"side")) < 1 :
                    time.sleep(1)

                time.sleep(10)
                # xpath do campo que tem que apertar enter
                # //*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p
                testeLoop = 0
                while len(self.navegador.find_elements(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p')) < 1 :
                    time.sleep(1)
                    testeLoop += 1
                    if testeLoop > 20:
                        raise Exception("Não foi concluir, Timeout")

                self.navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p').send_keys(Keys.ENTER)
                testeTotalOk += 1
                self.totalOk.emit(testeTotalOk)
                time.sleep(5)
                
            except Exception as e:
                print(e)
                testeTotalError += 1
                self.totalError.emit(testeTotalError)
        
        self.navegador.get("https://web.whatsapp.com/")
        self.finished.emit()

# classe principal do projeto
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # load the ui file
        # uic.loadUi("screen.ui", self)
        # loadUi("screen.ui", self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # definir planilha de contatos
        self.contatos_df = ""
        self.navegador = webdriver.Chrome()
        self.navegador.get("https://web.whatsapp.com/")

        # define buttons and functions
        self.buttonConnectZap = self.findChild(QPushButton, "buttonConnectZap")
        self.buttonConnectZap.clicked.connect(self.connectZap)

        self.buttonSelecionaArquivo = self.findChild(QPushButton, "buttonSelecionaArquivo")
        self.buttonSelecionaArquivo.clicked.connect(self.selecionaArquivo)

        self.buttonGeraArquivo = self.findChild(QPushButton, "buttonGeraArquivo")
        self.buttonGeraArquivo.clicked.connect(self.gerarArquivoExemplo)

        self.buttonEnviar = self.findChild(QPushButton, "buttonEnviar")
        self.buttonEnviar.clicked.connect(self.enviarMensagensAutomaticas)

        self.buttonEnviarTeste = self.findChild(QPushButton, "buttonEnviarTeste")
        self.buttonEnviarTeste.clicked.connect(self.enviarMensagemTeste)

        self.buttonExportarListaSemNumerosErros = self.findChild(QPushButton, "buttonExportarListaSemNumerosErros")
        self.buttonExportarListaSemNumerosErros.clicked.connect(self.exportarListaSemErros)

        self.labelStatusConnectZap = self.findChild(QLabel, "labelStatusConnectZap")
        self.labelArquivoSelecionado = self.findChild(QLabel, "labelArquivoSelecionado")
        self.labelTotalContatos = self.findChild(QLabel, "labelTotalContatos")
        self.labelTempoEstimado = self.findChild(QLabel, "labelTempoEstimado")
        self.labelEnviadosSucesso = self.findChild(QLabel, "labelEnviadosSucesso")
        self.labelEnviadosErro = self.findChild(QLabel, "labelEnviadosErro")

        self.lineEditNumeroTeste = self.findChild(QLineEdit, "lineEditNumeroTeste")
        self.textoParaEnviar = self.findChild(QPlainTextEdit, "textoParaEnviar")

        # show the app
        self.show()

    def connectZap(self):
        self.labelStatusConnectZap.setText("Aguardando Conexão")
        # Step 2: Create a QThread object
        self.threadConnectZap = QThread()
        # Step 3: Create a worker object
        self.workerConnectZap = WorkerConnectZap(navegador=self.navegador)
        # Step 4: Move worker to the thread
        self.workerConnectZap.moveToThread(self.threadConnectZap)
        # Step 5: Connect signals and slots
        self.threadConnectZap.started.connect(self.workerConnectZap.run)
        self.workerConnectZap.finished.connect(self.threadConnectZap.quit)
        self.workerConnectZap.finished.connect(self.workerConnectZap.deleteLater)
        self.threadConnectZap.finished.connect(self.threadConnectZap.deleteLater)
        # Step 6: Start the thread
        self.threadConnectZap.start()

        # Final resets
        self.buttonConnectZap.setEnabled(False)
        self.threadConnectZap.finished.connect(
            lambda: self.buttonConnectZap.setEnabled(True)
        )
        self.threadConnectZap.finished.connect(
            lambda: self.labelStatusConnectZap.setText("Conectado")
        )

    def selecionaArquivo(self):
        try:
            fname = QFileDialog.getOpenFileName(self, "Selecione o arquivo", "./", "Excel Files (*.xlsx)")
            if fname:
                self.labelArquivoSelecionado.setText(str(fname[0]))
                self.contatos_df = pd.read_excel(fname[0])
                self.labelTotalContatos.setText(str(len(self.contatos_df)))
                tempoTotal = int(self.labelTotalContatos.text()) * 20
                tempoHoras = tempoTotal // ( 60 * 60 )
                tempoSegundos = tempoTotal % ( 60 * 60 )
                tempoMinutos = tempoSegundos // ( 60 )
                tempoSegundos = tempoSegundos % ( 60 )
                stringToPrint = ""
                if tempoHoras:
                    stringToPrint += f'{tempoHoras}h '
                if tempoMinutos:
                    stringToPrint += f'{tempoMinutos}min '
                
                stringToPrint += f'{tempoSegundos}seg '

                self.labelTempoEstimado.setText(stringToPrint)
        except:
            pass
        
    #TODO fazer implementação do gerador de Arquivo Exemplo
    def gerarArquivoExemplo(self): 
        pass

    def setTotalOk(self, n):
        self.labelEnviadosSucesso.setText(str(n))

    def setTotalError(self, n):
        self.labelEnviadosErro.setText(str(n))

    def enviarMensagensAutomaticas(self):
        self.buttonEnviar.setText("Aguarde Finalizar")
        # Step 2: Create a QThread object
        self.threadEnviarMensagens = QThread()
        # Step 3: Create a worker object
        self.workerEnviarMensagens = WorkerEnviarMensagens(
            navegador=self.navegador, 
            contatos_df=self.contatos_df, 
            mensagem=self.textoParaEnviar.toPlainText()
            )
        # Step 4: Move worker to the thread
        self.workerEnviarMensagens.moveToThread(self.threadEnviarMensagens)
        # Step 5: Connect signals and slots
        self.threadEnviarMensagens.started.connect(self.workerEnviarMensagens.run)
        self.workerEnviarMensagens.finished.connect(self.threadEnviarMensagens.quit)
        self.workerEnviarMensagens.finished.connect(self.workerEnviarMensagens.deleteLater)
        self.threadEnviarMensagens.finished.connect(self.threadEnviarMensagens.deleteLater)
        self.workerEnviarMensagens.totalOk.connect(self.setTotalOk)
        self.workerEnviarMensagens.totalError.connect(self.setTotalError) 
        # Step 6: Start the thread
        self.threadEnviarMensagens.start()

        # Final resets
        self.buttonEnviar.setEnabled(False)
        self.threadEnviarMensagens.finished.connect(
            lambda: self.buttonEnviar.setEnabled(True)
        )
        self.threadEnviarMensagens.finished.connect(
            lambda: self.buttonEnviar.setText("Enviar")
        )

    def enviarMensagemTeste(self):
        self.enviarMensagemAutomatica(numero=self.lineEditNumeroTeste.text())

    #TODO fazer implementação do gerador de Arquivo sem numeros com erro
    def exportarListaSemErros(self):
        pass

    def enviarMensagemAutomatica(self, numero):
        texto = urllib.parse.quote(self.textoParaEnviar.toPlainText())
        #crio o link de navegação
        link = f"https://web.whatsapp.com/send?phone=5511{numero}&text={texto}"
        # vou até o link de envio
        self.navegador.get(link)

        # espera aparecer o elemento que tem id de "side"
        while len(self.navegador.find_elements(By.ID ,"side")) < 1 :
            time.sleep(1)
        time.sleep(10)
        # xpath do campo que tem que apertar enter
        # //*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p
        while len(self.navegador.find_elements(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p')) < 1 :
            time.sleep(1)
        self.navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p').send_keys(Keys.ENTER)
        time.sleep(5)

class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        # loadUi("splash.ui", self)


        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.progressBar = self.findChild(QProgressBar, "progressBar")

        self.setWindowFlag(Qt.FramelessWindowHint)
        # pixmap = QPixmap("images.png")
        # self.setPixmap(pixmap)
        self.center()
        self.show()
        self.progress()

    def progress(self):
        for i in range(40):
            time.sleep(0.1)
            self.progressBar.setValue(i)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = SplashScreen()

    UIWindow = UI()

    splash.finish(UIWindow)

    app.exec_()