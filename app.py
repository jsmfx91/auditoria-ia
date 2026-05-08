from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# ¡OJO A ESTA LÍNEA! Si creaste una clave nueva, ponla aquí dentro.
# Si sigue siendo la misma, déjala como está.
genai.configure(api_key="AIzaSyB_ckCFc0Y3J1ZZc9IBJvutNZcwUzvvbWY")
model = genai.GenerativeModel('gemini-pro')

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "No has puesto una URL"}), 400
    
    if not url.startswith('http'):
        url = 'https://' + url

    try:
        # 1. Intentamos leer la web como si fuéramos un navegador real
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status() # Esto nos avisa si la web da error 404
        
        sopa = BeautifulSoup(res.text, 'html.parser')
        contenido = sopa.get_text()[:3000]
        
        # 2. Intentamos hablar con la IA
        prompt = f"Analiza la web: {url}. Contenido: {contenido}. Dime 3 fallos y 1 consejo de ventas. Sé breve."
        respuesta_ia = model.generate_content(prompt)
        
        return jsonify({"informe": respuesta_ia.text})
    
    except requests.exceptions.RequestException as error_web:
        # Si el error es al leer la web, nos lo dirá aquí
        return jsonify({"error": f"Fallo al leer la web: {str(error_web)}"}), 500
        
    except Exception as error_ia:
        # Si el error es de la clave API o de Google, nos lo dirá aquí
        return jsonify({"error": f"Fallo en la Inteligencia Artificial: {str(error_ia)}"}), 500

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
