#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flaskapp'
db = SQLAlchemy(app)
client = MongoClient('127.0.0.1', 27017)
mdb = client.flaskapp1

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    create_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('files', lazy='dynamic'))
    content = db.Column(db.Text)


    def __init__(self, title, create_time, category, content):
        self.title = title
        self.create_time = create_time
        self.content = content
        self.category = category

    def add_tag(self, tag_name):
        items = mdb.files.find_one({'id': self.id})
        if items:
            tags = items['tag']
            if tag_name not in tags:
                tags.append(tag_name)
                mdb.files.update_one({'id':self.id},{'$set':{'tag':tags}})
        else:
            tags = [tag_name]
            mdb.files.insert({'id':self.id, 'tag':tags})
        return tags

    def remove_tag(self, tag_name):
        items = mdb.files.find_one({'id':self.id})
        if items:
            tags = items['tag']
            try:
                tags.remove(tag_name)
            except ValueError:
                print('%s is not in db'%tag_name)
                return tags
            mdb.files.update_one({'id':self.id},{'$set':{'tag':tags}})
        return []

    @property
    def tags(self):
        items = mdb.files.find_one({'id':self.id})
        if items:
            tags = items['tag']
            print(tags)
            return tags
        else:
            return []

    def __repr__(self):
        return '<File %s>'%self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %s>'%self.name

def insert_datas():
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
    file1.add_tag('tech')
    print(file1.tags)
    file1.add_tag('java')
    print(file1.tags)
    file1.add_tag('linux')
    print(file1.tags)
    file2.add_tag('tech')
    print(file2.tags)
    file2.add_tag('python')
    print(file2.tags)

@app.route('/')
def index():
    #file1 = File.query.filter_by(title='Hello Java').first()
    #file2 = File.query.filter_by(title='Hello Python').first()
    return render_template('index.html', files = File.query.all())

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

@app.route('/files/<int:file_id>')
def file(file_id):
    file1 = File.query.filter_by(title='Hello Java').first()
    file2 = File.query.filter_by(title='Hello Python').first()
    if file_id == int(file1.id):
        return render_template('file.html', content = file1)
    elif file_id == int(file2.id):
        return render_template('file.html', content = file2)
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
