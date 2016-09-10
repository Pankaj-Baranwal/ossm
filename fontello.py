# Agora NHS
import requests
from io import BytesIO
from zipfile import ZipFile

URL = 'http://fontello.com/'
FLLOC = 'frontend/assets/fontello-embedded.css'

def fontello():
  with open('fontello.config.json', 'rb') as fl:
    resp = requests.post(URL, files=dict(config=fl))
    session_id = resp.text

  zipfl = ZipFile(BytesIO((requests
      .get('{0}{1}/get'.format(URL, session_id))
      .content)))

  for cssflname in zipfl.namelist():
    if 'fontello-embedded.css' in cssflname:
      with open(FLLOC, 'wb') as fl:
        fl.write(zipfl.open(cssflname).read())
      return True


if __name__ == '__main__':
  fontello()
