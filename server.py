import os
from os.path import join
from pathlib import Path
from smbclient import register_session, remove, copyfile, scandir
from dotenv import load_dotenv
import paramiko
from datetime import datetime
import schedule
import time

# Carrega as variáveis de ambiente do diretório atual (src/)
dotenv_path = join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Seta as variáveis do servidor de arquivos Windows
server = os.environ.get("SERVER")
username = os.environ.get("USER")
password = os.environ.get("PASSWD")
inn = os.environ.get("INN")
out = os.environ.get("OUT")
out = os.environ.get("OUT")
lidos = os.environ.get("LIDOS")
extension = os.environ.get("EXTENSION")

# Registra a conexão do servidor de arquivos Windows
register_session(server, username=username, password=password)

# Lista os arquios para serem copiados da pasta de origem
def listar_arquivos():
    files = []
    for file in scandir(inn):
        if file.is_file():
            # Valida se a extensão do arquivo é de um arquivo válido para upload, no caso .xml
            if Path(file.name).suffix == extension:
                files.append(file.name)
    
    # Caso não exista arquivos para copiar, exibe mensagem de aviso
    if not files:
        h = datetime.now()
        print(h.strftime("%d/%m/%Y %H:%M:%S") + " Nenhum arquivo para ser copiado.")

    return files 

def mover_arquivos(files, src, dst):
    for file in files:
        h = datetime.now()
        print(h.strftime("%d/%m/%Y %H:%M:%S") + " Copiando o arquivo: " + src + file + " para " + dst + file)
        copyfile(src + file, dst + file)

def remover_arquivos(files, src):
    for file in files:
        h = datetime.now()
        print(h.strftime("%d/%m/%Y %H:%M:%S") + " Removendo o arquivo: " + src + file)
        remove(src + file)

def upload(files, src):
    # Cria o cliente SSH
    ssh_client = paramiko.SSHClient()

    # Seta as credenciais do SFTP 
    ftp_host = os.environ.get("FTP_HOST")
    ftp_username = os.environ.get("FTP_USER")
    ftp_password = os.environ.get("FTP_PASS")
    ftp_port = os.environ.get("FTP_PORT")
    ftp_path = os.environ.get("FTP_PATH")

    # Confia automaticamente no tráfego com o servidor remoto
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Realiza a conexão
    ssh_client.connect(hostname=ftp_host, port=ftp_port, username=ftp_username, password=ftp_password)

    # Cria o Objeto SFTP
    ftp = ssh_client.open_sftp()

    for file in files:
        h = datetime.now()
        print(h.strftime("%d/%m/%Y %H:%M:%S")  + " Uploading: " + src + file + " para: " + ftp_path + file)
        ftp.put(src + file, ftp_path + file)

    # Fecha a conexão
    ftp.close()
    ssh_client.close()

# ------------------------------------------------------------------------------------------- #
def job():
    # 1. Lista todos arquivos para serem copiados
    files = listar_arquivos()

    # 2. Mover da pasta inn para out
    mover_arquivos(files, inn, out)

    # 3. Remove os arquivos da pasta inn
    remover_arquivos(files, inn)

    # 4. Realiza o upload dos arquivos
    upload(files, out)

    # 5. Copia os arquivos da pasta out para lidos, após upload
    mover_arquivos(files, out, lidos)

    # 6. Remove os arquivos da pasta out
    remover_arquivos(files, out)
# ------------------------------------------------------------------------------------------- #

job()