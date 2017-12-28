from flask import Flask, request, render_template
import subprocess

app = Flask(__name__, static_url_path='')


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/build')
def build():
    subprocess.check_call('/bin/build.sh make-universe', shell=True)
    return "complete"


if __name__ == '__main__':
    app.run()
