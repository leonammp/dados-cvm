from db.db import DB
from dtos.eventoCorporativoDTO import EventoCorporativoDTO


class EventoCorporativoRepository:
    def __init__(self, db: DB):
        self.db = db

    def inserir(self, dados: EventoCorporativoDTO):
            self.db.execute('''INSERT INTO dados_cvm (cnpj_empresa, nome_empresa, codigo_cvm, categoria,
                                                    data_referencia, tipo, especie, assunto, data_entrega,
                                                    tipo_apresentacao, protocolo_entrega, versao, arquivo)
                                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                            (dados.cnpj_empresa, dados.nome_empresa, dados.codigo_cvm, dados.categoria,
                             dados.data_referencia, dados.tipo, dados.especie, dados.assunto, dados.data_entrega,
                             dados.tipo_apresentacao, dados.protocolo_entrega, dados.versao, dados.arquivo))
