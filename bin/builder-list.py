#!/usr/bin/python

import json
import os
import fileinput

options = ["<!--Generated list of options-->"]
for dirpath, dirs, files in os.walk("/universe-builder/universe/repo/packages"):
    for filename in files:
        fname = os.path.join(dirpath, filename)
        if fname.endswith('package.json'):
            data = json.load(open(fname))
            package = (data["name"] + ":" + data["version"])
            options.append(str("<option value=\"" + package + "\">" + package + "</option>"))
            options.sort()


for line in fileinput.input('/universe-builder/web/static/index.html', inplace=1):
    print line,
    if line.startswith('<!--Insert here-->'):
        for line in options: print line
