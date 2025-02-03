from fastapi import FastAPI, File, UploadFile

# Middleware do FastAPI para controlar as permissões de CORS (Cross-Origin Resource Sharing). Isso permite configurar DE QUAIS domínios ou portas o servidor pode receber requisições
from fastapi.middleware.cors import CORSMiddleware

# Utilizado para manipulação dos diretórios
import os 

# Módulo para manipulação de arquivos. Aqui está sendo utilizado para copiar o arquivo recebido, salvando-o
import shutil

# Para processar o html
from bs4 import BeautifulSoup

import time
import hashlib

def generate_unique_filename(filename):
    timestamp = str(int(time.time()))  # Gera um timestamp único
    hash_str = hashlib.md5(filename.encode()).hexdigest()  # Gera um hash do nome do arquivo
    return f"{timestamp}_{hash_str}_{filename}"



app = FastAPI()

UPLOAD_DIR = "uploads"


# Define as origens de onde pode receber requisições
origins = [
    "http://localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'], # Permite todos os métodos HTTP (desnecessario aqui).
    allow_headers=['*'] # Permite todos os cabeçalhos nas requisições (desnecessario aqui)
)


# a palavra-chave async nas funções de endpoint permite que a função seja executada de maneira assíncrona, sem bloquear outras requisições.
# Essa é uma das vantagens da FastAPI, que já suporta programação assíncrona nativamente

@app.post(path="/upload/")
async def upload_html(file: UploadFile = File(...)):
    """Recebe um arquivo HTML e salva no servidor"""
    
    # Garante que o diretório de uploads existe
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Caminho para salvar o arquivo
    file_path = os.path.join(UPLOAD_DIR, generate_unique_filename(file.filename))
    
    # Salva o arquivo no servidor
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    

    # PROCESSA O ARQUIVO
    with open(file_path, "r", encoding="utf-8") as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, "html.parser")
        
        # Procura pelas tags <meta>, que define o charset
        meta_tags = soup.find_all("meta") # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find
        
        found_charset = False

        # Vai tentando encontrar o charsert
        for meta_tag in meta_tags:
            if "charset" in meta_tag.attrs["content"]:
                charset = meta_tag.attrs["content"]
                found_charset = True
                break
        
        if not found_charset:
           charset = "Charset não encontrado"

    return {"filename": file.filename, "charset": charset,  "message": "Upload realizado com sucesso"}





