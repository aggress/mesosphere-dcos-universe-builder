from flask import Flask, request
import subprocess

app = Flask(__name__, static_url_path='')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/build')
def build():
    subprocess.check_call('/bin/build.sh make-universe', shell=True)
    return "complete"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
