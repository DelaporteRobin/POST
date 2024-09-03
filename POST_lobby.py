import os
import sys
import time 

from functools import partial


from textual.app import App, ComposeResult
from textual.widgets import Markdown, RadioSet, RadioButton, Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.validation import Function, Number
from textual.screen import Screen 
from textual import events
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual import on

from datetime import datetime
from pyfiglet import Figlet
from time import sleep

import threading
import json
import colorama




class POST_Application(App):
	def __init__(self):
		super().__init__()



		self.settings = {}





	def compose(self) -> ComposeResult:

		yield Header(show_clock=True)




		yield Button("hello world")





	async def on_key(self, event: events.Key) -> None:
		if event.key == "p":
			self.exit()






#launch the application
if __name__ == "__main__":
	app = POST_Application()
	app.run()