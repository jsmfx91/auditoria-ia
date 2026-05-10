from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

# EL CÓDIGO SEGURO: Busca la clave en Render, no en GitHub
LLAVE_MAESTRA = os.environ.get("GEMINI_KEY")

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    url = data.get('url')
    
    if not url or not LLAVE_MAESTRA:
        return jsonify({"error": "Configuración incompleta o falta URL"}), 400
    
    if not url.startswith('http'):
        url = 'https://' + url

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        contenido = BeautifulSoup(res.text, 'html.parser').get_text()[:2000]
        
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={LLAVE_MAESTRA}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Analiza esta web: {url}. Contenido: {contenido}. Dime 3 fallos y 1 consejo de ventas. Sé breve."}]}]
        }
        
        respuesta = requests.post(gemini_url, json=payload)
        datos = respuesta.json()
        
        if 'error' in datos:
            return jsonify({"error": "La IA no responde correctamente"}), 500
            
        informe = datos['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"informe": informe})

    except Exception:
        return jsonify({"error": "Error al procesar la web"}), 500

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
