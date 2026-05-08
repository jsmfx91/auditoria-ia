from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Tu clave ya integrada
genai.configure(api_key="AIzaSyB_ckCFc0Y3J1ZZc9IBJvutNZcwUzvvbWY")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL no proporcionada"}), 400
    
    try:
        # El agente visita la web
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        sopa = BeautifulSoup(res.text, 'html.parser')
        contenido = sopa.get_text()[:3000] # Limite de texto para rapidez
        
        # El agente genera el informe de dinero
        prompt = f"Analiza esta web: {url}. Contenido: {contenido}. Dime 3 fallos de SEO/Ventas y un consejo para ganar dinero rápido con esta web. Sé breve."
        respuesta_ia = model.generate_content(prompt)
        
        return jsonify({"informe": respuesta_ia.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Esto permite que Render asigne el puerto automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)