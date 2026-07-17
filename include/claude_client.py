

import anthropic
from config.config import ANTHROPIC_API_KEY

def gerar_sugestao(dataset_name, erro_descricao):
    if not erro_descricao:
        return ""

    cliente = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    resposta = cliente.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        messages=[{
            "role": "user",
            "content": (
                f"O dataset Power BI '{dataset_name}' falhou ao atualizar com o erro: "
                f"'{erro_descricao}'. Em no máximo 200 caracteres, sugira a causa provável "
                f"e a correção, em português, direto ao ponto, sem introduções e seja técnico."
            ),
        }],
    )

    texto = resposta.content[0].text.strip()
    return texto[:200]
