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
    # Caminho correto para .py e para .exe
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

#######################____Ajustes de tela e config___#########
def centralizar_janela(janela, largura, altura):
    # Obtém a largura e altura da tela do computador
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Calcula a posição X e Y para o canto superior esquerdo da janela
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2) - 50

    # Define a geometria: "Largura x Altura + PosX + PosY"
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")


Modelo = carregar_modelo()
Fabricante = "CUSTOM"
COR_PRODUCAO = "white"
COR_EXPEDIÇÃO= "white" 

#_________________________________________________________________
def liberar_modos():
    modo_selector.configure(state="normal") # Ativa o seletor
    modo_selector.pack(pady=10, after=label_produto)


def caminho_recurso(relativo):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relativo)
    return os.path.join(os.path.abspath("."), relativo)
####__________________Limpeza__________
def limpar_tela():
    btn_voltar_firmware.pack_forget()
    label_img.pack_forget()
    barra_img.pack_forget()
    final.pack_forget()
    campo_ns.delete(0, "end")
    campo_ns.focus()
    alerta_expedicao.pack_forget()
    resultado_verificado.configure(text="")
    resultado_verificado.pack_forget()
    label_img.pack_forget()
    final.configure(text="")
    botao_verificar.pack_forget()
    label_info.pack_forget()

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

####################VALIDAR PARA CONFIGURAR OU VERIFICAR DEPOIS
def ler_firmware():
    ns = campo_ns.get().strip()
    VERSAO_CORRETA = '809004: 88BA0501006.'
    
    resultado_verificado.pack(pady=10)

    if ns == VERSAO_CORRETA:
        campo_ns.configure(state="disabled")
        resultado_verificado.configure(
            text="\n✅ Firmware Válido\n",
            fg_color="green", text_color="white", width=150, height=50
        )
        
        # LIBERA OS BOTÕES DE NAVEGAÇÃO (O SegmentedButton)
        liberar_modos() 
        
        # Avisar o usuário
        final.configure(text="Escolha o próximo passo acima ↑", text_color="green")
        final.pack()
        
    elif len(ns) != VERSAO_CORRETA and len(ns) > 0:
        resultado_verificado.configure(
            text="\n❌ Firmware Incorreto\n",
            fg_color="red", text_color="white", width=150, height=50
        )
        modo_selector.pack_forget() # Esconde se errar

    else:
        resultado_verificado.pack_forget()

def resetar_para_firmware():
    # 1. Primeiro, atualizamos a variável de controle visual
    modo_operacao.set("Validar Firmware")
    # 2. Chama a função de mudança de modo, passando apenas a string
    ao_mudar_modo("Validar Firmware")
    modo_selector.configure(state="disabled")
    # Volta para o modo inicial
    modo_selector.pack_forget()
    btn_voltar_firmware.pack_forget()
    campo_ns.delete(0, "end")
    campo_ns.focus()
############################################################

def verificar_dispositivo():
    resultado_verificado.configure(text="Verificando...", text_color="purple", fg_color="transparent", width=150, height=100)
    resultado_verificado.pack(pady=5)
    app.update_idletasks()
    
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
        btn_voltar_firmware.pack(pady=10)
    elif ns_digitado == "":
        resultado_verificado.configure(
            text=(
                "Informações do Dispositivo:\n"
                f"Modelo: {modelo_extraido}\n"
                f"N/S: {ns_dispositivo}\n Insira o N/S,desconecte, conecte e verifique!"
            ),
            fg_color="blue",
            font=("Arial", 16, "bold"),
            text_color="cornsilk2"
        )
    else:
        resultado_verificado.configure(
            text=("❌ Dispositivo inválido\n\n"f"N/S esperado: {ns_digitado}\n"f"N/S encontrado: {ns_dispositivo}\n"f"Modelo: {modelo_extraido}"),
            fg_color="red",
            font=("Arial", 16, "bold"),
            text_color="cornsilk2"
        )
#''''''''''''''''''''''''''''''

# reage à troca Produção/Expeção Final/Validar Firmeware
def ao_mudar_modo(valor):
    limpar_tela()

    if valor == "Validar Firmware":
        ns = campo_ns.get()
        limpar_tela()
        barra_img.pack(pady=20)
        app.configure(fg_color=COR_PRODUCAO)
        trace_id = var_monitorada.trace_add("write", lambda *args: ler_firmware())
        campo_ns.configure(textvariable=var_monitorada)
        label_ns.configure(text="Escaneie o código de barras:")
        modo_selector.pack_forget()
        campo_ns.configure(state="normal")
        label_info.pack(pady=5)

    else:
        barra_img.pack_forget()
        liberar_modos()
        label_ns.configure(text='Numero de série:')
        campo_ns.configure(state="normal")
        limpar_tela()
        modo_selector.pack(pady=10, after=label_produto) 

        if valor == "Expeção Final":
            campo_ns.delete(0, "end")
            campo_ns.focus()
            app.configure(fg_color=COR_EXPEDIÇÃO)
            alerta_expedicao.configure(text="⚠️ Você está na Expedição Final, nenhum dispositivo será configurado")
            alerta_expedicao.pack(side="bottom", pady=10)
            campo_ns.configure(textvariable="")
        
        else:
            campo_ns.delete(0, "end")
            campo_ns.focus()
            alerta_expedicao.pack_forget()
            label_img.pack(pady=20)
            app.configure(fg_color=COR_PRODUCAO)
            final.pack(pady=5)
            campo_ns.configure(textvariable="") 


     # sempre reseta tudo
    resetar_tela()

def ao_pressionar_enter(event):
    btn_voltar_firmware.pack_forget()
    app.update_idletasks()
    modo = modo_operacao.get()
    

    if modo == "Expeção Final":
        # ENTER vira "clicar no verificar"
        verificar_dispositivo()
        campo_ns.delete(0, "end")
        campo_ns.focus()
    elif modo == "Validar Firmware":

        ler_firmware()
        campo_ns.delete(0, "end")
        campo_ns.focus()
    else:
        # Produção: ENTER gera o Datamatrix
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
# Define o tamanho da janEla
largura_app = 550
altura_app = 650

# Chama a função para centralizar
centralizar_janela(app, largura_app, altura_app)
app.iconbitmap(caminho_recurso("assets/configurator_code.ico"))


# fundo da janela continua funcionando
app.configure(fg_color=COR_PRODUCAO)

# carrega a imagem com transparência
img_fundo = ctk.CTkImage(
    Image.open(caminho_recurso("assets/logo.png")),
    size=(150, 80)  # mesmo tamanho da janela
)

label_fundo = ctk.CTkLabel(
    app,
    image=img_fundo,
    text=""
)

# IMAGEM posiciona como fundo
label_fundo.place(x=0, y=220, relwidth=1, relheight=1)
label_fundo.lower()  # 👈 joga a imagem para trás

modo_operacao = ctk.StringVar(value="Validar Firmware")

# Label produto
label_produto = ctk.CTkLabel(app, text=Modelo, font=("Microsoft Yi Baiti", 22, "underline", "bold"))
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
    fg_color="#232583",
    corner_radius=8,
    padx=10,
    pady=5
)

# Botão Validar firmware  Produção | Expeção Final COM command
modo_selector = ctk.CTkSegmentedButton(
    app,
    values=["Validar Firmware", "Produção", "Expeção Final"],
    variable=modo_operacao,
    command=ao_mudar_modo,
    state="disabled", #Começa bloqueado
    font=("Arial", 12, "bold"),
    selected_color="navy",
    selected_hover_color="dodgerblue4", fg_color="dodgerblue4", unselected_color="dodgerblue4"
)
#modo_selector.pack(pady=10)

# Label NS
label_ns = ctk.CTkLabel(app, text='Número de série:', font=("Segoe UI Symbol", 20))
label_ns.pack(pady=10)

# Entry
var_monitorada = ctk.StringVar()
trace_id = None # Guardará o ID do rastreador para poder ligar/desligar


campo_ns = ctk.CTkEntry(
    app, 
    width=250, 
    height=35, 
    font=("Arial", 20, "bold"),
)
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

label_info = ctk.CTkLabel(app, text="Valide o Firmware, escaneando o código acima\n (Com o firmware inválido não é possível iniciar outra etapa)", font=("Arial", 12))

#imagem do Codigo Firmware
img_objeto = ctk.CTkImage(Image.open(caminho_recurso("assets/imagem.png")), size=(380, 150))
barra_img = ctk.CTkLabel(app, image=img_objeto, text="")


btn_voltar_firmware = ctk.CTkButton(
    app, 
    text="↺ Validar Novo Firmware", 
    command=lambda: resetar_para_firmware(),
    fg_color="#056123",
    hover_color="#337948",
    font=("Arial", 14, "bold")
)

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