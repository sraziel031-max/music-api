from fastapi import FastAPI
from ytmusicapi import YTMusic
import yt_dlp

app = FastAPI()

ytmusic = YTMusic()


@app.get("/")
def home():
    return {
        "message": "Music API Running"
    }


@app.get("/search")
def search(q: str):

    results = ytmusic.search(
        q,
        filter="songs"
    )

    clean_results = []

    for song in results[:10]:

        clean_results.append({
            "title": song.get("title"),
            "videoId": song.get("videoId"),
            "artist": song["artists"][0]["name"]
            if song.get("artists")
            else "Unknown",
            "duration": song.get("duration")
        })

    return clean_results


@app.get("/stream/{video_id}")
def stream(video_id: str):

    url = f"https://youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestaudio"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

        return {
            "stream_url": info["url"]
        }