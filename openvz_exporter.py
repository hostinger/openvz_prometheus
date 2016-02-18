#!/usr/bin/python

import subprocess
import json
from flask import Flask
app = Flask(__name__)

def vzlist():
    command = "vzlist -o hostname,ip,laverage -j"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return p.communicate()[0]

def to_prometheus(hostname, ip, value):
    return 'node_openvz_laverage{hostname="%s", ip="%s"} %s\n' % (hostname, ip, value)

@app.route("/metrics")
def metrics():
    output = []
    for vz in json.loads(vzlist()):
        output.append(to_prometheus(vz['hostname'], vz['ip'][0], vz['laverage'][0]))

    return "".join(output), 200, {'Content-type': 'text/plain'}

if __name__ == "__main__":
    app.run(host='::', port=9119)
