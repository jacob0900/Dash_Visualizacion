Revisar la ultima version llamada Correccion 

📊 Dash_Visualizacion
Dashboard interactivo de visualización de datos desarrollado con Plotly Dash y Python.

🚀 Cómo ejecutarlo localmente
Sigue estos pasos para descargar el proyecto y correrlo en tu propia computadora.

✅ Requisitos previos
Asegúrate de tener instalado lo siguiente antes de comenzar:
HerramientaVersión mínimaDescargaPython3.8 o superiorpython.orgGitCualquier versión recientegit-scm.com

💡 Windows: Durante la instalación de Python, marca la opción "Add Python to PATH".

Verifica que estén correctamente instalados abriendo una terminal y ejecutando:
bashpython --version
git --version

📥 Instalación
1. Clona el repositorio
bashgit clone https://github.com/jacob0900/Dash_Visualizacion.git
cd Dash_Visualizacion
2. Crea un entorno virtual
bash# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate

Sabrás que el entorno está activo cuando veas (venv) al inicio de la línea en tu terminal.

3. Instala las dependencias
bashpip install -r requirements.txt
4. Ejecuta la aplicación
bashpython app.py
Abre tu navegador y ve a 👉 http://127.0.0.1:8050

✏️ Cómo modificar el código
Abre el proyecto en tu editor favorito. Si usas VS Code:
bashcode .
Los archivos principales son:
ArchivoDescripciónapp.pyArchivo principal: layout y callbacks del dashboardrequirements.txtLibrerías necesariasassets/CSS, imágenes y archivos estáticos
Para ver los cambios reflejados automáticamente en el navegador, asegúrate de que la última línea de app.py tenga el modo debug activo:
pythonapp.run(debug=True)

⚠️ Problemas comunes
python no se reconoce como comando
→ Reinstala Python y marca la opción "Add Python to PATH", o usa python3 en su lugar.
No module named dash
→ El entorno virtual no está activo. Actívalo con el comando del paso 2 y repite pip install -r requirements.txt.
El puerto 8050 ya está en uso
→ Cambia el puerto en app.py: app.run(debug=True, port=8051) y accede a http://127.0.0.1:8051.

💾 Guardar tus cambios
bashgit add .
git commit -m "Descripción de los cambios"
git push
