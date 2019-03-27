import sublime
import sublime_plugin
import os
import subprocess

class IncMultiCursorValuesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        word = self.view.substr(self.view.sel()[0])

        self.load_settings()
        enums = self.settings.get("enums")
        apply_enum = None
        for enum in enums:
            if word in enum:
                apply_enum = enum

        if apply_enum is None:
            try:
                num = int(word)
            except:
                num = 1
            for region in self.view.sel():
                self.view.replace(edit, region, str(num))
                num = int(num) + 1
        else:
            for region in self.view.sel():
                self.view.replace(edit, region, word)
                word = apply_enum[(apply_enum.index(word) + 1) % len(apply_enum)]

    def load_settings(self):
        defaults = {
            "enums": []
        }
        self.settings = {}
        settings = sublime.load_settings('inc_multi_cursor_values.sublime-settings')
        for setting in defaults:
            self.settings[setting] = settings.get(setting, defaults.get(setting))
