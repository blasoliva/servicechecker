#!/usr/bin/python
""" Service checker script """

import subprocess
import time
from email.mime.text import MIMEText

processes = [
    ('/etc/init.d/', 'apache2'),
    ('/etc/init.d/', 'nginx'),
]

log_path = '/var/log/servicechecker.log'

email = None

def exec_cmd(cmd):
    """ Execute command and return responses
    
    returncode -- code attribute
    output -- command output
    error -- error ouput
    """
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    rc = p.returncode
    return {'returncode': rc, 'output': out, 'error': err}

def write_log(msg):
    """ Write message into log file """
    logfile = open(log_path, 'a')
    logfile.write('[' + time.strftime('%c')  + '] ' + msg)
    logfile.close()

def send_email(to, msg):
    """ Send alert message to email """
    msg = MIMEText(msg + '\nThe service has been restarted.')
    msg["To"] = email
    msg["Subject"] = "Service checker alert"
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
    p.communicate(msg.as_string())
    write_log('Sending alert email\n')
    
# Iterate over processes
for p in processes:
    # Execute status command
    response = exec_cmd([p[0] + p[1], 'status'])
    # If process is not running (Usually when the service is running returncode is 0)
    if response['returncode'] > 0:
        # Write ouput into log file
        write_log(response['output'])
        # If email is set send alert email
        if email:
            send_email(email, response['output'])
        # Restart the service
        response = exec_cmd([p[0] + p[1], 'restart'])
        # Write output into log file (again...)
        write_log(response['output'])


