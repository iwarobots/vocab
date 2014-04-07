#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random

from flask import Flask, request, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
db = SQLAlchemy(app)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
    ndef = db.Column(db.Integer)
    list_name = db.Column(db.String)
    nmistakes = db.Column(db.Integer)

    def __init__(self, word, ndef, list_name, nmistakes=0):
        self.word = word
        self.ndef = ndef
        self.list_name = list_name
        self.nmistakes = nmistakes


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String)

    def __init__(self, list_name):
        self.list_name = list_name


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload_list', methods=['GET', 'POST'])
def upload_list():
    if request.method == 'GET':
        return render_template('upload_list.html')
    else:
        list_name = request.form['list_name']
        l = List(list_name)
        db.session.add(l)
        words = request.form['words']
        word_list = words.split('\r\n')

        for raw_word in word_list:
            w, ndef = raw_word.split('\t')
            word = Word(w, ndef, list_name)
            db.session.add(word)
        db.session.commit()
        return 'Successful upload.'


@app.route('/select_list')
def select_list():
    lists = List.query.all()
    return render_template('select_list.html', lists=lists)


@app.route('/show_list')
@app.route('/show_list/<list_name>')
def show_list(list_name=None):
    words = Word.query.filter_by(list_name=list_name).all()
    random.shuffle(words)
    return render_template('show_list.html', words=words)


@app.route('/record', methods=['POST'])
def record():
    ids = [int(id) for id in request.form.keys()]
    for id in ids:
        w = Word.query.get(id)
        new_nmistakes = w.nmistakes + 1
        w.nmistakes = new_nmistakes
    db.session.commit()
    return 'Recorded.'


if __name__ == '__main__':
    app.run()
    # db.create_all()