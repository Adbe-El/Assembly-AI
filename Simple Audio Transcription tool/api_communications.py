import time
import requests
from api_key import ASSEMBLYAI_API_KEY

# upload

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
headers = {'authorization': ASSEMBLYAI_API_KEY}

def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post( upload_endpoint,
                            headers=headers,
                            data=read_file(filename))

    audio_url = upload_response.json()['upload_url']
    return audio_url

# transcribe
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

def transcribe(audio_url):
    

    transcript_request = { "audio_url": audio_url }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    job_id = transcript_response.json()['id']

    return job_id
    
# poll
def poll(trascript_id):
    polling_endpoint = transcript_endpoint + '/' + trascript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

def getTranscriptionResultUrl(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']


        print('waiting 30sec...')
        time.sleep(30)



# save transcript

def saveTrancript(audio_url, filename):
    data, error = getTranscriptionResultUrl(audio_url)

    if data:
        text_filename = filename + '.txt'
        with open(text_filename, 'w') as f:
            f.write(data['text'])

        print('Transcription saved!')
    elif error:
        print('Error!', error)