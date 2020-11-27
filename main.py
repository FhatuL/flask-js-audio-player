from flask import Flask, render_template
import os
import json
from mutagen.mp3 import MP3


from flask.helpers import send_from_directory

app = Flask(__name__)

paths = os.listdir('audio')
paths.sort()
songs = []

for item,i in zip(paths, range(len(paths))):
    a = MP3('audio/'+ item).info.length
    a = str(a/60)
    a = a.split('.')
    min_ = a[0]
    sec = int(float('0.' + a[1][0:2])*60.0)
    if sec/10 < 1:
        sec = '0'+ str(sec)

    title_string = item.split('_')
    audio_title = ''
    for title in title_string:
        
        if '.mp3' in title:
            temp = title.split('.')
            audio_title += temp[0].title()

        else:
            audio_title += title.title() + ' '

    songs.append({
        'name': audio_title,
        'path': 'audio/'+item,
        'bpm': '0',
        'price': '',
        'index': i,
        'img': 'img/artwork/' + 'default.png',
        'length': min_ + ':' + str(sec)
    })

data = []

for item in songs:
    data.append(item['path'])

@app.route('/')
def home():
    return render_template('index.html', title = 'Player', songs = songs, data = json.dumps(data))

@app.route('/audio/<path:filename>')
def serve(filename):
    return send_from_directory('audio/', filename)

if __name__ == '__main__':
    app.run(debug=True, host = '192.168.8.102', port='8000')