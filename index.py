from flask import Flask, render_template, request, jsonify, send_file, make_response
from PIL import Image
from io import BytesIO
import dropbox, pandas as pd

from Flask_API_JWT import app, LOCAL_HOST
from .decorator import token_required


@app.route('/excel/info', methods=['POST'])
@token_required
def info(token):

    f = request.files.get('file', None)
    if f is None:
        return jsonify({'404' : 'file'})

    if '.' not in f.filename:
        return jsonify({'400': 'filename has no extension'})

    if 'xlsx' in f.filename.rsplit('.', 1)[1].lower():
        xls = pd.ExcelFile(f)
        sheets = xls.sheet_names
        return jsonify(sorted(sheets, key = lambda i: i,reverse=False))
    return jsonify({'400': 'extension not allowed'})


@app.route('/image/convert', methods=['POST'])
@token_required
def convert(token):

    f = request.files.get('file', None)
    if f is None:
        return jsonify({'404' : 'file'})

    if is_allowed(f.filename):
        ext = define_extension(f.filename)
        return sending_as_header(f, '/tmp/image.' + ext, ext)

    return jsonify({'400': 'extension not allowed'})


@app.route('/image/convert/fromdropbox', methods=['POST'])
@token_required
def convertFromDropBox(token):

    try:
        dbx = dropbox.Dropbox(token['dropbox_token'])
    except:
         return jsonify({'401': 'Dropbox token invalid'})

    url = request.form.get('url', None)
    if url is None or url == '':
        return jsonify({404 : 'url'})

    if is_allowed(url):
        ext = define_extension(url)

        try:
            metadata,file=dbx.files_download(url)
        except:
             return jsonify({404: 'URL server side'})

        f = BytesIO(file.content)
        return sending_as_header(f, '/tmp/image.' + ext, ext)
    return jsonify({'400': 'extension not allowed'})



def sending_as_header(f, url, ext):
    output = BytesIO()
    try:
        img = Image.open(f).convert('RGB')
        img.save(output, format=ext.upper())
    except:
        return jsonify({'400': 'is it a image?'})

    response = make_response(output.getvalue())
    response.headers.set('Content-Type', 'image/' + ext)
    response.headers.set('Content-Disposition', 'attachment', filename=url)
    return response


def is_allowed(name):
    if '.' in name:
        ext = name.rsplit('.', 1)[1].lower()
        if ext == 'png' or ext == 'jpg' or ext == 'jpeg':
            return True
    return False


def define_extension(name):
    ext = name.rsplit('.', 1)[1].lower()
    return 'png' if ext == 'jpg' else 'jpeg'
