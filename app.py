from flask import Flask, send_from_directory, after_this_request
from switchsd import *
import uuid
import os
import zipfile
import shutil

app = Flask(__name__)

@app.route('/')
def landing_page():
    return 'Hello World!'

@app.route('/<emusys>')
def emu_sys(emusys):
    unique_id = uuid.uuid4()
    if not os.path.exists('output'):
        os.mkdir('output')
    os.mkdir(os.path.join('output', str(unique_id)))
    if emusys == 'sys' or emusys == 'sysnand':
        EMUNAND = False
    else:
        EMUNAND = True
    prepare_sd(os.path.join('output', str(unique_id)), EMUNAND)
    with zipfile.ZipFile(os.path.join('output', str(unique_id), 'sdswitch.zip'), 'w') as zf:
        sdpath = os.path.join('output', str(unique_id), 'sdswitch')
        for dirname, subdirs, files, in os.walk(sdpath):
            for filename in files:
                zf.write(os.path.join(dirname, filename), os.path.join(dirname, filename).split('/sdswitch/')[1])
    shutil.rmtree(os.path.join('output', str(unique_id), 'sdswitch'))
    @after_this_request
    def remove_file(response):
        shutil.rmtree(os.path.join('output', str(unique_id)))
        return response
    return send_from_directory(os.path.join('output', str(unique_id)), filename='sdswitch.zip')

if __name__ == '__main__':
    app.run('0.0.0.0', 80)