import json, urllib, datetime, time, os,sys
from operator import itemgetter
import settings

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

# JSON Sample
# [0]  { picture_url: ,
#        picture_thumb: , 
#        author: ,   
#        width: ,
#        height:,
#        date_posted:
#       }
class Imagem:
    def __init__(self):
        self.picture_url = None
        self.picture_thumb = None
        self.author = None
        self.width = 0
        self.height = 0
        self.date_posted = datetime.datetime.now()
        self.original_url = None
        
    def dictit(self):
        img = {
            'picture_url' : self.picture_url,
            'picture_thumb' : self.picture_thumb,
            'author' : self.author,
            'width' : self.width,
            'height' : self.height,
            'date_posted' : self.date_posted,
            'original_url': self.original_url
            }
        return img
    def timestamp(self, dt):
        return 1000 * time.mktime(dt.timetuple())
        
class Twitter:
    def __init__(self, tag, api_key):
        self.name   = 'Twitter'
        self.api_url = 'http://search.twitter.com/search.json?q='+tag+'&rpp=100&include_entities=true&result_type=mixed'
        self.tag = tag
        self.api_key = api_key
        
    def getPictures(self):
        print 'Getting ' + self.name
        print self.api_url
        pictures = []
        for i in range(1,6): #pega 500 results
            soap = urllib.urlopen(self.api_url + '&page=' + str(i))
            soap = json.load(soap)
            for raw_imagem in soap['results']:
                if raw_imagem.has_key('entities') and raw_imagem['entities'].has_key('media'):
                    imagem = Imagem()
                    imagem.picture_url = raw_imagem['entities']['media'][0]['media_url']
                    imagem.picture_thumb = raw_imagem['entities']['media'][0]['media_url']
                    imagem.author = raw_imagem['from_user']
                    imagem.width = raw_imagem['entities']['media'][0]['sizes']['orig']['w']
                    imagem.height = raw_imagem['entities']['media'][0]['sizes']['orig']['h']
                    imagem.date_posted = imagem.timestamp(datetime.datetime.strptime(raw_imagem['created_at'], "%a, %d %b %Y %H:%M:%S +0000"))
                    imagem.original_url = raw_imagem['entities']['media'][0]['expanded_url']
                    pictures.append(imagem.dictit())
        return pictures
                

class Instagram:
    def __init__(self, tag, api_key):
        self.name = 'Instagram'
        self.api_url = 'https://api.instagram.com/v1/media/search?lat=-23.534933&lng=-46.65326&client_id=' + api_key + '&distance=5000'
        self.tag = tag
        self.api_key = api_key
        
    def getPictures(self):
        print 'Getting ' + self.name
        print self.api_url
        pictures = []
        soap = urllib.urlopen(self.api_url)
        soap = json.load(soap)
        for raw_imagem in soap['data']:
             if raw_imagem['caption']:
                if tag in raw_imagem['caption']['text'] or tag in raw_imagem['tags']:
                    imagem = Imagem()
                    imagem.picture_url = raw_imagem['images']['standard_resolution']['url']
                    imagem.picture_thumb = raw_imagem['images']['thumbnail']['url']
                    imagem.author = raw_imagem['user']['username']
                    imagem.width = raw_imagem['images']['standard_resolution']['width']
                    imagem.height = raw_imagem['images']['standard_resolution']['height']
                    imagem.date_posted = imagem.timestamp(datetime.datetime.fromtimestamp(float(raw_imagem['created_time'])))
                    imagem.original_link = raw_imagem['link']
                    pictures.append(imagem.dictit())
        return pictures

class Flickr:
    def __init__(self, tag, api_key):
        self.name   = 'Flickr'
        self.api_url = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=' + api_key +'&text=' + tag +'&sort=&per_page=500&format=json&nojsoncallback=1&extras=owner_name,date_upload,url_t,url_l'
        self.tag = tag
        
    def getPictures(self):
        print 'Getting ' + self.name
        print self.api_url
        pictures = []
        soap = urllib.urlopen(self.api_url)
        soap = json.load(soap)
        for raw_imagem in soap['photos']['photo']:
            imagem = Imagem()
            imagem.picture_thumb = raw_imagem['url_t']
            imagem.author = raw_imagem['ownername']
            if raw_imagem.has_key('url_l'):
                imagem.picture_url = raw_imagem['url_l']
                imagem.width = raw_imagem['width_l']
                imagem.height = raw_imagem['height_l']
            imagem.date_posted = imagem.timestamp(datetime.datetime.fromtimestamp(float(raw_imagem['dateupload'])))
            imagem.original_url = 'http://www.flickr.com/photos/' + raw_imagem['owner'] + '/' + raw_imagem['id'] + '/'
            pictures.append(imagem.dictit())
        return pictures

tag = 'baixocentro'
flickr = Flickr(tag, settings.config['flickr_apikey']).getPictures()
twitter = Twitter(tag, settings.config['twitter_apikey']).getPictures()
instagram = Instagram(tag, settings.config['instagram_apikey']).getPictures()
lista_de_fotos = flickr + twitter + instagram
lista_de_fotos = sorted(lista_de_fotos, key=itemgetter('date_posted'))
a = open(tag+'.json','w')
a.write(json.dumps(lista_de_fotos))
a.close()
