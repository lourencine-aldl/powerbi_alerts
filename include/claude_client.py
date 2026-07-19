import anthropic

from config.config import Settings
from include.diagnostics import known_diagnosis, sanitize_error


def gerar_sugestao(
    settings: Settings,
    dataset_name: str,
    erro_descricao: str | None,
    error_code: str | None = None,
) -> str:
    deterministic = known_diagnosis(error_code, erro_descricao)
    if deterministic:
        return deterministic

    sanitized_error = sanitize_error(erro_descricao)
    if not settings.llm_enabled or not settings.anthropic_api_key:
        return "Erro ainda não catalogado. Revise os detalhes técnicos no Power BI Service."

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    response = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=180,
        messages=[
            {
                "role": "user",
                "content": (
                    f"O modelo semântico Power BI '{dataset_name}' falhou com o erro: "
                    f"'{sanitized_error}'. Sugira causa provável e correção em português, "
                    "de forma técnica e objetiva, sem inventar informações."
                ),
            }
        ],
    )
    return response.content[0].text.strip()[:500]
