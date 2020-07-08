#!/usr/bin/env python

'''
#autorun from /etc/profile adding:
python3 /home/pi/web_server/app.py
#this will run this command in each login (reboot, ssh connection...)

#autorun using supervisor:
sudo apt-get install supervisor

#create file /etc/supervisor/conf.d/relay_web_control.conf
[program:relay_web_control]
command = /usr/bin/python3 /home/pi/Projects/relay_web_control/app.py
autostart = true
autorestart = true
stdout_logfile = /var/log/Projects/relay_web_control_out.log
stderr_logfile = /var/log/Projects/relay_web_control_err.log
'''

from flask import Flask, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)

'''
-, +, S
6, 4, 12

NO: light bulb + (off by default. if connected to NC is on by default)

COM: AC power +

light bulb - to AC power -
'''

RelayPin = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RelayPin, GPIO.OUT)
GPIO.output(RelayPin, False)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    if request.form.get('on') == '':
      GPIO.output(RelayPin, True)
    elif request.form.get('off') == '':
      GPIO.output(RelayPin, False)
  return render_template('index.html', status = GPIO.input(RelayPin))

try:
  if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
except KeyboardInterrupt:
  GPIO.cleanup()