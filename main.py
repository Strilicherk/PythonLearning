from src.dados.analisar_ocorrencias import AnalisarDados

analisador = AnalisarDados()

# Parâmetros para frequencia_temporal
coluna_temporal = "DIA_SEMANA"
filtros_temporal = {
    "ANO_BO": 2025,
    "CIDADE": "S.PAULO"
}

# Parâmetros para mapeamento_geografico
coluna_geografica = "BAIRRO"
filtros_geograficos = {
    "CIDADE": "S.PAULO",
    "MES_ESTATISTICA": 3
}

# Parâmetros para impacto_financeiro
coluna_dinheiro = "VALOR_DA_CARGA"
filtros_financeiros = {
    "CIDADE": "S.PAULO",
    "ANO_BO": 2025
}
operacao_matematica = "soma"

# resposta1 = analisador.frequencia_temporal(coluna_temporal, filtros_temporal)
# resposta2 = analisador.frequencia_geografica(coluna_geografica, filtros_geograficos, 5, False)
resposta3 = analisador.impacto_financeiro(coluna_dinheiro, filtros_financeiros, operacao_matematica)

# print(resposta1)
# print(resposta2)
print(resposta3)

