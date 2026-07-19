# Power BI Alerts — módulo VaderOps

Serviço de monitoramento das atualizações dos modelos semânticos do Power BI. Consulta os workspaces autorizados, identifica falhas, registra histórico local, evita notificações duplicadas, produz diagnóstico técnico e envia alertas por e-mail.

## Arquitetura

- **Power BI API:** coleta workspaces, modelos semânticos e última atualização.
- **SQLite:** persiste eventos e incidentes para deduplicação.
- **Catálogo de erros:** responde erros conhecidos sem custo de IA.
- **Claude opcional:** analisa somente erros não catalogados e sanitizados.
- **SMTP:** envia o alerta em HTML.

Esta base foi preparada para futuramente funcionar como o conector Power BI do VaderOps. O Reporte BI pode consumir o status dos ativos, enquanto o VaderOps permanece responsável pela saúde, incidentes e notificações.

## Principais melhorias

- deduplicação por refresh;
- histórico de eventos e incidentes;
- validação das variáveis obrigatórias;
- sanitização de mensagens antes do LLM;
- diagnóstico determinístico para erros conhecidos;
- LLM configurável e opcional;
- proteção contra HTML inesperado no e-mail;
- logs estruturados com o módulo `logging`;
- Docker e Docker Compose;
- teste automatizado da persistência.

## Configuração

Copie o exemplo de ambiente:

```bash
cp .env.example .env
```

Preencha as credenciais do Power BI, SMTP e, quando habilitado, Anthropic.

Variáveis importantes:

```env
APP_TIMEZONE=America/Bahia
DATABASE_URL=sqlite:///data/powerbi_alerts.db
LLM_ENABLED=true
EMAIL_TO=responsavel@empresa.com,outro@empresa.com
```

## Execução local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Docker

```bash
docker compose build
docker compose run --rm powerbi-alerts
```

O banco será persistido em `./data/powerbi_alerts.db`.

## Agendamento

Exemplo com cron a cada dez minutos:

```cron
*/10 * * * * cd /opt/powerbi_alerts && docker compose run --rm powerbi-alerts
```

Em uma evolução posterior, a execução pode ser coordenada pelo Prefect ou Airflow, mantendo este repositório responsável apenas pela regra de monitoramento.

## Testes

```bash
pytest -q
```

## Próximas evoluções

1. migrar a persistência para PostgreSQL;
2. monitorar atraso e atualização excessivamente longa;
3. registrar recuperação automática dos incidentes;
4. incluir Telegram, Teams, WhatsApp e webhooks;
5. expor API FastAPI para o VaderOps e Reporte BI;
6. monitorar gateways e capacidades do Power BI.
