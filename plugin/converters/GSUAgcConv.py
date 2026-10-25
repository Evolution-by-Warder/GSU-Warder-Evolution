#######################################################################
#
#    Converter for Enigma2
#    Coded by shamann (c)2013
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#######################################################################

from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.HardwareInfo import HardwareInfo

class GSUAgcConv(Converter, object):
	AGCTEXT = 1
	AGCNUM = 2
	
	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "AgcText":
			self.type = self.AGCTEXT
		elif type == "AgcNum":
			self.type = self.AGCNUM

	@cached
	def getText(self):
		percent = None
		if self.type == self.AGCTEXT:
			percent = self.source.agc
			if percent is not None:
				percent = self.calculateAGC(percent)
		if percent is None:
			return "N/A"
		return "%d %%" % (percent * 100 / 65536)

	text = property(getText)

	@cached
	def getValue(self):	
		if self.type == self.AGCNUM:
			count = self.source.agc			
			if count is not None: 
				count = self.calculateAGC(count)
			if count is None:
				return 0						
			return int(count * 100 // 65536)

	range = 100
	value = property(getValue)


	def calculateAGC(self, value):
		if HardwareInfo().get_device_name() == 'dm800se': 
			return min((value*10), 65536)
		elif HardwareInfo().get_device_name() == 'dm7020hd': 
			return abs(65536 - value)
		return value
