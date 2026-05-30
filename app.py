import os
from flask import Flask, request, jsonify
from pypdf import PdfReader
import requests

app = Flask(__name__)

# Configuración (Usa variables de entorno en producción)
API_KEY = "OPENAI_API_KEY"
PDF_PATH = "Numerologia_Pitagorica_Cuadro_Numerologi.pdf"

def extraer_texto_pdf(archivo):
    reader = PdfReader(archivo)
    return "".join([page.extract_text() for page in reader.pages])

def consultar_openai(numero, tipo):
    texto_libro = extraer_texto_pdf(PDF_PATH)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "Eres un experto numerólogo."},
            {"role": "user", "content": f"Basado en este texto: {texto_libro[:12000]}... Interpreta el {tipo} número {numero}."}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    fecha = data.get("fecha") # Ejemplo: "25-11-1973"
    # Aqui iria tu logica matematica que ya calculamos antes
    # Por ahora, para probar, llamamos directo a la IA
    resultado = consultar_openai(11, "Camino de Vida") 
    return jsonify({"respuesta": resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)