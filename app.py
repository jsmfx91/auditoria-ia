<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Web Auditor | Business Intelligence</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #0f172a; min-height: 100vh; display: flex; align-items: center; justify-content: center; font-family: sans-serif; }
        .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 2rem; }
    </style>
</head>
<body class="p-4 sm:p-0">
    <div class="max-w-lg w-full p-6 sm:p-8 glass-card shadow-2xl mx-auto">
        <div class="text-center mb-6 sm:mb-8">
            <h1 class="text-2xl sm:text-3xl font-bold text-white mb-2">Web Auditor <span class="text-indigo-500">IA</span></h1>
            <p class="text-slate-400 text-xs sm:text-sm">Detecta fallos en tu web y deja de perder clientes.</p>
        </div>

        <div class="space-y-4">
            <input type="text" id="urlInput" placeholder="www.ejemplo.com" 
                   onkeypress="if(event.key === 'Enter') enviarAnalisis()"
                   class="w-full bg-slate-800/50 border border-slate-700 p-4 rounded-xl text-white outline-none focus:border-indigo-500 transition-all text-sm sm:text-base">
            
            <button onclick="enviarAnalisis()" id="mainBtn" 
                    class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-xl shadow-lg transition-all transform active:scale-95 text-sm sm:text-base">
                Analizar Gratis
            </button>
        </div>

        <div id="resultadoArea" class="mt-6 sm:mt-8 hidden animate-fade-in">
            <div class="p-4 sm:p-5 bg-slate-800/50 rounded-2xl border border-slate-700">
                <p id="textoInforme" class="text-slate-300 text-xs sm:text-sm leading-relaxed whitespace-pre-line"></p>
            </div>
            <button onclick="window.location.href='TU_LINK_DE_PAGO'" class="w-full mt-4 sm:mt-6 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-4 rounded-xl shadow-xl transition-all text-sm sm:text-base">
                SOLUCIONAR CON IA (19€)
            </button>
        </div>
    </div>

    <script>
        async function enviarAnalisis() {
            const urlValue = document.getElementById('urlInput').value;
            const btn = document.getElementById('mainBtn');
            const resArea = document.getElementById('resultadoArea');
            const texto = document.getElementById('textoInforme');

            if(!urlValue) return alert("Escribe una URL");

            btn.innerText = "Agente analizando...";
            btn.disabled = true;
            resArea.classList.add('hidden');

            try {
                // TU ENLACE DE RENDER
                const URL_BACKEND = "https://auditoria-ia.onrender.com/analizar";

                const response = await fetch(URL_BACKEND, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: urlValue })
                });

                const data = await response.json();
                
                if(data.informe) {
                    texto.innerText = data.informe;
                    resArea.classList.remove('hidden');
                } else {
                    alert("Error: " + (data.error || "No se pudo obtener el informe."));
                }
            } catch (err) {
                alert("El servidor está despertando o hay un error de conexión. Reintenta en unos segundos.");
            } finally {
                btn.innerText = "Analizar Gratis";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
