#!/usr/bin/env python

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

status = {
    'power': False
    'volume': 0
}

def irsend(code, directive = "SEND_ONCE", remote = "nad"):
    print "Execute: irsend " + directive + " " + remote + " " + code + " "
    if code == 'KEY_POWER':
        status['power'] = not status['power']
    elif code == 'KEY_VOLUMEDOWN':
        status['volume'] -= status['volume']
        if status['volume'] < 0:
            status['volume'] = 0
    elif code == 'KEY_VOLUMEUP':
        status['volume'] += status['volume']
        if status['volume'] > 100:
            status['volume'] = 100
    return 0

def power_on():
    print "Turning power on - if not already on"
    if not status['power']:
        return irsend('KEY_POWER')
    else:
        return 0

def power_off():
    print "Turning power off - if not already off"
    if status['power']:
        return irsend('KEY_POWER')
    else:
        return 0

@app.route('/')
def index():
    return jsonify({'rc': 0, 'msg': 'Hello, World!'})

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({'status': status})

@app.route('/api/power_on', methods=['POST'])
def api_power_on():
    returnCode = power_on()
    return jsonify({'rc': returnCode})

@app.route('/api/power_off', methods=['POST'])
def api_power_off():
    returnCode = power_off()
    return jsonify({'rc': returnCode})

@app.route('/api/send', methods=['POST'])
def send_control():
    if not request.json or not 'code' in request.json:
        abort(400)
    directive = request.json.get('directive', 'SEND_ONCE')
    remote = request.json.get('remote', 'nad')
    code = request.json['code']
    if code == 'KEY_POWER_ON':
        returnCode = power_on()
    elif code == 'KEY_POWER_OFF':
        returnCode = power_off()
    else:
        returnCode = irsend(code, directive, remote)

    return jsonify({'rc': returnCode})

if __name__ == '__main__':
    app.run(debug=True)
