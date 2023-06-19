#importação das bibliotecas
import os
import time
from flask import Flask, request
from supabase import create_client, Client
#criação de um servidor em Pyhton
app = Flask(__name__)
# Chave de acesso ao supabase
url = "https://qycjcdntwivlombvmwsf.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF5Y2pjZG50d2l2bG9tYnZtd3NmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4NzE5NTY4NywiZXhwIjoyMDAyNzcxNjg3fQ.KmlbtEVcN9gZOsC1TgwcNhuq23q8rFaMuOcfcgPEUkg"
# Cria o cliente para conectar na API do supabase
supabase: Client = create_client(url, key)
# Seta o nome do bucket criado na URL em questão
bucket_name = "images"
# Rota para realizar upload de imagens
@app.route("/mandar", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        # Pega o arquivo correspondente ao upload que o usuário realizou via interface
        image = request.files["image"]
        # Lê o arquivo de imagem recebido pelo front
        data = image.read()
        # Cria um padrão de nome para as imagens enviadas
        filename = f"{time.time()}_{image.filename}"
        # Envia a imagem para o bucket do supabase
        response = supabase.storage.from_(bucket_name).upload(filename, data)
        print(response)
        # Confere se o upload foi concretizado
        if response.status_code == 200:
            return "A imagem foi enviada com sucesso."
        else:
            return "O upload da imagem falhou."

    # Retornando o HTML fornecido
    return '''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ponderada 4</title>
    <style>
        /* Estilização do input */
        input[type="file"] {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f8f8f8;
            color: #333;
            font-size: 16px;
            margin-bottom: 10px;
        }
        
        /* Estilização do botão de submit */
        input[type="submit"] {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        
        /* Estilização do botão de submit quando o mouse passa por cima */
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>Envie sua imagem aqui</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="image">
        <input type="submit" value="Enviar">
    </form>
</body>
</html>

    '''

if __name__ == '__main__':
    app.run(debug=True)
