# **Upload e Processamento de HTML - FastAPI e React**
## **Descrição**
Esta aplicação permite que um usuário envie um arquivo HTML para o back-end, onde ele será processado e, neste caso, retornará o charset do arquivo HTML. A aplicação é composta por um servidor FastAPI (back-end) e uma interface React (front-end).

## **Como rodar a aplicação**

### **1. Rodando o Back-End (FastAPI)**
Navegue até o diretório onde o back-end está localizado.
Instale as dependências necessárias:
`pip install -r requirements.txt`
Execute o servidor FastAPI:
`uvicorn main:app --host 127.0.0.1 --port 8000`
O back-end estará disponível em http://localhost:8000. Caso você tenha que executar em alguma outra porta, é necessário atualizar também o arquivo `frontend\src\api.ts`:
`baseURL: "http://localhost:{porta utilizada}"`

### **2. Rodando o Front-End (React)**
Navegue até o diretório onde o front-end está localizado.
Instale as dependências necessárias:
`npm install`
Execute o servidor de desenvolvimento React:
`npm run dev --port 5173`
O front-end estará disponível em http://localhost:5173. Caso você tenha que executar em alguma outra porta, é necessário atualizar também no arquivo `backend\main.py`:
`origins = ["http://localhost:{porta utilizada}"]`

3. Acessando a Aplicação
Abra o navegador e acesse http://localhost:{porta utilizada}
No front-end, será possível selecionar um arquivo HTML e enviá-lo para o servidor.
O back-end processará o arquivo e retornará o charset, que será mostrado no front-end.
