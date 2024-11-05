from google.cloud import storage
from google.cloud import bigquery
from dotenv import load_dotenv
from io import BytesIO
import os
import time
import random
import pandas as pd

def get_environments():
    # Define o caminho para o arquivo .env na pasta config
    env_path = os.path.join(os.getcwd(), "config", ".env")
    
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv(env_path)

    # Resgata as variáveis de ambiente
    google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")
    model_name = os.getenv("MODEL_NAME")
    folder_xlsx = os.getenv("FOLDER_XLSX")
    authenticator_login = os.getenv("AUTHENTICATOR_LOGIN")

    # Configura a variável de ambiente do Google Application Credentials
    if google_credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path

    return {
        "google_credentials_path": google_credentials_path,
        "project_id": project_id,
        "location": location,
        "model_name": model_name,
        "folder_xlsx": folder_xlsx,
        "authenticator_login": authenticator_login
    }


def obter_extensao_arquivo(file_name: str) -> str:
    """
    Retorna a extensão do arquivo se for .docx ou .pdf, caso contrário retorna None.

    Args:
        file_name: Nome do arquivo a ser validado.

    Returns:
        str: A extensão do arquivo se for válida, None caso contrário.
    """
    if file_name.lower().endswith(('.docx', '.pdf')):
        return file_name.split('.')[-1]  # Retorna a extensão
    return None


def excel_to_dataframe(file_path):
    # Lê o arquivo Excel e carrega todas as planilhas em um dicionário
    df = pd.read_excel(file_path, sheet_name="Export")
    return df


