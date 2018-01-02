from __future__ import print_function
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
    packages = ""
    result = request.form
    for i in result.getlist('package'):
        print(str(i), file=sys.stderr)
        packages = packages + i + ','
    packages = packages[:-1]
    print(packages, file=sys.stderr)
    return render_template("result.html", result=result)


@app.route('/build')
def build():
    subprocess.check_call('/bin/build.sh make-universe', shell=True)
    return "complete"


if __name__ == '__main__':
    app.run()
