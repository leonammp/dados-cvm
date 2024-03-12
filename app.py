from flask import Flask
from gevent import monkey

monkey.patch_all()
import gevent
from dotenv import load_dotenv
import schedule

from db.db import DB
from services.cvmDataService import CVMDataService

load_dotenv()
app = Flask(__name__)

url_arquivo = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_2024.zip'
extrair_para = 'temp'

db = DB()
cvm_service = CVMDataService(url_arquivo, extrair_para, db)


def executar_servico_cvm():
    cvm_service.executar()


# Agendar a execução do serviço todos os dias às 01h
schedule.every().day.at("01:00").do(executar_servico_cvm)


@app.route("/")
def status():
    return "Serviço CVM agendado para ser executado todos os dias às 01h."


def run_schedule():
    while True:
        schedule.run_pending()
        gevent.sleep(1)


# Criar uma nova tarefa Gevent para executar o agendamento
schedule_task = gevent.spawn(run_schedule)

application = app
