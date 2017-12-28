#!/usr/bin/python

import json
import os

options = ["<!--Generated list of options-->"]
for dirpath, dirs, files in os.walk("/universe-builder/universe/repo/packages"):
    for filename in files:
        fname = os.path.join(dirpath, filename)
        if fname.endswith('package.json'):
            data = json.load(open(fname))
            package = (data["name"] + ":" + data["version"])
            options.append(str("<option value=\"" + package + "\">" + package + "</option>"))
            options.sort()

template = open('/universe-builder/web/templates/index.html', 'w')
template.write("{% extends \"base.html\" %}\n")
template.write("{% block content %}\n")

for item in options:
    template.write("%s\n" % item)

template.write("{% endblock %}\n")
template.close()
