from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import zipfile
import os

app = Flask(__name__)
CORS(app)

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    files = request.files.getlist('images')
    if not files:
        return {"error": "No files provided."}, 400

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file in files:
            img = Image.open(file.stream).convert("RGBA")
            output = remove(img)
            output_io = io.BytesIO()
            output.save(output_io, format="PNG")
            output_io.seek(0)
            zip_file.writestr(file.filename.rsplit('.', 1)[0] + '_no_bg.png', output_io.read())

    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name='output.zip', mimetype='application/zip')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
