from dataclasses import dataclass


@dataclass
class EventoCorporativoDTO:
    cnpj_empresa: str
    nome_empresa: str
    codigo_cvm: str
    categoria: str
    data_referencia: str
    versao: str
    especie: str
    data_entrega: str
    tipo: str
    assunto: str
    tipo_apresentacao: str
    protocolo_entrega: str
    arquivo: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data.get('CNPJ_Companhia', ''),
            data.get('Nome_Companhia', ''),
            data.get('Codigo_CVM', ''),
            data.get('Categoria', ''),
            data.get('Data_Referencia', ''),
            data.get('Versao', ''),
            data.get('Especie', ''),
            data.get('Data_Entrega', ''),
            data.get('Tipo', ''),
            data.get('Assunto', ''),
            data.get('Tipo_Apresentacao', ''),
            data.get('Protocolo_Entrega', ''),
            data.get('Link_Download', '')
        )