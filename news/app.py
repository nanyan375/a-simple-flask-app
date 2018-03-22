#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template,abort
import json,os

app = Flask(__name__)

class Getfiles:
    def __init__(self):
        self.filenames = None
        self.result = []
    def get_data(self):
        filepath = os.path.join(os.path.abspath(os.path.dirname(__name__)),'..','files')
        for root,dirs,files in os.walk(filepath):
            self.filenames = files
        try:
            shiyanlou_file = self.filenames[self.filenames.index('helloshiyanlou.json')]
            world_file = self.filenames[self.filenames.index('helloworld.json')]
            with open(filepath + '/' + shiyanlou_file) as sf:
                s_dict = json.loads(sf.read())
                self.result.append(s_dict)
            with open(filepath + '/' + world_file) as wf:
                w_dict= json.loads(wf.read())
                self.result.append(w_dict)
            return self.result

        except (IndexError, ValueError):
            print('The file has some problems')
            self.error = True
            return None

getfiles = Getfiles()
data = getfiles.get_data()

@app.route('/')
def index():
    return render_template('index.html', content = data)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

@app.route('/files/<filename>')
def file(filename):
    if data:
        if filename == 'helloshiyanlou':
            return render_template('file.html', content = data[0])
        elif filename == 'helloworld':
            return render_template('file.html', content = data[1])
        else:
            abort(404)
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
