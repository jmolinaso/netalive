#!/usr/bin/env python

import socket
import subprocess
import sched, time
import logging.config

logging.config.fileConfig('netalive.conf')

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

def restart_raspbian_wlan():
    restart_command = ['sudo','systemctl','restart','ifup@wlan0.service']
    output_commnad = subprocess.call(restart_command)
    if output_commnad == 0:
        logger.info("Successfully restarted")
    else:
        logger.info("Failed to restart command returned {}".format(output_commnad))

def has_internet():
    REMOTE_SERVER="www.google.com"
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        socket.create_connection((host,80),2)
        return True
    except:
        return False

def main():
    if has_internet():
        logger.info("Nothing to worry")
    else:
        logger.info("No internet detected, restarting connection")
        restart_raspbian_wlan()

def loop_scheduler(rescheduler, interval, task, arguments=()):
    rescheduler.enter(interval, 1, task, arguments)
    rescheduler.run()
    loop_scheduler(rescheduler,interval, task)

if __name__ == '__main__':
    logger.info("Start internet watcher")
    time_scheduler = sched.scheduler(time.time, time.sleep)
    loop_scheduler(time_scheduler, 10, main)
    logger.info("Finished execution")
