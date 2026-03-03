#!/usr/bin/env python

import os


def switch_focus():
	os.popen("hyprctl dispatch movefocus r")
	
if __name__ == "__main__":
	switch_focus()