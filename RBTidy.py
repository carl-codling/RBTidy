# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from gi.repository import GObject,Gtk, Peas
from gi.repository import RB
from gi.repository import Gio

import rb
import re

_SLIST = [".mp3",".wav",".flac","/",":",",","-","_","&","~","!"]

class RBTidy (GObject.Object, Peas.Activatable):	    
	__gtype_name = 'RBTidy'
	object = GObject.property(type=GObject.GObject)

	def __init__(self):
		GObject.Object.__init__(self)
		
		shell = self.object

	def do_activate(self):
		shell = self.object
		
		self.prop_type = RB.RhythmDBPropType.TITLE
		
		self.toppanel = RBTidyTopPanel(self)
		shell.add_widget (self.toppanel, RB.ShellUILocation.MAIN_BOTTOM , expand=True, fill=True)
		self.panel = RBTidyPanel(self)
		shell.add_widget (self.panel, RB.ShellUILocation.MAIN_BOTTOM , expand=True, fill=True)
		self.panel3 = RBTidyPanel3(self)
		shell.add_widget (self.panel3, RB.ShellUILocation.MAIN_BOTTOM , expand=True, fill=True)
		self.panel2 = RBTidyPanel2(self)
		shell.add_widget (self.panel2, RB.ShellUILocation.MAIN_BOTTOM , expand=True, fill=True)
				
	def do_deactivate(self):
		shell = self.object
		shell.remove_widget (self.panel, RB.ShellUILocation.MAIN_BOTTOM)
		
	def regex_replace(self,a,search,replace,test=False):
		shell = self.object
		db=shell.props.db
		src = shell.props.library_source
		v = src.get_entry_view()
		selection = v.get_selected_entries()
		for entry in selection:
			ttl = entry.get_string(self.prop_type)
			
			if replace == "::REGEX-MATCH":
				stripped_ttl = re.sub(search, self.get_regex_match, ttl).strip(' \t\n\r')
			else:
				stripped_ttl = re.sub(search, replace, ttl).strip(' \t\n\r')
			if ttl != stripped_ttl and len(stripped_ttl)>0:
				if test:
					self.toppanel.testmode_outp.set_text(stripped_ttl)
					
				else:
					db.entry_set(entry,self.prop_type,stripped_ttl)
		db.commit ()
	
	def get_regex_match(self,matchobj):
		return matchobj.group(1)
	

class RBTidyTopPanel(Gtk.HBox):
	def __init__(self,_RBT):
		Gtk.HBox.__init__(self)	
		self._RBT = _RBT
		
		
		vbox = Gtk.HBox()
		
		self.editselect = Gtk.ComboBoxText()
		self.editselect.append(None,"EDIT: TITLE")
		self.editselect.append(None,"EDIT: ARTIST")
		self.editselect.append(None,"EDIT: ALBUM")
		self.editselect.append(None,"EDIT: GENRE")
		self.editselect.set_active(0)
		self.editselect.connect("changed", self.set_prop_type)
		vbox.add(self.editselect)
		
		label = Gtk.Label("TEST OUTPUT:")
		
		self.testmode_outp = Gtk.Entry()
		vbox.add(label)
		vbox.add(self.testmode_outp)
		self.add(vbox)
		
		self.show_all()
		
	def set_prop_type(self,a):
		indx = a.get_active()
		if indx == 0:
			self._RBT.prop_type = RB.RhythmDBPropType.TITLE
		elif indx == 1:
			self._RBT.prop_type = RB.RhythmDBPropType.ARTIST
		elif indx == 2:
			self._RBT.prop_type = RB.RhythmDBPropType.ALBUM
		elif indx == 3:
			self._RBT.prop_type = RB.RhythmDBPropType.GENRE
	
	
class RBTidyPanel(Gtk.HBox):
	def __init__(self,_RBT):
		Gtk.HBox.__init__(self)	
		self._RBT = _RBT
		
		
		hbox = Gtk.HBox()
		
		self.testmode = False
		self.test_switch = Gtk.Switch()
		self.test_switch.connect("notify::active", self.set_testmode)
		
		btn = Gtk.Button("Strip track no.")
		btn.connect("clicked", self._RBT.regex_replace, '^[0-9\s?]+\s?[\-\.\:\;\\\/\[\]\s\_]+', ' ', self.set_testmode)
		hbox.add(btn)
		
		btn = Gtk.Button("Strip special")
		btn.connect("clicked", self._RBT.regex_replace, '\W+', '', self.set_testmode)
		hbox.add(btn)
		
		btn = Gtk.Button("Special to space")
		btn.connect("clicked", self._RBT.regex_replace, '\W+', ' ', self.set_testmode)
		hbox.add(btn)
		
		btn = Gtk.Button("Special to -")
		btn.connect("clicked", self._RBT.regex_replace, '\W+', '-', self.set_testmode)
		hbox.add(btn)
		
		
		btn = Gtk.Button("Capitalise")
		btn.connect("clicked", self.capitalise)
		hbox.add(btn)
		
		
		hbox.add(self.test_switch)
		
		self.add(hbox)
		
		self.show_all()
	
	def set_testmode(self,a,b):
		self.testmode = self.test_switch.get_active()	
		
	def capitalise(self,a):
		shell = self._RBT.object
		db=shell.props.db
		src = shell.props.library_source
		v = src.get_entry_view()
		selection = v.get_selected_entries()
		for entry in selection:
			ttl = entry.get_string(self._RBT.prop_type)
			attl = ttl.split(" ")
			outp = ""
			for s in attl:
				outp += s.capitalize()+" "
			if ttl != outp and len(outp)>0:
				if self.set_testmode:
					self._RBT.toppanel.testmode_outp.set_text(new_str)
					return
				else:
					db.entry_set(entry,self._RBT.prop_type,outp.strip(' \t\n\r') )
		db.commit ()
		
class RBTidyPanel2(Gtk.HBox):
	def __init__(self,_RBT):
		Gtk.HBox.__init__(self)	
		self._RBT = _RBT
		
		
		
		hbox = Gtk.HBox()
		
		label = Gtk.Label("Move from:")
		hbox.pack_start(label, False, False, 5)
		
		self.startselect = Gtk.ComboBoxText().new_with_entry()
		self.startselect.append(None,"[Start]")
		for s in _SLIST:
			self.startselect.append(None,s)
		self.startselect.set_active(0)
		hbox.pack_start(self.startselect, False, False, 5)
		
		label = Gtk.Label("to:")
		hbox.pack_start(label, False, False, 5)
		
		self.endselect = Gtk.ComboBoxText.new_with_entry()
		hbox.pack_start(self.endselect, False, False, 5)
		self.endselect.append(None,"[End]")
		for s in _SLIST:
			self.endselect.append(None,s)
		label = Gtk.Label("to:")
		hbox.pack_start(label, False, False, 5)
		
		
		self.moveto = Gtk.ComboBoxText()
		self.moveto.append(None,"title field")
		self.moveto.append(None,"artist field")
		self.moveto.append(None,"album field")
		self.moveto.append(None,"genre field")
		self.moveto.set_active(0)
		hbox.pack_start(self.moveto, False, False, 5)
		
		label = Gtk.Label("| Rem. from src?")
		hbox.pack_start(label, False, False, 5)
		
		self.remfromsrc = Gtk.Switch()
		hbox.pack_start(self.remfromsrc, False, False, 5)
		
		btn = Gtk.Button("Move")
		btn.connect("clicked", self.do_move)
		hbox.add(btn)
		
		btn = Gtk.Button("Test")
		btn.connect("clicked", self.do_move, True)
		hbox.add(btn)
		
		self.add(hbox)
		
		
		self.show_all()
	
		
	def do_move(self,a, test=False):
		shell = self._RBT.object
		db=shell.props.db
		src = shell.props.library_source
		v = src.get_entry_view()
		selection = v.get_selected_entries()
		start_str = self.startselect.get_active_text()
		end_str = self.endselect.get_active_text()
		for entry in selection:
			ttl = entry.get_string(self._RBT.prop_type)
			
			if start_str == "[Start]":
				startpos = 0
			else:
				startpos = ttl.find(start_str)+len(start_str)
			if end_str == "[End]":
				endpos = len(ttl)
			else:
				endpos = ttl.find(end_str)
				
			new_str = ttl[startpos:endpos]	
			
			if test:
				self._RBT.toppanel.testmode_outp.set_text(new_str)
				return
			
			moveto_ptype = self.get_prop_type(self.moveto.get_active())	
			db.entry_set(entry,moveto_ptype,new_str.strip(' \t\n\r'))
			
			if self.remfromsrc.get_active() and self._RBT.prop_type != moveto_ptype:
				new_ttl = ttl.replace(new_str,"")
				db.entry_set(entry,self._RBT.prop_type,new_ttl.strip(' \t\n\r'))
		db.commit()
		
	def get_prop_type(self,indx):
		if indx == 0:
			return RB.RhythmDBPropType.TITLE
		elif indx == 1:
			return RB.RhythmDBPropType.ARTIST
		elif indx == 2:
			return RB.RhythmDBPropType.ALBUM
		elif indx == 3:
			return RB.RhythmDBPropType.GENRE
			
class RBTidyPanel3(Gtk.HBox):
	def __init__(self,_RBT):
		Gtk.HBox.__init__(self)	
		self._RBT = _RBT
		
		
		
		hbox = Gtk.HBox()
		
		label = Gtk.Label("Replace:")
		hbox.pack_start(label, False, False, 5)
		
		self.search_entry = Gtk.ComboBoxText.new_with_entry()
		hbox.pack_start(self.search_entry, False, False, 5)
		self.search_entry.append(None,"REGEX::[()\[\]{}]+")
		self.search_entry.append(None,"REGEX::\[[^\[\]]+\]|\([^\)|(]+\)|{[^{}]+}")
		self.search_entry.append(None,"REGEX::\(([^\)\(]+)\)")
		
		for s in _SLIST:
			self.search_entry.append(None,s)
		
		self.search_entry.set_active(3)
		label = Gtk.Label("With:")
		hbox.pack_start(label, False, False, 5)
		
		self.replacement_entry = Gtk.ComboBoxText.new_with_entry()
		self.replacement_entry.append(None,"::REGEX-MATCH")
		hbox.pack_start(self.replacement_entry, False, False, 5)
		
		btn = Gtk.Button("Replace")
		btn.connect("clicked", self.replace)
		hbox.add(btn)
		
		btn = Gtk.Button("Test")
		btn.connect("clicked", self.replace, True)
		hbox.add(btn)
		
		self.add(hbox)
		self.show_all()
	
		
		
	def replace(self,a,test=False):
		shell = self._RBT.object
		db=shell.props.db
		src = shell.props.library_source
		v = src.get_entry_view()
		selection = v.get_selected_entries()
		for entry in selection:
			ttl = entry.get_string(self._RBT.prop_type).strip(' \t\n\r')
			searchstr = self.search_entry.get_active_text()
			replstr = self.replacement_entry.get_active_text()
			stripped_ttl = ttl.replace(searchstr, replstr)
			if searchstr[:7] == "REGEX::":
				self._RBT.regex_replace(None,searchstr.replace('REGEX::',""),replstr,test)
				return
			elif ttl != stripped_ttl and len(stripped_ttl)>0:
				if test:
					self._RBT.toppanel.testmode_outp.set_text(stripped_ttl)
				else:
					db.entry_set(entry,self._RBT.prop_type,stripped_ttl)
		db.commit ()
	
		
		
