import re

ERROR_CATALOG: dict[str, str] = {
    "DM_GWPipeline_Gateway_TimeoutError": (
        "O gateway excedeu o tempo limite. Verifique o serviço do gateway, "
        "a conectividade com a fonte e a duração das consultas."
    ),
    "ModelRefreshFailed_CredentialsNotSpecified": (
        "As credenciais da fonte estão ausentes ou expiradas. Atualize as "
        "credenciais no Power BI Service e teste a conexão."
    ),
    "GatewayNotReachable": (
        "O gateway está indisponível. Confirme se o serviço está ativo, online "
        "e associado corretamente à fonte de dados."
    ),
}


def sanitize_error(text: str | None) -> str:
    if not text:
        return "Erro não informado pela API do Power BI."

    sanitized = text
    sanitized = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[IP_REMOVIDO]", sanitized)
    sanitized = re.sub(r"(?i)(password|pwd|secret)\s*=\s*[^;\s]+", r"\1=[REMOVIDO]", sanitized)
    sanitized = re.sub(r"[A-Za-z]:\\[^\s]+", "[CAMINHO_REMOVIDO]", sanitized)
    return sanitized[:4000]


def known_diagnosis(error_code: str | None, description: str | None) -> str | None:
    if error_code and error_code in ERROR_CATALOG:
        return ERROR_CATALOG[error_code]

    searchable = description or ""
    for code, diagnosis in ERROR_CATALOG.items():
        if code.lower() in searchable.lower():
            return diagnosis
    return None
