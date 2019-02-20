import re
import requests
import telegram
from bs4 import BeautifulSoup
from django.conf import settings
from django.template.loader import render_to_string
from .utils import get_file_content


class Base:
    def __init__(self, update):
        self.update = update
        self.bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

    @property
    def chat_id(self):
        return self.update.message.chat_id

    @property
    def text(self):
        return self.update.message.text.strip()

    @property
    def photo(self):
        return self.update.message.photo

    def reply_message(self, *args, **kwargs):
        self.bot.sendMessage(chat_id=self.chat_id, *args, **kwargs)

    def reply_photo(self, *args, **kwargs):
        self.bot.sendPhoto(chat_id=self.chat_id, *args, **kwargs)

    def reply_voice(self, *args, **kwargs):
        self.bot.sendVoice(chat_id=self.chat_id, *args, **kwargs)


class PhotoSaveResponse(Base):
    def is_valid(self):
        return len(self.photo) > 0

    def proc(self):
        file_id = self.photo[-1]['file_id']
        content = get_file_content(file_id)
        # TODO: 사진 저장
        self.reply_message(text='사진 {}bytes를 읽었지만, 아직 저장은 구현되지 않았습니다.'.format(len(content)))


class NaverRealtimeKeywordResponse(Base):
    def is_valid(self):
        return bool(re.match(r'^네이버\s*실검$', self.text))

    def proc(self):
        response = '\n'.join(self.get_keyword_list())
        self.reply_message(text=response)

    def get_keyword_list(self):
        res = requests.get("http://naver.com")
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        tag_list = soup.select('.PM_CL_realtimeKeyword_rolling .ah_k')
        return [tag.text for tag in tag_list]


class NaverBlogSearchResponse(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queyr = None

    def is_valid(self):
        matched = re.match(r'네이버에?서? (.+) 검색', self.text)
        if matched:
            self.query = matched.groups(1)
        return bool(matched)

    def proc(self):
        post_list = self.naver_blog_search(self.query)
        response = render_to_string('bot/naver_blog_search.html', {'post_list': post_list})
        self.reply_message(text=response)

    def naver_blog_search(self, query):
         url = "https://search.naver.com/search.naver"
         params = {
             'where': 'post',
             'sm': 'tab_jum',
             'query': query,
         }

         res = requests.get(url, params=params)
         html = res.text
         soup = BeautifulSoup(html, 'html.parser')
         tag_list = soup.select('.sh_blog_title')

         post_list = []
         for tag in tag_list:
             post_url = tag['href']
             post_title = tag['title']
             post_list.append({
                 'title': post_title,
                 'url': post_url,
             })

         return post_list


class TelegramLogoResponse(Base):
    def is_valid(self):
        return bool(re.match(r'^텔레그램\s*로고$', self.text))

    def proc(self):
        self.reply_photo(photo='https://telegram.org/img/t_logo.png')


class NotFoundResponse(Base):
    def is_valid(self):
        return True

    def proc(self):
        self.reply_message(text='니가 무슨 말 하는 지, 모르겠어. :(')

