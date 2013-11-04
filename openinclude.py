import sublime, sublime_plugin
import os.path
import re

class OpenInclude(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			syntax = self.view.syntax_name(region.begin())
			if re.match(".*string.quoted.double", syntax): self.select(self.view, region, '"') # Match & Select Doubles
			if re.match(".*string.quoted.single", syntax): self.select(self.view, region, "'") # Match & Select Singles
			
			for region in self.view.sel():
				if region.empty():
					line = self.view.line(region)
					filepath = self.view.substr(line).strip()
				else:
					filepath = self.view.substr(region)

			if os.path.isfile(filepath):
				self.view.window().open_file(filepath)
				sublime.status_message("Opening file " + filepath)

		def select(self, view, region, char):
			begin = region.begin() - 1
			end = region.begin()
			while view.substr(begin) != char or view.substr(begin - 1) == '\\': begin -= 1
			while view.substr(end) != char or view.substr(end - 1) == '\\': end += 1
			view.sel().subtract(region)
			view.sel().add(sublime.Region(begin + 1, end))