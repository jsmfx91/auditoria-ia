<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Web Auditor IA | Business Intelligence</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Fondo con profundidad y gradiente profesional */
        body { 
            background: radial-gradient(circle at top right, #1e1b4b, #0f172a);
            min-height: 100vh; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; 
            margin: 0;
            padding: 1.5rem;
        }
        /* Efecto de cristal esmerilado premium */
        .glass-card { 
            background: rgba(30, 41, 59, 0.7); 
            backdrop-filter: blur(20px); 
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1); 
            border-radius: 2rem; 
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
        }
        /* Animación de entrada suave */
        .fade-in {
            animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Personalización del scrollbar para el informe */
        #textoInforme::-webkit-scrollbar { width: 6px; }
        #textoInforme::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    </style>
</head>
<body class="text-slate-200">

    <div class="w-full max-w-2xl p-8 sm:p-12 glass-card mx-auto fade-in">
        
        <div class="text-center mb-12">
            <div class="flex justify-center mb-6">
                <svg width="80" height="80" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" class="drop-shadow-2xl">
                    <circle cx="50" cy="50" r="48" stroke="url(#paint0_linear)" stroke-width="4"/>
                    <path d="M35 50L4
