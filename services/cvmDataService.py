import os
from datetime import datetime, timedelta
import requests
import zipfile
import csv

from db.db import DB
from dtos.eventoCorporativoDTO import EventoCorporativoDTO

from repository.eventoCorporativoRepository import EventoCorporativoRepository


class CVMDataService:
    tempfile = 'temp.zip'

    def __init__(self, url_arquivo: str, extrair_para: str, db: DB):
        self.url_arquivo = url_arquivo
        self.extrair_para = extrair_para
        self.evento_corporativo_repository = EventoCorporativoRepository(db)

    def executar(self):
        self.baixar_e_extrair_zip()
        csv_file = os.path.join(self.extrair_para, "ipe_cia_aberta_2024.csv")
        self.inserir_dados_do_csv(csv_file)
        self.remover_diretorio()

    def baixar_e_extrair_zip(self) -> None:
        """Faz o download de um arquivo ZIP e extrai seu conteúdo."""
        response = requests.get(self.url_arquivo)
        with open(self.tempfile, 'wb') as f:
            f.write(response.content)
        with zipfile.ZipFile(self.tempfile, 'r') as zip_ref:
            zip_ref.extractall(self.extrair_para)
        os.remove(self.tempfile)

    def inserir_dados_do_csv(self, csv_file: str) -> None:
        """Insere dados de um arquivo CSV na tabela do banco de dados."""
        with open(csv_file, newline='', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                evento_corporativo: EventoCorporativoDTO = EventoCorporativoDTO.from_dict(row)
                data_entrega = datetime.strptime(evento_corporativo.data_entrega, '%Y-%m-%d')
                data_ontem = datetime.now() - timedelta(days=1)
                if data_entrega.date() == data_ontem.date():
                    self.evento_corporativo_repository.inserir(evento_corporativo)

    def remover_diretorio(self) -> None:
        """Remove o diretório e seu conteúdo."""
        for filename in os.listdir(self.extrair_para):
            file_path = os.path.join(self.extrair_para, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    for sub_filename in os.listdir(file_path):
                        sub_file_path = os.path.join(file_path, sub_filename)
                        os.unlink(sub_file_path)
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Erro ao excluir {file_path}: {e}")
