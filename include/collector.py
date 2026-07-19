import hashlib
import json

import pandas as pd

from include.powerbi_client import (
    listar_workspaces,
    listar_datasets,
    obter_ultima_atualizacao,
    obter_descricao_erro,
)


def _refresh_key(workspace_id: str, dataset_id: str, refresh: dict) -> str:
    raw_key = "|".join(
        [
            workspace_id,
            dataset_id,
            str(refresh.get("requestId") or ""),
            str(refresh.get("startTime") or ""),
            str(refresh.get("status") or ""),
        ]
    )
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def coletar_datasets(headers):
    dados = []

    for workspace in listar_workspaces(headers):
        for dataset in listar_datasets(workspace["id"], headers):
            try:
                refresh = obter_ultima_atualizacao(
                    workspace["id"], dataset["id"], headers
                )
            except Exception as exc:
                refresh = None
                consulta_erro = str(exc)
            else:
                consulta_erro = None

            linha_base = {
                "Workspace": workspace["name"],
                "Workspace ID": workspace["id"],
                "Dataset": dataset["name"],
                "Dataset ID": dataset["id"],
            }

            if refresh is None:
                dados.append(
                    {
                        **linha_base,
                        "Refresh Key": hashlib.sha256(
                            f"{workspace['id']}|{dataset['id']}|consulta".encode("utf-8")
                        ).hexdigest(),
                        "Status Atualização": "Erro ao consultar",
                        "Descrição Erro": consulta_erro,
                        "Código Erro": None,
                        "Data Início": None,
                        "Data Fim": None,
                        "Payload": {},
                    }
                )
            elif refresh == {}:
                dados.append(
                    {
                        **linha_base,
                        "Refresh Key": hashlib.sha256(
                            f"{workspace['id']}|{dataset['id']}|nunca".encode("utf-8")
                        ).hexdigest(),
                        "Status Atualização": "Nunca Atualizado",
                        "Descrição Erro": None,
                        "Código Erro": None,
                        "Data Início": None,
                        "Data Fim": None,
                        "Payload": {},
                    }
                )
            else:
                raw_error = refresh.get("serviceExceptionJson")
                error_code = None
                if raw_error:
                    try:
                        error_code = json.loads(raw_error).get("errorCode")
                    except (TypeError, json.JSONDecodeError):
                        pass

                dados.append(
                    {
                        **linha_base,
                        "Refresh Key": _refresh_key(
                            workspace["id"], dataset["id"], refresh
                        ),
                        "Status Atualização": refresh.get("status"),
                        "Descrição Erro": obter_descricao_erro(refresh),
                        "Código Erro": error_code,
                        "Data Início": refresh.get("startTime"),
                        "Data Fim": refresh.get("endTime"),
                        "Payload": refresh,
                    }
                )

    return pd.DataFrame(dados)


def tratar_dataframe(df, timezone: str = "America/Bahia"):
    if df.empty:
        return df

    for coluna in ["Data Início", "Data Fim"]:
        df[coluna] = pd.to_datetime(df[coluna], utc=True, errors="coerce").dt.tz_convert(
            timezone
        )

    return df[df["Status Atualização"] != "Nunca Atualizado"]
