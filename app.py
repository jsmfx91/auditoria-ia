from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

app = Flask(__name__)
# Esto permite que tu HTML hable con este servidor sin bloqueos
CORS(app)

# Configuración de tu IA con tu clave
genai.configure(api_key="AIzaSyB_ckCFc0Y3J1ZZc9IBJvutNZcwUzvvbWY")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "No has puesto una URL"}), 400
    
    # Asegurar que la URL tenga http
    if not url.startswith('http'):
        url = 'https://' + url

    try:
        # El agente visita la web
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        sopa = BeautifulSoup(res.text, 'html.parser')
        
        # Extraer texto relevante
        contenido = sopa.get_text()[:3000]
        
        # El agente razona y genera el informe
        prompt = (
            f"Analiza profesionalmente la web: {url}. "
            f"Contenido: {contenido}. "
            "Dime 3 errores específicos de SEO o diseño que les hacen perder dinero "
            "y un consejo clave. Sé directo y profesional."
        )
        
        respuesta_ia = model.generate_content(prompt)
        
        return jsonify({"informe": respuesta_ia.text})
    
    except Exception as e:
        return jsonify({"error": "La web no respondió a tiempo o es privada."}), 500

if __name__ == '__main__':
    # IMPORTANTE: Render usa un puerto dinámico, esto lo soluciona
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)