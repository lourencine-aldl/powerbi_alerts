from include.powerbi_client import autenticar
from include.collector import coletar_datasets, tratar_dataframe
from include.claude_client import gerar_sugestao
from include.email_sender import enviar_email, montar_corpo_email


def processar_alertas(df):
    falhas = df[df["Status Atualização"] == "Failed"]

    for _, linha in falhas.iterrows():
        sugestao = gerar_sugestao(linha["Dataset"], linha["Descrição Erro"])

        corpo = montar_corpo_email(
            dataset=linha["Dataset"],
            workspace=linha["Workspace"],
            erro=linha["Descrição Erro"],
            sugestao=sugestao,
        )

        enviar_email(
            assunto=f"[Power BI] Falha na atualização - {linha['Dataset']}",
            corpo=corpo,
        )

        print(f"Alerta enviado: {linha['Dataset']}")


def main():
    headers = autenticar()

    df = coletar_datasets(headers)
    df = tratar_dataframe(df)

    print(df)
    #print(f"\nTotal de datasets: {len(df)}")

    processar_alertas(df)


if __name__ == "__main__":
    main()
