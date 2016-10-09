# Agora NHS
import requests
import shutil
from io import BytesIO
from zipfile import ZipFile

URL = 'http://fontello.com/'


def fontello():
  with open('fontello.config.json', 'rb') as fl:
    resp = requests.post(URL, files=dict(config=fl))
    session_id = resp.text

  zipfl = ZipFile(BytesIO((requests
      .get('{0}{1}/get'.format(URL, session_id))
      .content)))

  for fl in zipfl.namelist():
    if 'css' in fl or 'font/' in fl:
      loc = zipfl.extract(fl, 'frontend')

  dirname = loc.split('/')[1]
  shutil.rmtree('frontend/assets/css')
  shutil.rmtree('frontend/assets/font')
  shutil.move('frontend/%s/css' % dirname, 'frontend/assets')
  shutil.move('frontend/%s/font' % dirname, 'frontend/assets')
  shutil.rmtree('frontend/%s' % dirname)

if __name__ == '__main__':
  fontello()
