import io
import os
import requests
from StringIO import StringIO
from PIL import Image, ImageOps
from flask import Flask, render_template, make_response


CACHE_DIR = os.path.abspath('cache')


app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/thumb/<size>/<path:url>')
@app.route('/thumb/<size>/<fit>/<path:url>')
def thumb(url, size, fit=False):
    thumb = Cache(url, size, fit).get()
    response = make_response(thumb)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


class Cache(object):

    def __init__(self, url, size, fit=True):
        self.url = url
        self.size = map(int, size.split('x'))
        self.fit = fit

    def get(self):
        name = '{1}x{2}-{0}'.format(self.url.split('/')[-1], *self.size)
        path = os.path.join(CACHE_DIR, name)
        try:
            with io.open(path, 'rb') as f:
                return f.read()
        except IOError:
            with io.open(path, 'wb') as f:
                thumb = self.thumb()
                f.write(thumb)
                return thumb

    def thumb(self):
        output = StringIO()
        image = requests.get(self.url).content
        img = Image.open(StringIO(image))
        if self.fit:  # Means that we'll have to respect the size
            img = ImageOps.fit(img, self.size, Image.ANTIALIAS)
        img.thumbnail(self.size, Image.ANTIALIAS)
        img.save(output, 'JPEG', quality=85)
        output.seek(0)
        return output.getvalue()


if __name__ == '__main__':
    app.run(debug=True)
