#!/usr/bin/python

import subprocess, time

subprocess.call("sync")
subprocess.call(["shutdown", "-h", "now"])

