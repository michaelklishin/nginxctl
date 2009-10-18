#!/usr/bin/env python

import sys
import os
from os import system

class NginxCtl(object):
  """
  Nginx control operations abstraction
  """

  def __init__(self,
               pid_file_path,
               bin_file_path):
    """
    Arguments:

    pid_file_path: Nginx pid file path
    bin_file_path: Nginx bin file path
    """
    self._pid_file_path = pid_file_path
    self._bin_file_path = bin_file_path

  def run(self, command):
    """
    Runs the command
    """
    cmd2run = ""

    if command == "start":
      cmd2run = "sudo %s" % self._bin_file_path
    elif command == "reload":
      cmd2run = self.signal_command("HUP")
    elif command == "stop":
      cmd2run = self.signal_command("QUIT")
    elif command == "force-stop":
      cmd2run = self.signal_command("INT")
    elif command == "reopen-log":
      cmd2run = self.signal_command("USR1")
    elif command == "upgrade-executable":
      cmd2run = self.signal_command("USR2")
    elif command == None:
      self.quit("Commands are start, reload, stop, force-stop, reopen-log, upgrade-executable")
    else:
      self.quit("Unknown command %s" % command)

    print "Executing %s" % cmd2run
    system(cmd2run)

  def quit(self, message):
     """
     Prints a message and exits
     """
     print(message)
     sys.exit()

  def signal_command(self, signal):
     """
     Returns shell command used to send some signal
     to Nginx master process.
     """
     return "sudo kill -s %s %s" % (signal, self.find_pid())

  def find_pid(self):
    """
    Returns Nginx pid
    """
    pidfile = open(self._pid_file_path)
    pid     = pidfile.read().strip()
    pidfile.close()

    return pid


ctl = NginxCtl(pid_file_path = os.environ["NGINX_PID_FILE"],
               bin_file_path = os.environ["NGINX_BIN_FILE"])

try:
  command = sys.argv[1]
except:
  command = None

ctl.run(command)
