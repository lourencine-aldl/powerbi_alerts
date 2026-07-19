import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html import escape

from config.config import Settings


def montar_corpo_email(dataset: str, workspace: str, erro: str, sugestao: str) -> str:
    dataset = escape(dataset or "")
    workspace = escape(workspace or "")
    erro = escape(erro or "")
    sugestao = escape(sugestao or "")

    return f"""\
<html>
  <body style="margin:0;padding:0;background:#faf9f8;font-family:'Segoe UI',Arial,sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="padding:32px 0;">
      <tr><td align="center">
        <table role="presentation" width="560" cellpadding="0" cellspacing="0" style="background:#fff;border:1px solid #edebe9;border-radius:6px;">
          <tr><td style="height:4px;background:#d83b01;border-radius:6px 6px 0 0;"></td></tr>
          <tr><td style="padding:24px 32px 8px;">
            <p style="margin:0;font-size:12px;color:#605e5c;text-transform:uppercase;">VaderOps · Power BI</p>
            <h1 style="margin:6px 0 0;font-size:20px;color:#201f1e;">Falha na atualização</h1>
          </td></tr>
          <tr><td style="padding:16px 32px 0;">
            <p><strong>Modelo semântico:</strong> {dataset}</p>
            <p><strong>Workspace:</strong> {workspace}</p>
          </td></tr>
          <tr><td style="padding:12px 32px 0;"><hr style="border:0;border-top:1px solid #edebe9;"></td></tr>
          <tr><td style="padding:12px 32px 0;">
            <p style="color:#d83b01;font-weight:600;">Erro</p>
            <p style="line-height:1.5;">{erro}</p>
          </td></tr>
          <tr><td style="padding:12px 32px 24px;">
            <p style="color:#0078d4;font-weight:600;">Diagnóstico</p>
            <p style="line-height:1.5;">{sugestao}</p>
            <p style="margin-top:24px;font-size:11px;color:#a19f9d;">Mensagem automática. Verifique o incidente no VaderOps.</p>
          </td></tr>
        </table>
      </td></tr>
    </table>
  </body>
</html>
"""


def enviar_email(settings: Settings, assunto: str, corpo: str) -> None:
    message = MIMEMultipart()
    message["From"] = settings.email_from
    message["To"] = ", ".join(settings.email_to)
    message["Subject"] = assunto
    message.attach(MIMEText(corpo, "html", "utf-8"))

    with smtplib.SMTP(settings.smtp_server, settings.smtp_port, timeout=30) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.email_from, settings.email_to, message.as_string())
