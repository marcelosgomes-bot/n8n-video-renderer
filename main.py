from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/render', methods=['POST'])
def render():
    audio = request.files['audio']
    image = request.files['image']
    audio.save("audio.mp3")
    image.save("image.jpg")
    
    # Comando FFmpeg para unir imagem e áudio
    # Comando FFmpeg OTIMIZADO para planos de 512MB
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', 'image.jpg', 
        '-i', 'audio.mp3', 
        '-vf', 'scale=1280:-2,format=yuv420p', # Reduz para 720p (mais leve)
        '-c:v', 'libx264', 
        '-preset', 'ultrafast', # Usa menos RAM e CPU no processamento
        '-tune', 'stillimage', 
        '-c:a', 'aac', '-b:a', '128k', 
        '-shortest', 'video.mp4'
    ]
    subprocess.run(cmd, check=True)
    return send_file('video.mp4', mimetype='video/mp4')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
