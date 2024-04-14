from pytube import Playlist, YouTube

def download_single_video(url, option):
    try:
        yt = YouTube(url)
        if option == 'V':
            stream = yt.streams.get_highest_resolution()
        elif option == 'A':
            stream = yt.streams.filter(only_audio=True).first()
        print(f"Downloading: {yt.title}")
        stream.download()
        print(f"{yt.title} downloaded successfully!\n")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def download_playlist(url, option):
    playlist = Playlist(url)

    for video in playlist.video_urls:
        try:
            yt = YouTube(video)
            if option == 'V':
                stream = yt.streams.get_highest_resolution()
            elif option == 'A':
                stream = yt.streams.filter(only_audio=True).first()
            print(f"Downloading: {yt.title}")
            stream.download()
            print(f"{yt.title} downloaded successfully!\n")
        except Exception as e:
            print(f"Error downloading {yt.title}: {str(e)}")

def download_by_url(url, option):
    if 'playlist' in url:
        download_playlist(url, option)
    else:
        download_single_video(url, option)

if __name__ == "__main__":
    url = input("Enter the YouTube video or playlist URL: ")
    option = input("Enter 'V' to download video or 'A' to download audio: ").upper()
    download_by_url(url, option)
