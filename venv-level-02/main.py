import requests
# from api_secrets import API_KEY_ASSEMBLYAI
import sys
import time

API_KEY_ASSEMLYAI = "secret is deleted"
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"  # submitting endpoint

filename = sys.argv[1]
headers = {'authorization': API_KEY_ASSEMBLYAI}


def upload():
    # upload => uploading our file
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(
        upload_endpoint,
        headers=headers,
        data=read_file(filename)
    )

    # print(response.json())
    # extracting the url from the respons
    audio_url = upload_response.json()["upload_url"]

    return audio_url


# transcription => submitting our file
def transcribe(audio_url):
    transcript_request = {"audio_url": audio_url}
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


def get_transcription_results_url(audio_url):
    transcript_id = transcribe(audio_url)
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
def save_transcript(audio_url):
    data, error = get_transcription_results_url(audio_url)

    if (data):
        text_file = filename + ".txt"
        with open(text_file, "w") as f:
            f.write(data["text"])
    elif (error):
        print("Error while saving the files => \n", error)


# audio_url = upload()
# save_transcript(audio_url)
print(API_KEY_ASSEMBLYAI)
# print("Our data => \n", data)
# print("Error => \n", error)
