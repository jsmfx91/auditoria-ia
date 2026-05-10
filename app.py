from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

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
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=12)
        res.raise_for_status()
        contenido = BeautifulSoup(res.text, 'html.parser').get_text(separator=' ', strip=True)[:2000]

        # 2. AUTO-DESCUBRIMIENTO DE MODELO (Solución anti-bloqueos)
        url_lista = f"https://generativelanguage.googleapis.com/v1beta/models?key={LLAVE_MAESTRA}"
        res_lista = requests.get(url_lista).json()
        
        if 'error' in res_lista:
            return jsonify({"error": f"Error de autenticación de Google: {res_lista['error']['message']}"}), 500
            
        modelos_disponibles = []
        if 'models' in res_lista:
            # Filtramos solo los modelos que generan texto
            modelos_disponibles = [m['name'] for m in res_lista['models'] if 'generateContent' in m.get('supportedGenerationMethods', [])]
        
        if not modelos_disponibles:
            return jsonify({"error": "Tu clave de Google está restringida por región y no tiene modelos de texto asignados."}), 500

        # Seleccionamos el mejor modelo que Google te permita usar
        modelo_elegido = modelos_disponibles[0] 
        opciones_top = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-1.0-pro", "models/gemini-pro"]
        for opc in opciones_top:
            if opc in modelos_disponibles:
                modelo_elegido = opc
                break

        # 3. CONEXIÓN CON EL MODELO EXACTO APROBADO
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/{modelo_elegido}:generateContent?key={LLAVE_MAESTRA}"
        
        prompt = f"Analiza esta web: {url}. Contenido: {contenido}. Dime 3 fallos graves y 1 consejo de ventas. Sé profesional y breve."
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        respuesta = requests.post(gemini_url, json=payload, headers={'Content-Type': 'application/json'})
        datos = respuesta.json()
        
        if 'error' in datos:
            return jsonify({"error": f"Fallo al usar {modelo_elegido}: {datos['error']['message']}"}), 500
            
        informe = datos['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"informe": informe})

    except Exception as e:
        return jsonify({"error": f"Error del sistema: {str(e)}"}), 500

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
