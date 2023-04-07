import json
from yt_extractor import get_audio_url, get_video_info
from api import save_transcript


def save_video_sentiments(url):
    video_info = get_video_info(url)
    audio_url = get_audio_url(video_info)

    title = video_info["title"]
    title = title.strip().replace(" ", "_")
    title = "saved_data/" + title
    save_transcript(audio_url, title, sentiment_analysis=True)


if __name__ == "__main__":
    # save_video_sentiments("https://www.youtube.com/shorts/apoWKUpNvas") #use this for those data which is not in your local

    with open("saved_data/Be_a_Python_Pro_with_Enumerate_sentiments.json", "r") as file:
        data = json.load(file)

    positive = []
    negative = []
    neutral = []

    for results in data:
        text = results["text"]
        if (results["sentiment"] == "POSITIVE"):
            positive.append(text)
        if (results["sentiment"] == "NEGATIVE"):
            negative.append(text)
        if (results["sentiment"] == "NEUTRAL"):
            neutral.append(text)

    n_pos = len(positive)
    n_neg = len(negative)
    n_neu = len(neutral)

    rate = n_pos + (n_neu * 0.5) / (n_pos + n_neg + (n_neu * 0.5)) * 100
    print("number of postive sentences", n_pos)
    print("number of negative sentences", n_neg)
    print("number of neutral sentences", n_neu)
    print(f"over all postive sentiment of that video is {rate:.3f}")
