import logging
import sys

from config.config import get_settings
from include.claude_client import gerar_sugestao
from include.collector import coletar_datasets, tratar_dataframe
from include.diagnostics import sanitize_error
from include.email_sender import enviar_email, montar_corpo_email
from include.powerbi_client import autenticar
from include.repository import AlertRepository

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("powerbi_alerts")


def processar_alertas(df, settings, repository: AlertRepository) -> None:
    if df.empty:
        logger.info("Nenhum modelo semântico encontrado")
        return

    for _, row in df.iterrows():
        event = {
            "refresh_key": row["Refresh Key"],
            "workspace_id": row["Workspace ID"],
            "workspace_name": row["Workspace"],
            "dataset_id": row["Dataset ID"],
            "dataset_name": row["Dataset"],
            "status": row["Status Atualização"],
            "start_time": row["Data Início"].isoformat() if row["Data Início"] is not None and not row["Data Início"] is not row["Data Início"] else None,
            "end_time": row["Data Fim"].isoformat() if row["Data Fim"] is not None and not row["Data Fim"] is not row["Data Fim"] else None,
            "error_code": row.get("Código Erro"),
            "error_description": row.get("Descrição Erro"),
            "payload": row.get("Payload", {}),
        }
        repository.save_refresh(event)

        if row["Status Atualização"] != "Failed":
            continue

        refresh_key = row["Refresh Key"]
        if repository.was_notified(refresh_key):
            logger.info("Falha já notificada: %s", row["Dataset"])
            continue

        error_description = sanitize_error(row.get("Descrição Erro"))
        diagnosis = gerar_sugestao(
            settings,
            row["Dataset"],
            error_description,
            row.get("Código Erro"),
        )
        repository.create_incident(refresh_key, diagnosis)

        body = montar_corpo_email(
            dataset=row["Dataset"],
            workspace=row["Workspace"],
            erro=error_description,
            sugestao=diagnosis,
        )
        enviar_email(
            settings,
            assunto=f"[VaderOps][Power BI] Falha - {row['Dataset']}",
            corpo=body,
        )
        repository.mark_notified(refresh_key)
        logger.info("Alerta enviado: %s", row["Dataset"])


def main() -> int:
    try:
        settings = get_settings()
        repository = AlertRepository(settings.database_url)
        headers = autenticar()
        dataframe = tratar_dataframe(
            coletar_datasets(headers),
            timezone=settings.app_timezone,
        )
        processar_alertas(dataframe, settings, repository)
        return 0
    except Exception:
        logger.exception("Falha na execução do monitor")
        return 1


if __name__ == "__main__":
    sys.exit(main())
