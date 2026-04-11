📊 Dash_Visualizacion es un proyecto académico de visualización interactiva de datos desarrollado con Plotly Dash y Python, enfocado en mostrar análisis estadísticos y resultados sobre el Banco de la República de Colombia, con el objetivo de hacer más accesible la información económica y financiera mediante dashboards reproducibles.

🚀 Para ejecutarlo localmente debes clonar el repositorio con git clone https://github.com/jacob0900/Dash_Visualizacion.git y entrar en la carpeta, crear un entorno virtual (python -m venv venv y activarlo con venv\Scripts\activate en Windows o source venv/bin/activate en Mac/Linux), instalar las dependencias con pip install -r requirements.txt y correr la aplicación con python app.py para abrirla en tu navegador en 👉 http://127.0.0.1:8050.

✏️ Para modificar el código abre el proyecto en tu editor favorito (por ejemplo VS Code con code .), los archivos principales son app.py (layout y callbacks del dashboard), requirements.txt (librerías necesarias) y la carpeta assets/ (CSS e imágenes). Para ver los cambios reflejados automáticamente asegúrate de que app.run(debug=True) esté activo.

⚠️ Problemas comunes: si python no se reconoce como comando, reinstala Python y marca Add to PATH; si aparece No module named dash, activa el entorno virtual y reinstala dependencias; si el puerto 8050 está ocupado, cambia el puerto en app.py con app.run(debug=True, port=8051) y accede a http://127.0.0.1:8051.

💾 Para guardar 
