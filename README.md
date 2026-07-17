# Monitor de Falhas de Atualização do Power BI com IA

Desenvolvi um serviço simples que monitora a última atualização de todos os datasets do Power BI, identifica falhas e envia um alerta por e-mail contendo o erro encontrado e uma sugestão de correção gerada por um LLM.

> No projeto de teor acadêmico utilizei a **Claude (Anthropic)**, mas a solução pode ser executda com qualquer outro modelo de IA.

---

## O que ele faz

- Autentica no Power BI utilizando **Service Principal**, garantindo acesso seguro à API.
- Percorre os **workspaces** autorizados.
- Consulta a última atualização de cada **dataset**.
- Identifica automaticamente os datasets cuja atualização falhou.
- Envia o erro para um LLM, que gera uma sugestão objetiva de correção.
- Dispara um e-mail de alerta contendo:
  - Dataset
  - Workspace
  - Erro encontrado
  - Sugestão de correção

---

## Como Utilizar

Para acessar a API do Power BI é necessário criar um **Service Principal** no Azure e possuir as seguintes credenciais (você acha facilmente tutoriais no Youtube).

- `CLIENT_ID`
- `TENANT_ID`
- `CLIENT_SECRET`

Essas credenciais permitem que a aplicação acesse a API do Power BI de forma segura e sem depender de um usuário.

---

## Variáveis de ambiente (crie um arquivo `.env` na raiz do diretório)

### Power BI

```env
PBI_TENANT_ID=
PBI_CLIENT_ID=
PBI_CLIENT_SECRET=
```

### Claude (modelo llm)

```env
ANTHROPIC_API_KEY=
```

### SMTP (email)

```env
SMTP_SERVER=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
EMAIL_FROM=
EMAIL_TO=
```

---

## Instalação

```bash
pip install -r requirements.txt
```

Preencha as variáveis com suas credenciais.

```bash
python main.py
```


