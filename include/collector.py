import pandas as pd
from include.powerbi_client import (
    listar_workspaces,
    listar_datasets,
    obter_ultima_atualizacao,
    obter_descricao_erro,
)
#coletar os dados do servico do powerbi
def coletar_datasets(headers):
    dados = []

    for workspace in listar_workspaces(headers):
        for dataset in listar_datasets(workspace["id"], headers):

            refresh = obter_ultima_atualizacao(workspace["id"], dataset["id"], headers)

            linha_base = {
                "Workspace": workspace["name"],
                "Workspace ID": workspace["id"],
                "Dataset": dataset["name"],
                "Dataset ID": dataset["id"],
            }

            if refresh is None:
                dados.append({
                    **linha_base,
                    "Atualização": None,
                    "Status Atualização": "Erro ao consultar",
                    "Descrição Erro": None,
                    "Data Início": None,
                    "Data Fim": None,
                })

            elif refresh == {}:
                dados.append({
                    **linha_base,
                    "Atualização": None,
                    "Status Atualização": "Nunca Atualizado",
                    "Descrição Erro": None,
                    "Data Início": None,
                    "Data Fim": None,
                })

            else:
                dados.append({
                    **linha_base,
                    "Atualização": 1,
                    "Status Atualização": refresh.get("status"),
                    "Descrição Erro": obter_descricao_erro(refresh),
                    "Data Início": refresh.get("startTime"),
                    "Data Fim": refresh.get("endTime"),
                })

    return pd.DataFrame(dados)

#tratar os dados em um df com as informacoes que precisamos e as devidas conversoes
def tratar_dataframe(df):
    for coluna in ["Data Início", "Data Fim"]:
        df[coluna] = (
            pd.to_datetime(df[coluna], utc=True)
            .dt.tz_convert("America/Sao_Paulo")
        )

    return df[df["Status Atualização"] != "Nunca Atualizado"]
