
import json
import requests

from config.config import TENANT_ID, CLIENT_ID, CLIENT_SECRET, BASE_URL

#realizar a autenticacao com o token
def autenticar():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    resposta = requests.post(
        url,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "https://analysis.windows.net/powerbi/api/.default",
        },
    )
    resposta.raise_for_status()

    return {"Authorization": f"Bearer {resposta.json()['access_token']}"}

#listar os workspaces autorizados
def listar_workspaces(headers):
    url = f"{BASE_URL}/groups"
    return requests.get(url, headers=headers).json()["value"]

#listar os datasets
def listar_datasets(workspace_id, headers):
    url = f"{BASE_URL}/groups/{workspace_id}/datasets"
    return requests.get(url, headers=headers).json()["value"]

#capturar a ultima atualização do dataset
def obter_ultima_atualizacao(workspace_id, dataset_id, headers):
    url = (
        f"{BASE_URL}/groups/{workspace_id}/datasets/"
        f"{dataset_id}/refreshes?$top=1"
    )

    resposta = requests.get(url, headers=headers)

    if resposta.status_code != 200:
        return None

    refreshes = resposta.json().get("value", [])
    return refreshes[0] if refreshes else {}

# buscar os detalhes do erro
def obter_descricao_erro(refresh):
    if not refresh or refresh.get("status") != "Failed":
        return None

    erro = refresh.get("serviceExceptionJson")
    if not erro:
        return None

    try:
        erro = json.loads(erro)
        return erro.get("errorDescription") or erro.get("errorCode")
    except Exception:
        return erro
