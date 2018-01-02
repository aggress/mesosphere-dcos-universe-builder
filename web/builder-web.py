from flask import Flask, request, render_template
import subprocess
import sys

app = Flask(__name__,
            static_url_path='',
            static_folder='static')


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def result():
    result = request.form
    return render_template("result.html", result=result)


@app.route('/build')
def build():
    subprocess.check_call('/bin/build.sh make-universe', shell=True)
    return "complete"


if __name__ == '__main__':
    app.run()
