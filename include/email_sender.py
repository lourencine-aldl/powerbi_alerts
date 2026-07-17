import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config.config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM, EMAIL_TO

def montar_corpo_email(dataset, workspace, erro, sugestao):
    return f"""\
<html>
  <body style="margin:0; padding:0; background-color:#faf9f8;
               font-family: 'Segoe UI', Arial, sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
           style="background-color:#faf9f8; padding: 32px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="560" cellpadding="0" cellspacing="0"
                 style="background-color:#ffffff; border:1px solid #edebe9; border-radius:4px;">

            <!-- Barra superior fina indicando severidade -->
            <tr>
              <td style="height:4px; background-color:#d83b01; border-radius:4px 4px 0 0;"></td>
            </tr>

            <!-- Cabeçalho -->
            <tr>
              <td style="padding: 24px 32px 8px 32px;">
                <p style="margin:0; font-size:12px; color:#605e5c; letter-spacing:.5px; text-transform:uppercase;">
                  Alerta de processamento
                </p>
                <h1 style="margin:6px 0 0; font-size:20px; font-weight:600; color:#201f1e;">
                  Falha na atualização do dataset
                </h1>
              </td>
            </tr>

            <!-- Detalhes -->
            <tr>
              <td style="padding: 16px 32px 0 32px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
                       style="font-size:13px; color:#323130;">
                  <tr>
                    <td style="padding:6px 0; color:#605e5c; width:110px;">Dataset</td>
                    <td style="padding:6px 0; font-weight:600;">{dataset}</td>
                  </tr>
                  <tr>
                    <td style="padding:6px 0; color:#605e5c;">Workspace</td>
                    <td style="padding:6px 0; font-weight:600;">{workspace}</td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- Linha divisória -->
            <tr>
              <td style="padding: 20px 32px 0 32px;">
                <div style="border-top:1px solid #edebe9;"></div>
              </td>
            </tr>

            <!-- Erro -->
            <tr>
              <td style="padding: 16px 32px 0 32px;">
                <p style="margin:0 0 4px; font-size:12px; font-weight:600; color:#d83b01; text-transform:uppercase; letter-spacing:.5px;">
                  Erro
                </p>
                <p style="margin:0; font-size:14px; color:#323130; line-height:1.5;">
                  {erro}
                </p>
              </td>
            </tr>

            <!-- Sugestão -->
            <tr>
              <td style="padding: 16px 32px 0 32px;">
                <p style="margin:0 0 4px; font-size:12px; font-weight:600; color:#0078d4; text-transform:uppercase; letter-spacing:.5px;">
                  Sugestão
                </p>
                <p style="margin:0; font-size:14px; color:#323130; line-height:1.5;">
                  {sugestao}
                </p>
              </td>
            </tr>

            <!-- Rodapé -->
            <tr>
              <td style="padding: 28px 32px 24px 32px;">
                <p style="margin:0; font-size:11px; color:#a19f9d;">
                  Esta é uma mensagem automática. Não é necessário responder.
                </p>
              </td>
            </tr>

          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""


def enviar_email(assunto, corpo):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "html", "utf-8"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
        servidor.starttls()
        servidor.login(SMTP_USER, SMTP_PASSWORD)
        servidor.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
