import os
import requests
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

db = DB()
cvm_service = CVMDataService(db)


def executar_servico_cvm():
    cvm_service.executar()


def executar_request_servidor():
    """Request no servidor para a Render.io não hibernar a máquina"""
    r = requests.get(os.environ.get("URL_APP"))
    return r.text


# Agendar a execução do serviço todos os dias às 01h
schedule.every().day.at("01:00").do(executar_servico_cvm)
# Execução do request para o servidor não hibernar
schedule.every(10).minutes.do(executar_request_servidor)


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
