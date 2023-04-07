import requests
from api_secrets import API_KEY_ASSEMBLYAI, API_KEY_LISTENNOTES
import time
import pprint
import json

# endpoints
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"  # submitting endpoint
listennotes_episodes_endpoint = "https://listen-api.listennotes.com/api/v2/episodes"

# headers
assemblyai_headers = {'authorization': API_KEY_ASSEMBLYAI}
listennotes_headers = {'X-ListenAPI-Key': API_KEY_LISTENNOTES}

# this function is fetching the data from listennote


def get_episode_audio_url(episode_id):
    url = listennotes_episodes_endpoint + "/" + episode_id
    res = requests.request("GET", url, headers=listennotes_headers)

    data = res.json()
    # pprint.pprint(data)

    audio_url = data["audio"]
    ep_description = data['description']
    pd_title = data['podcast']['title']
    ep_thumbnail = data["thumbnail"]
    ep_title = data["title"]

    return audio_url, pd_title, ep_description, ep_thumbnail, ep_title


# transcription => submitting our file


def transcribe(audio_url, auto_chapters):
    transcript_request = {
        "audio_url": audio_url,
        "auto_chapters": auto_chapters
    }
    transcript_response = requests.post(
        transcript_endpoint, json=transcript_request, headers=assemblyai_headers)
    # print(response.json())
    job_id = transcript_response.json()["id"]

    return job_id


# poll
'''
it is required because transcripting is a time taking proccess.
if we save the transcript immediate after submiting the request, the job will be undone
polling is done for checking whether the job is done or not 
'''


def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    polling_response = requests.get(
        polling_endpoint, headers=assemblyai_headers)
    # print(polling_response.json())
    return polling_response.json()


def get_transcription_results_url(audio_url, auto_chapters):
    transcript_id = transcribe(audio_url, auto_chapters)
    print("job-id is => ", transcript_id)

    while (True):
        data = poll(transcript_id)
        if (data["status"] == "completed"):
            return data, None
        elif (data["status"] == "error"):
            return data, data["error"]

        print("wait atleast 60sec...🙂")
        time.sleep(60)


# save the transcript
def save_transcript(episode_id, auto_chapters=False):
    audio_url, podcast_title, ep_description, ep_thumbnail, ep_title = get_episode_audio_url(
        episode_id)
    data, error = get_transcription_results_url(audio_url, auto_chapters)

    if (data):
        text_file = episode_id + ".txt"
        with open(text_file, "w") as f:
            f.write(data["text"])

        # doing it with .json so that we can parse it easily
        chapters_filename = episode_id + "_chapters.json"
        with open(chapters_filename, "w") as f:
            chapters = data["chapters"]

            episode_data = {"chapters": chapters}
            episode_data["episode_thumbnail"] = ep_thumbnail
            episode_data["episode_title"] = ep_title
            episode_data["podcast_title"] = podcast_title
            episode_data["description"] = ep_description

            json.dump(episode_data, f)
            print("Transcript is saved!!!")

        return True

    elif (error):
        print("Error while saving the files => \n", error)
        return False
