import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variável de ambiente obrigatória ausente: {name}")
    return value


def _bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    pbi_tenant_id: str
    pbi_client_id: str
    pbi_client_secret: str
    base_url: str
    request_timeout_seconds: int
    request_max_retries: int
    app_timezone: str
    database_url: str
    llm_enabled: bool
    anthropic_api_key: Optional[str]
    anthropic_model: str
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    email_from: str
    email_to: list[str]


def get_settings() -> Settings:
    smtp_user = _required("SMTP_USER")
    recipients = [
        item.strip()
        for item in _required("EMAIL_TO").split(",")
        if item.strip()
    ]

    llm_enabled = _bool("LLM_ENABLED", True)
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if llm_enabled and not anthropic_api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY é obrigatória quando LLM_ENABLED=true"
        )

    return Settings(
        pbi_tenant_id=_required("PBI_TENANT_ID"),
        pbi_client_id=_required("PBI_CLIENT_ID"),
        pbi_client_secret=_required("PBI_CLIENT_SECRET"),
        base_url=os.getenv("PBI_BASE_URL", "https://api.powerbi.com/v1.0/myorg"),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30")),
        request_max_retries=int(os.getenv("REQUEST_MAX_RETRIES", "3")),
        app_timezone=os.getenv("APP_TIMEZONE", "America/Bahia"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///data/powerbi_alerts.db"),
        llm_enabled=llm_enabled,
        anthropic_api_key=anthropic_api_key,
        anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_user=smtp_user,
        smtp_password=_required("SMTP_PASSWORD"),
        email_from=os.getenv("EMAIL_FROM", smtp_user),
        email_to=recipients,
    )
