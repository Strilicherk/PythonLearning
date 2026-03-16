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

    def impacto_financeiro(self, nome_coluna: str, filtro: dict, operacao: str):
        result = self._aplicar_filtros(nome_coluna, filtro)
        if isinstance(result, str):
            return result

        mapa_valores = {
            "Sem Informação": np.nan,
            "Até R$ 5.000, 00": 5000.0,
            "De R$ 5.001,00 a R$ 10 mil": 7500.0,
            "De R$ 10.001,00 a R$ 20 mil": 15000.0,
            "De R$ 20.001,00 a R$ 30 mil": 25000.0,
            "De R$ 30.001,00 a R$ 40 mil": 35000.0,
            "De R$ 40.001,00 a R$ 50 mil": 45000.0,
            "De R$ 50.001,00 a R$ 60 mil": 55000.0,
            "De R$ 60.001,00 a R$ 70 mil": 65000.0,
            "De R$ 70.001,00 a R$ 80 mil": 75000.0,
            "De R$ 80.001,00 a R$ 90 mil": 85000.0,
            "De R$ 90.001,00 a R$ 100 mil": 95000.0,
            "De R$ 100.001,00 a R$ 150 mil": 125000.0,
            "De R$ 150.001,00 a R$ 200 mil": 175000.0,
            "De R$ 200.001,00 a R$ 400 mil": 300000.0,
            "De R$ 400.001,00 a R$ 800 mil": 600000.0,
            "De R$ 800.001,00 a R$ 1 milhão": 900000.0,
            "Acima de R$ 1 milhão": 1000000.0,
        }

        valores_numericos = result.map(mapa_valores)

        if operacao.lower() == "soma":
            return valores_numericos.sum()
        elif operacao.lower() == "media":
            return valores_numericos.mean()
        elif operacao.lower() == "mediana":
            return valores_numericos.median()
        else:
            return "Operação matemática não reconhecida. Utilize 'soma' ou 'media'."







