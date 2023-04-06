import yt_dlp
from yt_dlp.utils import DownloadError


ydl = yt_dlp.YoutubeDL()


def get_video_info(url):
    with ydl:
        try:
            result = ydl.extract_info(
                url,
                download=False
            )
        except DownloadError:
            return None
    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result
    return video


def get_audio_url(video_info):
    for f in video_info["formats"]:
        if f["ext"] == "m4a":
            return f["url"]


if __name__ == "__main__":
    video_info = get_video_info("https://youtu.be/e-kSGNzu0hM")
    audio_url = get_audio_url(video_info)

