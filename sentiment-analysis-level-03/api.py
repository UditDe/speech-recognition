import requests
from api_secrets import API_KEY_ASSEMBLYAI
import time
import json


upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"  # submitting endpoint


headers_auth = {'authorization': API_KEY_ASSEMBLYAI}
headers = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

# upload => uploading our file
def upload(filename):

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(
        upload_endpoint,
        headers=headers_auth,
        data=read_file(filename)
    )

    # print(response.json())
    # extracting the url from the respons

    return upload_response.json()["upload_url"]


# transcription => submitting our file
def transcribe(audio_url, sentiment_analysis):
    transcript_request = {
        "audio_url": audio_url,
        "sentiment_analysis": sentiment_analysis
    }
    transcript_response = requests.post(
        transcript_endpoint, json=transcript_request, headers=headers)
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
    polling_response = requests.get(polling_endpoint, headers=headers)
    # print(polling_response.json())
    return polling_response.json()


def get_transcription_results_url(url, sentiment_analysis):
    transcript_id = transcribe(url, sentiment_analysis)
    print("job-id is => ", transcript_id)

    while (True):
        data = poll(transcript_id)
        if (data["status"] == "completed"):
            return data, None
        elif (data["status"] == "error"):
            return data, data["error"]

        print("wait atleast 30sec...🙂")
        time.sleep(30)


# save the transcript
def save_transcript(url, filename, sentiment_analysis=False):
    data, error = get_transcription_results_url(url, sentiment_analysis)

    if (data):
        text_file = filename + ".txt"
        with open(text_file, "w") as f:
            f.write(data["text"])
            print("Transcript got!!")

        if(sentiment_analysis):
            text_file = filename + "_sentiments.json"
            with open(text_file, "w") as f:
                sentiments = data["sentiment_analysis_results"]
                json.dump(sentiments, f, indent=4)
            print("sentiment analysis is done!!")
        return True
    elif (error):
        print("Error while saving the files => \n", error)
        return False
