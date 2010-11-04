#!/usr/bin/env python

import os, sys, getpass, bz2, pickle

settings_file = "./settings.dat"

def ask_credentials():
	global settings_file
	USER = raw_input("username: ")
	USER = bz2.compress(USER)
	PASS = getpass.getpass("password: ")
	PASS = bz2.compress(PASS)

	user_dict = {"user": USER, "pass": PASS}
	f = open(settings_file, "w")
	pickle.dump(user_dict, f)
	f.close()
	
def get_credentials():
	global settings_file
	f = open(settings_file, "r")

	input = pickle.load(f)
	f.close()
	
	return input	

if __name__ == "__main__":
	ask_credentials()
