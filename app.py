from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

# Tu clave API
LLAVE_MAESTRA = "AIzaSyAuj1QSKF9NRlMzgar0yPe48wqKFk-pE3g"

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "No has puesto una URL"}), 400
    
    if not url.startswith('http'):
        url = 'https://' + url

    try:
        # 1. Leer la web simulando un navegador
        headers_web = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers_web, timeout=15)
        res.raise_for_status() 
        
        sopa = BeautifulSoup(res.text, 'html.parser')
        contenido = sopa.get_text()[:3000]
        
        # 2. CONEXIÓN DIRECTA Y BLINDADA A LA IA (Sin librerías conflictivas)
        prompt = f"Analiza la web: {url}. Contenido: {contenido}. Dime 3 fallos y 1 consejo de ventas. Sé profesional y directo."
        
        # Usamos el enlace directo oficial de Google
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={LLAVE_MAESTRA}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        respuesta_ia = requests.post(gemini_url, headers={'Content-Type': 'application/json'}, json=payload)
        datos_ia = respuesta_ia.json()
        
        # Comprobar si Google da algún error
        if 'error' in datos_ia:
            return jsonify({"error": f"Respuesta de Google: {datos_ia['error']['message']}"}), 500
            
        informe = datos_ia['candidates'][0]['content']['parts'][0]['text']
        
        return jsonify({"informe": informe})
    
    except requests.exceptions.RequestException as error_web:
        return jsonify({"error": "Fallo al leer la web. Prueba con otra sin bloqueos."}), 500
        
    except Exception as error_general:
        return jsonify({"error": f"Error del sistema: {str(error_general)}"}), 500

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
