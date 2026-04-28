import subprocess
import re

def verificar_leitor_usb():
    comando = '''
    Get-PnpDevice -PresentOnly | Where-Object {
        $_.InstanceId -like "*VID_060C*PID_0660*"
    } | ForEach-Object {
        $props = Get-PnpDeviceProperty -InstanceId $_.InstanceId

        [PSCustomObject]@{
            Descricao   = ($props | Where-Object KeyName -like '*DeviceDesc*').Data
            InstanceId  = $_.InstanceId
        }
    }
    '''

    proc = subprocess.run(
        ["powershell", "-Command", comando],
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    texto = proc.stdout

    # 🔎 pega descrição entre {}
    desc_match = re.search(r"\{(.+?)\}", texto)

    # 🔎 pega NS corretamente
    instance_match = re.search(
        r"USB\\VID_060C&PID_0660\\([^\s\r\n]+)",
        texto
    )

    if desc_match and instance_match:
        descricao_completa = desc_match.group(1).strip()

        # pega só o modelo (após vírgula)
        partes = descricao_completa.split(",")
        modelo = partes[-1].strip()

        ns = instance_match.group(1).strip()

        return modelo, ns

    return None, None