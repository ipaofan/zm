#coding:utf8
import time
from flask import Flask
from flask import request
from opera_redis import insert_redis
from config import current_dir,rooms
from utils import write_log
import os

app = Flask(__name__)

@app.route('/send_table',methods=['GET','POST'])
def send_table():
    if request.method == 'POST':
        url = request.url
        copywriting = request.form.get('copywriting')
        table = request.form.get('table')
        room = request.form.get('room')
        write_log('url:{}'.format(url))
        write_log('copywriting:{}'.format(copywriting))
        write_log('table:{}'.format(table))
        write_log('room:{}'.format(room))
        if not table:
            return 'your request error!'
        table = "<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>{}</body></html>".format(table)
        import imgkit
        options = {'encoding': 'utf8'}
        photo_path = current_dir + 'photos/' + str(round(time.time() * 1000)) + '.jpg'
        if not os.path.exists(current_dir + 'photos/'):
            os.makedirs(current_dir + 'photos/')
        imgkit.from_string(table, photo_path,options=options)
        from PIL import Image, ImageChops
        im = Image.open(photo_path)
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            im = im.crop(bbox)
        im.save(photo_path)
        if not copywriting:
            copywriting = '您好，小时报请查收:'
        if not room:
            room = rooms[0]
        dict1 = {'copywriting':copywriting,'photo_path':photo_path,'room':room}
        insert_redis(dict1)
        return 'new photo produced!'
    if request.method == 'GET':
        return 'please send post request!'

@app.route('/send_text',methods=['GET','POST'])
def send_text():
    if request.method == 'POST':
        url = request.url
        copywriting = request.form.get('copywriting')
        text = request.form.get('text')  #参数名为username
        room = request.form.get('room')

        write_log('url:{}'.format(url))
        write_log('copywriting:{}'.format(copywriting))
        write_log('text:{}'.format(text))
        write_log('room:{}'.format(room))
        if not text:
            return 'your request error!'
        if not copywriting:
            copywriting = '您好，小时报请查收:'
        if not room:
            room = rooms[0]
        dict1 = {'copywriting':copywriting,'text':text,'room':room}
        insert_redis(dict1)
        return 'new text produced!'
    if request.method == 'GET':
        return 'please send post request!'



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)