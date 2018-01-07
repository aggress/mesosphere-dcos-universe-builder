from __future__ import print_function
from flask import Flask, request, render_template
import subprocess
import sys
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='static')


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def result():
    packages = ""
    version = ""
    result = request.form
    for i in result.getlist('package'):
        packages = packages + i + ','
    packages = packages[:-1]
    for i in result.getlist('version'):
        version = version + i
    print(packages, file=sys.stderr)
    print(version, file=sys.stderr)
    os.environ['PACKAGES'] = packages
    os.environ['DCOS_VER'] = version
    print(os.environ["PACKAGES"], file=sys.stderr)
    print(os.environ["DCOS_VER"], file=sys.stderr)
    subprocess.check_call('/universe-builder/bin/run.sh make-universe', shell=True)
    return render_template("result.html", result=result)


@app.route('/shutdown', methods=['POST'])
def build():
    subprocess.check_call('killall flask', shell=True)
    return "complete"


if __name__ == '__main__':
    app.run()
