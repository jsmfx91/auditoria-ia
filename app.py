from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

# La clave se extrae de forma segura desde el panel de Render
LLAVE_MAESTRA = os.environ.get("GEMINI_KEY")

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.json
    url = data.get('url')
    
    # Validaciones iniciales de seguridad
    if not url: 
        return jsonify({"error": "Falta URL"}), 400
    if not LLAVE_MAESTRA: 
        return jsonify({"error": "Falta configurar GEMINI_KEY en Render"}), 500

    if not url.startswith('http'):
        url = 'https://' + url

    try:
        # 1. Extracción de contenido web con evasión de bloqueos básicos
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        res = requests.get(url, headers=headers, timeout=12)
        res.raise_for_status()
        
        # Limpieza profesional del texto para no saturar a la IA
        contenido = BeautifulSoup(res.text, 'html.parser').get_text(separator=' ', strip=True)[:2500]
        
        # 2. Conexión a la ruta de PRODUCCIÓN EXACTA (Cero errores 404)
        gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={LLAVE_MAESTRA}"
        
        # Prompt mejorado y configuración de generación estructurada
        prompt = f"Actúa como un experto consultor de negocios y optimización web (CRO). Analiza el siguiente texto extraído de la web {url}. Identifica 3 fallos graves que les estén haciendo perder clientes y proporciona 1 consejo accionable para aumentar sus ventas. Formatea la respuesta con viñetas claras.\n\nContenido:\n{contenido}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 800
            }
        }
        
        respuesta = requests.post(gemini_url, json=payload, headers={'Content-Type': 'application/json'})
        datos = respuesta.json()
        
        # Captura de errores directos de Google
        if 'error' in datos:
            return jsonify({"error": f"API Google: {datos['error']['message']}"}), 500
            
        # Extracción del informe exitoso
        informe = datos['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"informe": informe})

    except requests.exceptions.RequestException:
        return jsonify({"error": "No se pudo acceder a la web. Es posible que tenga un escudo de seguridad activo."}), 500
    except Exception as e:
        return jsonify({"error": f"Fallo en la arquitectura: {str(e)}"}), 500

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
