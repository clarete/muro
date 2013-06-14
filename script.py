# -*- coding: utf-8; -*-
import json
import urllib
import time
from operator import itemgetter
from datetime import datetime
from settings import config


class Media(object):
    """Format of a media object

    Each object has the following keys:

     * content
     * thumb
     * author
     * width
     * height
     * date_posted
     * media_type
     * media_provider
    """
    def __init__(self):
        self.content = None
        self.thumb = None
        self.author = None
        self.width = 0
        self.height = 0
        self.date_posted = datetime.now()
        self.original_url = None
        self.media_type = None
        self.media_provider = None

    def dictit(self):
        return {
            'content': self.content,
            'thumb': self.thumb,
            'author': self.author,
            'width': self.width,
            'height': self.height,
            'date_posted': self.date_posted,
            'original_url': self.original_url,
            'media_type': self.media_type,
            'media_provider': self.media_provider
        }

    def timestamp(self, dt):
        return 1000 * time.mktime(dt.timetuple())


class Twitter(object):
    def __init__(self, tag, api_key):
        self.name = 'Twitter'
        self.tag = tag
        self.api_key = api_key
        self.api_url = 'http://search.twitter.com/search.json'

    def getPictures(self):
        print 'Getting ' + self.name
        print self.api_url

        pictures = []

        params = {
            'q': self.tag,
            'rpp': 100,
            'include_entities': True,
            'result_type': 'recent',
        }

        for i in range(1, 6):  # pega 500 results
            params.update({'page': i})

            url = '{0}?{1}'.format(self.api_url, urllib.urlencode(params))
            data = json.load(urllib.urlopen(url))

            # Sanity checks again
            if 'results' not in data:
                continue

            for item in data['results']:
                # Sanity check to proceed retrieving things
                if not ('entities' in item and
                        'media' in item['entities']):
                    continue

                # Building the Media item that will be added to the return list
                imagem = Media()
                imagem.media_type = 'image'
                imagem.media_provider = self.name.lower()
                imagem.content = \
                    item['entities']['media'][0]['media_url']
                imagem.thumb = item['entities']['media'][0]['media_url']
                imagem.author = item['from_user']
                imagem.width = \
                    item['entities']['media'][0]['sizes']['orig']['w']
                imagem.height = \
                    item['entities']['media'][0]['sizes']['orig']['h']

                date_posted = datetime.strptime(
                    item['created_at'], "%a, %d %b %Y %H:%M:%S +0000")
                imagem.date_posted = \
                    imagem.timestamp(date_posted)

                imagem.original_url = \
                    item['entities']['media'][0]['expanded_url']
                pictures.append(imagem.dictit())
        return pictures


class Instagram(object):
    def __init__(self, tag, api_key):
        self.name = 'Instagram'
        self.tag = tag
        self.api_key = api_key
        self.api_url = (
            'https://api.instagram.com/'
            'v1/tags/{0}/media/recent?client_id={1}'.format(tag, api_key))

    def getPictures(self):
        print 'Getting ' + self.name
        print self.api_url

        pictures = []

        data = json.load(urllib.urlopen(self.api_url))

        for item in data['data']:
            imagem = Media()
            imagem.media_type = 'image'
            imagem.media_provider = self.name.lower()
            imagem.content = item['images']['standard_resolution']['url']
            imagem.thumb = item['images']['thumbnail']['url']
            imagem.author = item['user']['username']
            imagem.width = item['images']['standard_resolution']['width']
            imagem.height = item['images']['standard_resolution']['height']

            date_posted = datetime.fromtimestamp(float(item['created_time']))
            imagem.date_posted = imagem.timestamp(date_posted)
            imagem.original_url = item['link']
            pictures.append(imagem.dictit())
        return pictures


class Flickr(object):
    def __init__(self, tag, api_key):
        self.name = 'Flickr'
        self.tag = tag
        self.api_url = 'http://api.flickr.com/services/rest/'
        self.api_key = api_key

    def getPictures(self):
        print 'Getting ' + self.name
        print self.api_url

        pictures = []

        params = {
            'method': 'flickr.photos.search',
            'api_key': self.api_key,
            'text': self.tag,
            'per_page': 500,
            'format': 'json',
            'nojsoncallback': 1,
            'extras': 'owner_name,date_upload,url_t,url_l',
        }

        url = '{0}?{1}'.format(self.api_url, urllib.urlencode(params))
        data = json.load(urllib.urlopen(url))

        for item in data['photos']['photo']:
            # Sanity checks
            if 'url_l' in item:
                imagem = Media()
                imagem.media_type = 'image'
                imagem.media_provider = self.name.lower()
                imagem.thumb = item['url_t']
                imagem.author = item['ownername']
                imagem.content = item['url_l']
                imagem.width = item['width_l']
                imagem.height = item['height_l']
                imagem.date_posted = imagem.timestamp(
                    datetime.fromtimestamp(float(item['dateupload'])))
                imagem.original_url = \
                    'http://www.flickr.com/photos/{0}/{1}'.format(
                        item['owner'], item['id'])
                pictures.append(imagem.dictit())
        return pictures


class Picasa(object):
    def __init__(self, tag):
        self.name = 'Picasa'
        self.api_url = 'https://picasaweb.google.com/data/feed/base/all'
        self.tag = tag

    def getPictures(self):
        print 'Getting ' + self.name
        print self.api_url

        pictures = []

        params = {
            'alt': 'json',
            'kind': 'photo',
            'access': 'public',
            'filter': 1,
            'imgmax': 1600,
            'hl': 'pt_BR',
            'q': self.tag,
        }

        url = '{0}?{1}'.format(self.api_url, urllib.urlencode(params))
        data = json.load(urllib.urlopen(url))

        for item in data['feed']['entry']:
            imagem = Media()
            imagem.media_type = 'image'
            imagem.media_provider = self.name.lower()
            imagem.author = [x['name']['$t'] for x in item['author']]
            imagem.content = item['content']['src']
            imagem.date_posted = imagem.timestamp(
                datetime.strptime(
                    item['published']['$t'], "%Y-%m-%dT%H:%M:%S.000Z"))
            imagem.original_url = [x['href'] for x in item['link']][2]
            pictures.append(imagem.dictit())
        return pictures


class Youtube(object):
    def __init__(self, tag):
        self.name = 'Youtube'
        self.tag = tag
        self.api_url = (
            'http://gdata.youtube.com'
            '/feeds/api/videos/-/{0}?alt=json'.format(tag))

    def getVideos(self):
        print 'Getting ' + self.name
        print self.api_url

        videos = []

        data = json.load(urllib.urlopen(self.api_url))

        for item in data['feed']['entry']:
            video = Media()
            video.media_type = 'video'
            video.media_provider = self.name.lower()
            video.content = item['media$group']['media$content'][0]['url']
            video.thumb = item['media$group']['media$thumbnail'][0]['url']
            video.author = item['author'][0]['name']['$t']
            video.width = item['media$group']['media$thumbnail'][0]['width']
            video.height = item['media$group']['media$thumbnail'][0]['height']
            video.date_posted = video.timestamp(
                datetime.strptime(
                    item['updated']['$t'], "%Y-%m-%dT%H:%M:%S.000Z"))
            video.original_url = item['link'][0]['href']
            videos.append(video.dictit())
        return videos


def rockndroll():
    tag = 'baixocentro'

    flickr = Flickr(tag, config['flickr_apikey']).getPictures()
    twitter = Twitter(tag, config['twitter_apikey']).getPictures()
    instagram = Instagram(tag, config['instagram_apikey']).getPictures()
    picasa = Picasa(tag).getPictures()
    youtube = Youtube(tag).getVideos()

    data = flickr + twitter + instagram + picasa + youtube
    data = sorted(data, key=itemgetter('date_posted'), reverse=True)

    with open('{0}.json'.format(tag), 'w') as f:
        f.write(json.dumps(data))


if __name__ == '__main__':
    rockndroll()
