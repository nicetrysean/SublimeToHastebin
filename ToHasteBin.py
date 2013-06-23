try:
	import urllib2 as ulib
except ImportError:
	import urllib.request as ulib
import os
import json
import sublime, sublime_plugin

## So here's all the code for my plugin.. pretty snazy ay?
## Just be sure to mention my name when you're pasting this to your friends, and claiming it your own.

## Written by nicetrysean /-/ Sean O'Dowd.

PLUGIN_NAME = 'ToHasteBin'

class SendToHasteBinCommand( sublime_plugin.TextCommand ):

	def get_file_name(self):
		name = "Untitled.txt"
		try: name = os.path.split(self.view.file_name())[-1]
		except AttributeError: pass
		finally: return name

	def run(self, view, paste_name = None): 

		settings = sublime.load_settings(PLUGIN_NAME + '.sublime-settings')
		URL = settings.get('Hastebin-full-url')

		for region in self.view.sel():

			if not region.empty():
				content = self.view.substr(region).encode('utf8')
			else:
				content = self.view.substr(sublime.Region(0, self.view.size())).encode('utf8')
			req = ulib.Request(URL, content)
			response = ulib.urlopen(req)
			the_page = response.read()
			key = json.loads(the_page.decode("utf8"))['key']
			url = settings.get('Hastebin-short-url') + key

			filename = self.get_file_name()
			extension = os.path.splitext(filename)[1]

			sublime.set_clipboard(url + extension)
			sublime.status_message('Hastebin URL copied to clipboard: ' + url + extension)
