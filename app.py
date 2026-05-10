from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

# Recupera la clave de la variable de entorno de Render
LLAVE_MAESTRA = os.environ.get("GEMINI_KEY")

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    url = data.get('url')
    
    if not url: return jsonify({"error": "Falta URL"}), 400
    if not LLAVE_MAESTRA: return jsonify({"error": "Falta GEMINI_KEY en Render"}), 500

    if not url.startswith('http'):
        url = 'https://' + url

    try:
        # 1. Leer la web
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        contenido = BeautifulSoup(res.text, 'html.parser').get_text()[:2500]
        
        # 2. CONEXIÓN A LA API ESTABLE v1 (La que funciona ahora)
        # Hemos cambiado v1beta por v1 y el modelo al nombre oficial
        gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={LLAVE_MAESTRA}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Analiza esta web: {url}. Contenido: {contenido}. Dime 3 fallos y 1 consejo de ventas. Sé profesional y breve."}]}]
        }
        
        respuesta = requests.post(gemini_url, json=payload)
        datos = respuesta.json()
        
        # Si Google da error, nos dirá el motivo
        if 'error' in datos:
            return jsonify({"error": f"Google dice: {datos['error']['message']}"}), 500
            
        informe = datos['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"informe": informe})

    except Exception as e:
        return jsonify({"error": f"Error técnico: {str(e)}"}), 500

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
