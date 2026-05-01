from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import io

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    text = data.get('text', '').strip()
    lang = data.get('lang', 'fr')

    if not text:
        return jsonify({'error': 'Texte vide.'}), 400

    try:
        tts = gTTS(text=text, lang=lang)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return send_file(
            audio_buffer,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='audio.mp3'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🎙 DelphanVoice en cours...")
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
    
