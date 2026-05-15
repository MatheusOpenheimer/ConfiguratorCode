def ns_lido_evento(event, modo_operacao, limpar_callback, gerar_callback):
    """
    Função de leitura do ENTER.
    NÃO mexe em widgets.
    Só coordena ações.
    """
    limpar_callback()

    if modo_operacao.get() == "Produção":
        gerar_callback()
