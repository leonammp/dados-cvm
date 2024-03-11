from dotenv import load_dotenv

from db.db import DB
from services.cvmDataService import CVMDataService

load_dotenv()

url_arquivo = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_2024.zip'
extrair_para = 'temp'

db = DB()
cvm_service = CVMDataService(url_arquivo, extrair_para, db)
cvm_service.executar()
