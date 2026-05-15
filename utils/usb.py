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

    modelo_match = re.search(r"(CBR2D-V)", texto)
    instance_match = re.search(
        r"USB\\VID_060C&PID_0660\\([^\r\n]+)",
        texto
    )

    if modelo_match and instance_match:
        return modelo_match.group(1), instance_match.group(1)

    return None, None