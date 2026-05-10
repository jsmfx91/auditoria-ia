<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>AI Web Auditor | Business Intelligence</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Fondo premium con degradado moderno */
        body { 
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); 
            min-height: 100vh; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-family: system-ui, -apple-system, sans-serif; 
            margin: 0;
            padding: 1rem;
        }
        /* Efecto cristal mejorado */
        .glass-card { 
            background: rgba(30, 41, 59, 0.6); 
            backdrop-filter: blur(16px); 
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08); 
            border-radius: 1.5rem; 
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }
        /* Animación suave para el informe */
        .fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body class="text-slate-200">
    <div class="w-full max-w-xl p-6 sm:p-10 glass-card mx-auto">
        
        <div class="text-center mb-10">
            <h1 class="text-4xl sm:text-5xl font-extrabold text-white mb-3 tracking-tight">
                Web Auditor <span class="text-indigo-500">IA</span>
            </h1>
            <p class="text-base sm:text-lg text-slate-400 font-medium">
                Detecta fallos críticos en tu web y deja de perder clientes hoy.
            </p>
        </div>

        <div class="space-y-5">
            <input type="url" id="urlInput" placeholder="Ej: www.tuempresa.com" 
                   onkeypress="if(event.key === 'Enter') enviarAnalisis()"
                   class="w-full bg-slate-900/80 border border-slate-700 p-5 sm:text-lg rounded-xl text-white outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50 transition-all placeholder-slate-500 shadow-inner">
            
            <button onclick="enviarAnalisis()" id="mainBtn" 
                    class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-lg py-5 rounded-xl shadow-lg hover:shadow-indigo-500/30 transition-all transform active:scale-95 uppercase tracking-wide">
                Analizar Web Gratis
            </button>
        </div>

        <div id="resultadoArea" class="mt-10 hidden fade-in">
            <div class="p-6 sm:p-8 bg-slate-900/80 rounded-2xl border border-slate-700 shadow-inner">
                <h3 class="text-indigo-400 font-bold mb-4 text-lg border-b border-slate-700 pb-2">Resultados de la Auditoría</h3>
                <p id="textoInforme" class="text-slate-300 text-base sm:text-lg leading-relaxed whitespace-pre-wrap"></p>
            </div>
            
            <button onclick="window.open('AQUI_IRA_TU_ENLACE_DE_STRIPE', '_blank')" 
                    class="w-full mt-6 bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-lg sm:text-xl py-5 rounded-xl shadow-[0_0_20px_rgba(5,150,105,0.3)] hover:shadow-[0_0_30px_rgba(5,150,105,0.5)] transition-all transform hover:-translate-y-1 active:translate-y-0 active:scale-95 uppercase tracking-wide">
                Solucionar con IA (19€)
            </button>
            <p class="text-center text-xs text-slate-500 mt-3 flex items-center justify-center gap-1">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"></path></svg>
                Pago 100% Seguro
            </p>
        </div>
    </div>

    <script>
        async function enviarAnalisis() {
            const urlValue = document.getElementById('urlInput').value;
            const btn = document.getElementById('mainBtn');
            const resArea = document.getElementById('resultado
