from src.dados.analisar_ocorrencias import AnalisarDados

analisador = AnalisarDados()

# coluna_filtro = "LOGRADOURO"
# filtros = {
#     "LOGRADOURO": "Avenida Dona Belmira MarIN",
# }

# Teste a partir de
# coluna_filtro = "DIA_SEMANA"
# filtros = {
#     "MUNICIP_CIRCUNSCRICAO": "S.PAULO",
#     "HORA_INICIO": 18
# }

# Teste usando datas completas
# coluna_filtro = "DESCR_TIPOLOCAL"
# filtros = {
#     "DATA_INICIO": "2025-01-01",
#     "DATA_FIM": "2025-01-15",
#     "MUNICIP_CIRCUNSCRICAO": "S.PAULO"
# }

# Teste combinando mes e dias
coluna_filtro = "HORA_OCORRENCIA_BO"
filtros = {
    "MES_ESTATISTICA": 2,
    "DIA_INICIO": 10,
    "DIA_FIM": 20
}

resposta = analisador.frequencia_temporal(coluna_filtro, filtros)

print(resposta)

