import customtkinter as ctk
import subprocess
from PIL import Image
from logic.datamatrix import gerar_datamatrix
from logic.leitor import ns_lido_evento
from utils.usb import verificar_leitor_usb
import os
import sys


##################LEITURA DO MODELO DE PRODUTO###############
def debug_modelo():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    caminho = os.path.join(base_path, "modelo.txt")

    print("=== DEBUG MODELO ===")
    print("Base path:", base_path)
    print("Existe modelo.txt?", os.path.exists(caminho))

    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            print("Conteúdo bruto:", repr(f.read()))
    print("====================")

def carregar_modelo():
    # Caminho correto tanto para .py quanto para .exe
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    caminho = os.path.join(base_path, "modelo.txt")

    if not os.path.exists(caminho):
        return "MODELO_NAO_DEFINIDO"

    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()

    if not conteudo:
        return "MODELO_NAO_DEFINIDO"

    return conteudo

debug_modelo()

################################################################
Modelo = carregar_modelo()
Fabricante = "CUSTOM"
COR_PRODUCAO = "azure2"
COR_EXPEDIÇÃO= "azure3" 



def caminho_recurso(relativo):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relativo)
    return os.path.join(os.path.abspath("."), relativo)

def ao_pressionar_enter(event):
    modo = modo_operacao.get()

    if modo == "Expeção Final":
        # ENTER vira "clicar no verificar"
        verificar_dispositivo()
        campo_ns.delete(0, "end")
        campo_ns.focus()
    else:
        # Produção: ENTER gera o QR
        gerar_datamatrix(
            campo_ns,
            label_img,
            botao_verificar,
            final,
            app,
            Fabricante,
            Modelo,
            limpar_resultado_verificacao
        )
def ao_mudar_modo(valor):
    limpar_tela()

def limpar_tela():
    resultado_verificado.configure(text="")
    resultado_verificado.pack_forget()
    label_img.pack_forget()
    final.configure(text="")

def limpar_resultado_verificacao():
    resultado_verificado.configure(text="")
    resultado_verificado.pack_forget()

def resetar_tela():
    limpar_resultado_verificacao()
    # limpa textos
    final.configure(text="")
    # esconde widgets visuais
    label_img.pack_forget()
    resultado_verificado.pack_forget()

def verificar_dispositivo():
    
    # 1. NS digitado
    ns_digitado = campo_ns.get()

    # 2. Dados do USB
    modelo_extraido, ns_dispositivo = verificar_leitor_usb()

    # 🔧 NORMALIZAÇÃO OBRIGATÓRIA
    ns_digitado = str(ns_digitado).strip()
    ns_dispositivo = str(ns_dispositivo).strip()

    resultado_verificado.pack(pady=10)

    if modelo_extraido == Modelo and ns_dispositivo == ns_digitado:
        resultado_verificado.configure(
            text=(
                "✅ Dispositivo válido\n\n"
                f"Modelo: {modelo_extraido}\n"
                f"N/S: {ns_dispositivo}"
            ),
            fg_color="green",
            font=("Arial", 16, "bold"),
            text_color="cornsilk2"
        )
    elif ns_digitado == "":
        resultado_verificado.configure(
            text=(
                "Informações do Dispositivo:\n"
                f"Modelo: {modelo_extraido}\n"
                f"N/S: {ns_dispositivo}\n Insira o N/S, desconecte, conecte e verifique!"
            ),
            fg_color="blue",
            font=("Arial", 16, "bold"),
            text_color="cornsilk2"
        )
    else:
        resultado_verificado.configure(
            text=("❌ Dispositivo não Configurado\n\n"f"N/S esperado: {ns_digitado}\n"f"N/S encontrado: {ns_dispositivo}\n"f"Modelo: {modelo_extraido}"),
            fg_color="red",
            font=("Arial", 16, "bold"),
            text_color="cornsilk2"
        )
#''''''''''''''''''''''''''''''

# reage à troca Produção/Expeção Final
def ao_mudar_modo(valor):
    if valor == "Expeção Final":
        campo_ns.delete(0, "end")
        campo_ns.focus()
        app.configure(fg_color=COR_EXPEDIÇÃO)
        label_img.pack_forget()
        final.configure(text="")
        alerta_expedicao.configure(text="⚠️ Você está na Expedição Final, nenhum dispositivo será configurado")
        alerta_expedicao.pack(side="bottom", pady=10)

        resultado_verificado.configure(text="")
        botao_verificar.configure(text='Verificação Final')
    else:
        campo_ns.delete(0, "end")
        campo_ns.focus()
        alerta_expedicao.pack_forget()
        label_img.pack(pady=20)
        app.configure(fg_color=COR_PRODUCAO)
        botao_verificar.configure(text='Verificar Dispositivo')
     # sempre reseta tudo
    resetar_tela()

    # se quiser, aqui você decide o que volta em Produção
    if valor == "Produção":
        pass  # por enquanto não mostra nada automaticamente

# '''''''''''''RESET''''''''''''''''''''''
def mostrar_reset_fabrica():
    janela_reset = ctk.CTkToplevel(app, fg_color='white')
    janela_reset.title("Reconfiguração de Fábrica")
    janela_reset.geometry("400x290")
    janela_reset.resizable(False, False)
#FORÇAR JANELA NA FRENTE
    janela_reset.attributes("-topmost", True)
    janela_reset.lift()
    janela_reset.focus_force()

    caminho_img = os.path.join("assets", "reset.jpeg")
    img = Image.open(caminho_img)

    img_ctk = ctk.CTkImage(
        light_image=img,
        size=(400, 300)
    )
    label_img = ctk.CTkLabel(janela_reset, image=img_ctk, text="")
    label_img.image = img_ctk  # mantém referência
    label_img.pack(pady=10)
#'''''''''''''''''''''''''''''''''

# Aparência
ctk.set_appearance_mode('light')

# Janela
app = ctk.CTk()
app.title(f'Configurador {Modelo}')
app.geometry('500x600')
app.iconbitmap(caminho_recurso("assets/configurator_code.ico"))


# fundo da janela continua funcionando
app.configure(fg_color=COR_PRODUCAO)

# carrega a imagem com transparência
img_fundo = ctk.CTkImage(
    Image.open(caminho_recurso("assets/logo.png")),
    size=(150, 100)  # mesmo tamanho da janela
)

label_fundo = ctk.CTkLabel(
    app,
    image=img_fundo,
    text=""
)

# IMAGEM posiciona como fundo
label_fundo.place(x=0, y=220, relwidth=1, relheight=1)
label_fundo.lower()  # 👈 joga a imagem para trás



modo_operacao = ctk.StringVar(value="Produção")
# Label produto
label_produto = ctk.CTkLabel(app, text=Modelo, font=("Microsoft Yi Baiti", 22, "underline"))
label_produto.pack(pady=5)
label_fundo.image = img_fundo

botao_reset = ctk.CTkButton(
    app,
    text="⚙️ Reset",
    width=80,
    height=30,
    fg_color="#555555",
    hover_color="#777777",
    font=("Arial", 12, "bold"),
    command=mostrar_reset_fabrica
)


# Canto superior direito RESET DE FABRICA
botao_reset.place(
    relx=0.98,
    rely=0.02,
    anchor="ne"
)


alerta_expedicao = ctk.CTkLabel(
    app,
    text="",
    font=("Segoe UI", 14, "bold"),
    text_color="white",
    fg_color="#232583",      # vermelho alerta
    corner_radius=8,
    padx=10,
    pady=5
)

# Botão Produção | Expeção Final COM command
modo_selector = ctk.CTkSegmentedButton(
    app,
    values=["Produção", "Expeção Final"],
    variable=modo_operacao,
    command=ao_mudar_modo,
    font=("Segoe UI Black", 14),
    selected_color="navy",
    selected_hover_color="dodgerblue4", fg_color="dodgerblue4", unselected_color="dodgerblue4"
)
modo_selector.pack(pady=10)

# Label NS
label_ns = ctk.CTkLabel(app, text='Número de série:', font=("Segoe UI Symbol", 20))
label_ns.pack(pady=10)

# Entry
campo_ns = ctk.CTkEntry(app, width=250, height=35, font=("Arial", 20, "bold"))
campo_ns.pack(pady=5)

campo_ns.bind("<Return>", ao_pressionar_enter)

# Botão verificar
botao_verificar = ctk.CTkButton(
    app,
    text='Verificar Dispositivo',
    fg_color='navy',
    font=("Arial", 16, "bold"),
    text_color="cornsilk2",
    command=lambda: (
        verificar_dispositivo(),
        campo_ns.delete(0, "end"),
        campo_ns.focus()
    )
)
botao_verificar.pack(pady=10)

# Imagem do QR
label_img = ctk.CTkLabel(app, text="", width=200, height=200)
label_img.pack(pady=20)

# Resultado
resultado_verificado = ctk.CTkLabel(app, text='')
resultado_verificado.pack(pady=10)

# Mensagem final
final = ctk.CTkLabel(app, text='')
final.pack(pady=5)

#  garante estado inicial correto
ao_mudar_modo(modo_operacao.get())
app.after(100, campo_ns.focus)
app.mainloop()