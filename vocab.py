#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, request, render_template


app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload_word_list', methods=['GET', 'POST'])
def upload_word_list():
    if request.method == 'GET':
        return render_template('upload_word_list.html')
    else:
        word_list_name = request.form['word_list_name']
        words = request.form['words']
        with open('data/%s.txt' % word_list_name, 'w') as f:
            f.write(words)


if __name__ == '__main__':
    app.run()