import urllib2
import os
import json


import sublime, sublime_plugin

URL = 'http://hastebin.com/documents'

class SendToHasteBinCommand( sublime_plugin.TextCommand ):

	def get_file_name(self):
		name = "Untitled.txt"
		try: name = os.path.split(self.view.file_name())[-1]
		except AttributeError: pass
		finally: return name

	def run(self, view, paste_name = None): 

		for region in self.view.sel():

			text = self.view.substr(region).encode('utf8')
			if not text:
				sublime.status_message('Error sending to HasteBin: Nothing selected')
			else:
				req = urllib2.Request(URL, text)
				response = urllib2.urlopen(req)
				the_page = response.read()
				key = json.loads(the_page)['key']
				url = "http://hastebin.com/%s" % key

				filename = self.get_file_name()
				extension = os.path.splitext(filename)[1]

				sublime.set_clipboard(url + extension)
				sublime.status_message('Hastebin URL copied to clipboard: ' + url + extension)
