from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

# La clave se lee de forma segura desde el panel de Render
LLAVE_MAESTRA = os.environ.get("GEMINI_KEY")

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    url = data.get('url')
    
    if not url: return jsonify({"error": "Falta URL"}), 400
    if not LLAVE_MAESTRA: return jsonify({"error": "Falta GEMINI_KEY en Render"}), 500
    if not url.startswith('http'): url = 'https://' + url

    try:
        # 1. Leer web
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=12)
        res.raise_for_status()
        contenido = BeautifulSoup(res.text, 'html.parser').get_text(separator=' ', strip=True)[:2000]

        # 2. Descubrir modelo disponible
        url_lista = f"https://generativelanguage.googleapis.com/v1beta/models?key={LLAVE_MAESTRA}"
        res_lista = requests.get(url_lista).json()
        
        if 'error' in res_lista:
            return jsonify({"error": f"Error de Google: {res_lista['error']['message']}"}), 500
            
        modelos_disponibles = [m['name'] for m in res_lista['models'] if 'generateContent' in m.get('supportedGenerationMethods', [])]
        
        # Seleccionamos el mejor modelo
        modelo_elegido = modelos_disponibles[0] 
        prioridad = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        for p in prioridad:
            if p in modelos_disponibles:
                modelo_elegido = p
                break

        # 3. Consultar a la IA
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/{modelo_elegido}:generateContent?key={LLAVE_MAESTRA}"
        prompt = f"Analiza esta web: {url}. Contenido: {contenido}. Dime 3 fallos graves y 1 consejo de ventas. Sé profesional y breve."
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        respuesta = requests.post(gemini_url, json=payload)
        datos = respuesta.json()
        
        informe = datos['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"informe": informe})

    except Exception as e:
        return jsonify({"error": f"Error del sistema: {str(e)}"}), 500

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
