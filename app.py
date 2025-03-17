from flask import Flask, render_template, jsonify, send_from_directory
import cloudinary
import cloudinary.api
import cloudinary.uploader
import os
import json
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),  # Load from .env
    api_key=os.getenv("CLOUDINARY_API_KEY"),  # Load from .env
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),  # Load from .env
    secure=True
)

# Ruta para la página principal donde se mostrarán los videos
@app.route('/')
def index():
    try:
         # Obtener una lista de videos desde Cloudinary
        response = cloudinary.api.resources(
            resource_type="image",  # Solo imagenes
            type="upload",  # Necesitamos especificar el tipo "upload" para recursos subidos
            prefix="certificados/",
            max_results=100  # Carpeta donde se encuentran los archivos
        )
        
        num_recursos = len(response['resources'])  # Número total de recursos

        # Construir las URLs sin número de versión
        certificados_data = [
            {
                "nombre": resource['public_id'].split('/')[-1],  # Nombre del archivo
                "url": f"http://res.cloudinary.com/{cloudinary.config().cloud_name}/image/upload/{resource['public_id']}.{resource['format']}",  # URL sin versión
            }
            for resource in response['resources']
        ]
        
        
          # Número total de elementos
        #return render_template('index.html', certificados=certificados_data)
        return jsonify({"length": num_recursos,"data":certificados_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))