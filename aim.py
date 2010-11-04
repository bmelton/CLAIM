#!/usr/bin/env python

from __future__ import print_function

from twisted.words import *
from twisted.words.protocols import oscar
from twisted.internet import reactor, protocol
import login, getpass, re, random, bz2, threading, readline, sys

HOST = 'login.oscar.aol.com'
PORT = 5190
icqMode = 0
DEBUG = True
PROMPT = "> "

class aimBot(oscar.BOSConnection):
	print("")
	print("Welcome to CLAIM, the Command Line AIM client.")
	print("It sucks, right now.  Might always.  Hooray!")
	print("==================================================")
	
	global USER
	seqnum = 0
	
	#capabilities = [oscar.CAP_CHAT]

	def initDone(self):
		if DEBUG:
			print("DEBUG: entered initDone method")
			print("DEBUG: Requesting Self Info")
		self.requestSelfInfo().addCallback(self.gotSelfInfo)
		if DEBUG: 
			print("DEBUG: Requesting SSI")
		self.requestSSI().addCallback(self.gotBuddyList)
		#self.activateSSI()

	def offlineBuddy(self, user):
		print("%s is offline" % user)

	def updateBuddy(self, user):
		print("%s" % user)

	def gotBuddyList(self, l):
		if DEBUG:
			print("DEBUG: entered gotBuddyList method")
			print("DEBUG: Activating SSI")
		self.activateSSI()
		if DEBUG:
			print("DEBUG: Setting profile to available")
		self.setProfile("Your mother loves me.")
		if DEBUG:
			print("DEBUG: Resetting idle time")
		self.setIdleTime(0)
		if DEBUG:
			print("DEBUG: ClientReady")
		self.clientReady()
	
	def gotConfig(self, mode, buddylist, permit, deny):
		if DEBUG: 
			print("DEBUG: entered gotConfig method")
		global USER
		self.add_buddy([USER])
		if DEBUG: 
			print("DEBUG: Logging in")
		self.signon()
		if DEBUG:
			print("DEBUG: Logged in")

	def gotSelfInfo(self, user):
		if DEBUG:
			print("DEBUG: Entered gotSelfInfo method")
		self.name = user.name

	def receiveMessage(self, user, message, reply):
		print("%s: %s" % (user.name, message[0][0]))
		# BLM: This prompt is blocking
		#response = raw_input("reply: ")
		#self.sendMessage(user.name, response, wantAck = 1, autoResponse = (self.awayMessage != None)).addCallback(self.respondToMessage)

	def respondToMessage(self, (username, message)):
		if DEBUG:
			print("DEBUG: Entered respondToMessage method")
		print("%s: %s" % (username, message))
		pass

	def hearWarning(self, warnlvl, screenname):
		#print(screenname, " warned us")
		print("ZOMG %s warned us!" % screenname)

	def hearError(self, errcode, *args):
		print("Error: ", errcode)

	def cli(self):
	        while True:
			cli = str(raw_input(PROMPT))
			if cli == "exit":
				self.disconnect()
				print("Exiting")
				sys.exit()
			if cli == "send":
				to = str(raw_input("TO: "))
				msg = str(raw_input("MSG: "))
				self.sendMessage(to, msg, wantAck=0, autoResponse=(self.awayMessage != None)).addCallback(self.respondToMessage)
				#print("%s: %s" % (to, msg))


class aimAuth(oscar.OscarAuthenticator):
	BOSClass = aimBot

account = login.get_credentials()
USER = bz2.decompress(account["user"])
PASS = bz2.decompress(account["pass"])
print("Attempting to log in as %s" % USER)

if __name__ == '__main__':
	auth = aimAuth
	aimbot = aimBot(auth, oscar.BOSConnection)
	threading.Thread(target=aimbot.cli).start()
	
	chat = protocol.ClientCreator(reactor, aimAuth, USER, PASS, 0)
	chat.connectTCP(HOST, PORT)
        threading.Timer(1, reactor.run()).start()

	#reactor.run()
