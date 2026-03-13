import pandas as pd
import numpy as np

class AnalisarDados:
    def __init__(self):
        self.dados = pd.read_excel("data/v3.0 - SP CARGA FILTRADA.xlsx", sheet_name="SPCARGA")
        self.dados["SEMESTRE"] = np.where(self.dados["MES_ESTATISTICA"] < 7, 1, 2)
        self.dados["DATA_HORA_OCORRENCIA_BO"] = pd.to_datetime(self.dados["DATA_OCORRENCIA_BO"].astype(str) + " " + self.dados["HORA_OCORRENCIA_BO"].astype(str), errors='coerce')
        self.dicionario_colunas = {
            "HORA_INICIO": {"COLUNA": "DATA_HORA_OCORRENCIA_BO",
                            "FUNCAO": lambda x: x.dt.hour},
            "HORA_FIM": {"COLUNA": "DATA_HORA_OCORRENCIA_BO",
                         "FUNCAO": lambda x: x.dt.hour},

            "DIA_INICIO": {"COLUNA": "DATA_HORA_OCORRENCIA_BO",
                           "FUNCAO": lambda x: x.dt.day},
            "DIA_FIM": {"COLUNA": "DATA_HORA_OCORRENCIA_BO",
                        "FUNCAO": lambda x: x.dt.day},

            "DATA_INICIO": {"COLUNA": "DATA_HORA_OCORRENCIA_BO",
                            "FUNCAO": lambda x: x},
            "DATA_FIM": {"COLUNA": "DATA_HORA_OCORRENCIA_BO",
                         "FUNCAO": lambda x: x},

            "MES_INICIO": {"COLUNA": "MES_ESTATISTICA",
                           "FUNCAO": lambda x: x},
            "MES_FIM": {"COLUNA": "MES_ESTATISTICA",
                        "FUNCAO": lambda x: x},

            "ANO_INICIO": {"COLUNA": "ANO_BO",
                           "FUNCAO": lambda x: x},
            "ANO_FIM": {"COLUNA": "ANO_BO",
                        "FUNCAO": lambda x: x},
        }

    def _aplicar_filtros(self, nome_coluna: str, filtro: dict):
        mascara_final = pd.Series(True, self.dados.index)
        for chave, valor in filtro.items():
            if chave in self.dados.columns or chave in self.dicionario_colunas:
                if "INICIO" in chave:
                    coluna_real = self.dicionario_colunas.get(chave).get("COLUNA")
                    funcao = self.dicionario_colunas.get(chave).get("FUNCAO")
                    mascara_final = mascara_final & (funcao(self.dados[coluna_real]) >= valor)
                elif "FIM" in chave:
                    coluna_real = self.dicionario_colunas.get(chave).get("COLUNA")
                    funcao = self.dicionario_colunas.get(chave).get("FUNCAO")
                    mascara_final = mascara_final & (funcao(self.dados[coluna_real]) <= valor)
                else:
                    if isinstance(valor, str):
                        mascara_final = mascara_final & (self.dados[chave].str.upper() == valor.upper())
                    else:
                        mascara_final = mascara_final & (self.dados[chave] == valor)
                if not mascara_final.any():
                    return "Nenhum registro criminal encontrado com os filtros informados."
        return self.dados[mascara_final][nome_coluna]

    def frequencia_temporal(self, nome_coluna: str, filtro: dict):
        result = self._aplicar_filtros(nome_coluna, filtro)
        if isinstance(result, str):
            return result
        else:
            return result.value_counts()

    def frequencia_geografica(self, nome_coluna: str, filtro: dict, limite: int, crescente: bool):
        result = self._aplicar_filtros(nome_coluna, filtro)
        if isinstance(result, str):
            return result

        return result.value_counts(ascending=crescente).head(limite)







