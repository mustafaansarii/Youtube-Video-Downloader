from flask import Flask, render_template, request
from pytube import Playlist, YouTube
import os

app = Flask(__name__)

# Function to download a single video
def download_single_video(url, download_audio=False):
    try:
        yt = YouTube(url)
        if download_audio:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.get_highest_resolution()
        file_path = stream.download()
        return file_path, yt.title
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return None, None

# Function to download videos from a playlist
def download_playlist(url, download_audio=False):
    playlist = Playlist(url)
    downloaded_files = []

    for video in playlist.video_urls:
        try:
            yt = YouTube(video)
            if download_audio:
                stream = yt.streams.filter(only_audio=True).first()
            else:
                stream = yt.streams.get_highest_resolution()
            file_path = stream.download()
            downloaded_files.append((file_path, yt.title))
        except Exception as e:
            print(f"Error downloading {yt.title}: {str(e)}")
    
    return downloaded_files

# Determine the type of URL and download accordingly
def download_by_url(url, download_audio=False):
    if 'playlist' in url:
        return download_playlist(url, download_audio)
    else:
        return [download_single_video(url, download_audio)]

@app.route('/', methods=['GET', 'POST'])
def index():
    files = None
    if request.method == 'POST':
        url = request.form['url']
        choice = request.form['choice']

        if choice == 'video':
            files = download_by_url(url)
        elif choice == 'audio':
            files = download_by_url(url, download_audio=True)
        else:
            return "Invalid choice."
    
    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
