from tokenRequired import *
import dropbox


@app.route('/excel/info', methods=['POST'])
@token_required
def info(token):

    f = request.files.get('file', None)
    if f is None:
        return jsonify({'message': 'missing -F file arg'})

    if '.' not in f.filename:
        return jsonify({'message': 'filename has no extension'})

    if 'xlsx' in f.filename.rsplit('.', 1)[1].lower():
        xls = pd.ExcelFile(f)
        sheets = xls.sheet_names
        return jsonify(sorted(sheets, key = lambda i: i,reverse=False))
    return jsonify({'message': 'extension not allowed'})


@app.route('/image/convert', methods=['POST'])
@token_required
def convert(token):

    f = request.files.get('file', None)
    if f is None:
        return jsonify({'message': 'missing -F file arg'})

    if '.' not in f.filename:
        return jsonify({'message': 'filename has no extension'})

    if is_allowed(f.filename):
        ext = define_extension(f.filename)
        return sending_as_header(f, '/tmp/image.' + ext, ext)

    return jsonify({'message': 'extension not allowed'})


@app.route('/image/convert/fromdropbox', methods=['POST'])
@token_required
def convertFromDropBox(token):

    try:
        dbx = dropbox.Dropbox(token['dropbox_token'])
    except:
         return jsonify({'message': 'Dropbox token invalid'})

    url = request.form.get('url', None)
    if url is None or url == '':
        return jsonify({'message': 'missing -F url arg'})

    if is_allowed(url):
        ext = define_extension(url)

        try:
            metadata,file=dbx.files_download(url)
        except:
             return jsonify({'message': 'URL 404 server side'})

        f = BytesIO(file.content)
        return sending_as_header(f, '/tmp/image.' + ext, ext)
    return jsonify({'message': 'extension not allowed'})


def sending_as_header(f, url, ext):
    output = BytesIO()
    img = Image.open(f).convert('RGB')
    img.save(output, format=ext.upper())
    response = make_response(output.getvalue())
    response.headers.set('Content-Type', 'image/' + ext)
    response.headers.set('Content-Disposition', 'attachment', filename=url)
    return response


def is_allowed(name):
    ext = name.rsplit('.', 1)[1].lower()
    if ext == 'png' or ext == 'jpg' or ext == 'jpeg':
        return True
    return False


def define_extension(name):
    ext = name.rsplit('.', 1)[1].lower()
    return 'png' if ext == 'jpg' else 'jpeg'
