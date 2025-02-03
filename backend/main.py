from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os 
import shutil
from bs4 import BeautifulSoup


app = FastAPI()

UPLOAD_DIR = "uploads"

origins = [
    "http://localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)


# a palavra-chave async nas funções de endpoint permite que a função seja executada de maneira assíncrona, sem bloquear outras requisições.
@app.post(path="/upload/")
async def upload_html(file: UploadFile = File(...)):
    """Recebe um arquivo HTML e salva no servidor"""
    
    # Garante que o diretório de uploads existe
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Caminho para salvar o arquivo
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Salva o arquivo no servidor
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    

    # PROCESSA O ARQUIVO
    with open(file_path, "r", encoding="utf-8") as html_file:
        content = html_file.read()
        soup = BeautifulSoup(content, "html.parser")
        
        # Procura pela tag <meta> que define o charset
        meta_tags = soup.find_all("meta") # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find
        
        found_charset = False

        for meta_tag in meta_tags:
            if "charset" in meta_tag.attrs["content"]:
                charset = meta_tag.attrs["content"]
                found_charset = True
                break
        
        if not found_charset:
           charset = "Charset não encontrado"

    return {"filename": file.filename, "charset": charset,  "message": "Upload realizado com sucesso"}





