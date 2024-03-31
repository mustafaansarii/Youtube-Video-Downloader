from flask import Flask, render_template, request, send_file
from pytube import YouTube
from pytube.exceptions import RegexMatchError
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    selected_option = request.form['download_option']
    try:
        yt = YouTube(video_url)
        if selected_option == 'video':
            video_and_audio_stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
            if video_and_audio_stream:
                video_path = f"{yt.title}.mp4"
                if not os.path.exists(video_path):
                    video_and_audio_stream.download(output_path='downloads', filename=f"{yt.title}.mp4")
                return send_file(os.path.join('downloads', f"{yt.title}.mp4"), as_attachment=True, conditional=True, attachment_filename=f"{yt.title}.mp4")
            else:
                return "Error: Video and audio stream not found."
        elif selected_option == 'mp3':
            highest_audio_stream = yt.streams.filter(only_audio=True).order_by('bitrate').desc().first()
            if highest_audio_stream:
                audio_path = f"downloads/{yt.title}.mp3"
                if not os.path.exists(audio_path):
                    highest_audio_stream.download(output_path='downloads', filename=f"{yt.title}.mp3")
                return send_file(os.path.join('downloads', f"{yt.title}.mp3"), as_attachment=True, conditional=True, attachment_filename=f"{yt.title}.mp3")
            else:
                return "Error: Audio stream not found."
        else:
            return "Error: Invalid format selected."
    except (RegexMatchError, Exception) as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
