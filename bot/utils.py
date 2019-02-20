import requests
from django.conf import settings


def get_file_content(file_id):
    token = settings.TELEGRAM_BOT_TOKEN

    url = 'https://api.telegram.org/bot{token}/getFile?file_id={file_id}'.format(token=token, file_id=file_id)
    res = requests.get(url)
    meta = res.json()
    if meta['ok']:
        file_path = meta['result']['file_path']
        url = 'https://api.telegram.org/file/bot{token}/{file_path}'.format(token=token, file_path=file_path)
        res = requests.get(url)
        return res.content
    else:
        raise IOError(str(meta))

