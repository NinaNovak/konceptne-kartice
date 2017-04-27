#datoteke se shranjujejo na C:\tmp\...

from bottle import *
import os

@route('/upload')
def upload():
    return template('upload')

@route('/upload', method='POST')
def do_upload():
    print('cwd je ' + os.getcwd())
    category   = request.forms.get('category')
    print('')
    upload     = request.files.get('upload')
    print('')
    name, ext = os.path.splitext(upload.filename)
    print('')
    save_path = "/tmp/{category}".format(category=category)
    print('')
    if not os.path.exists(save_path):
        print('')
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    print('cela pot je ' + os.path.abspath(file_path))
    upload.save(file_path)
    print('')
    return "File successfully saved to '{0}'.".format(save_path)

run(debug=True)
