import json
import requests
import telegram
from django.http import HttpResponseBadRequest, JsonResponse
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import resolve_url
from django.views.decorators.csrf import csrf_exempt
from . import tasks


TASK_LIST = [
    tasks.PhotoSaveResponse,
    tasks.NaverRealtimeKeywordResponse,
    tasks.NaverBlogSearchResponse,
    tasks.TelegramLogoResponse,
]


@csrf_exempt
def webhook(request):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    obj = json.loads(request.body)
    update = telegram.update.Update.de_json(obj, bot)

    for cls in TASK_LIST:
        task = cls(update)
        if task.is_valid():
            task.proc()
            break
    else:
        tasks.NotFoundResponse(update).proc()

    return JsonResponse({})


@staff_member_required
def set_webhook(request):
    host = request.get_host()
    if 'localhost' in host or '127.0.0.1' in host:
        return HttpResponseBadRequest('에러) 공용 도메인으로 접속해주세요. ({})'.format(host))

    url = 'https://' + host + resolve_url('bot:webhook')
    token = settings.TELEGRAM_BOT_TOKEN
    endpoint = 'https://api.telegram.org/bot{token}/setWebhook?url={url}'.format(token=token, url=url)
    res = requests.get(endpoint)
    return JsonResponse(res.json())


@staff_member_required
def delete_webhook(request):
    token = settings.TELEGRAM_BOT_TOKEN
    endpoint = 'https://api.telegram.org/bot{token}/deleteWebhook'.format(token=token)
    res = requests.get(endpoint)
    return JsonResponse(res.json())

