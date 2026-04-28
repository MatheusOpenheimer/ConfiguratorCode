import subprocess
from PIL import Image
import customtkinter as ctk
import os
import sys

def caminho_recurso(relativo):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relativo)
    return os.path.join(os.path.abspath("."), relativo)

def gerar_datamatrix(campo_ns, label_img, botao_verificar, final, app, Fabricante, Modelo, limpar_verificacao):
    final.configure(text='')

    limpar_verificacao()

    ns = campo_ns.get().strip()
    if not ns:
        return

    codigo = f"802002{Fabricante};802000{Modelo};811005{ns}."

    # Caminhos corretos
    caminho_img = caminho_recurso("assets/codigo.png")
    zint_path = caminho_recurso("zint/zint.exe")

    resultado = subprocess.run(
        [
            zint_path,
            "-b", "71",
            "--square",
            "-d", codigo,
            "--init",
            "--scale", "10",
            "-o", caminho_img
        ],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    if resultado.returncode != 0:
        print("Erro no Zint:", resultado.stderr)
        return

    try:
        img = Image.open(caminho_img)
    except Exception as e:
        print("Erro ao abrir imagem:", e)
        return

    label_img.pack(pady=10)
    ctk_img = ctk.CTkImage(light_image=img, size=(200, 200))
    label_img.configure(image=ctk_img)
    label_img.image = ctk_img

    botao_verificar.pack(pady=10)

    def mostrar_mensagem():
        final.configure(
            text="Desconecte o USB e conecte novamente",
            font=("Arial", 14, "bold"),
            text_color="purple4"
        )
    
    app.after(6000, mostrar_mensagem)