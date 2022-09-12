import sys
from api_communications import *

filename =  sys.argv[1]

audio_url = upload(filename)
saveTrancript(audio_url, filename)