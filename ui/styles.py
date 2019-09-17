#!/usr/bin/env python
"""
=====================================
Style for whole project
=====================================
Usage: %prog
:Author: Vu Lam, lamtuanvuqs@gmail.com
:Date: 2019-08-16
Sources: N/A
"""

####Color####

COLOR_NORMAL_COMMAND = (38, 166, 91)
COLOR_SUCCESS = (31, 58, 147) # Jacksons Purple
COLOR_ERROR = (240, 52, 52) #Pomegranate
COLOR_RESULT = (115, 101, 152) # Scampi
COLOR_BREAK_LINE = (30, 130, 76)
COLOR_DESCRIPTION = (46, 49, 49)
COLOR_HIDE = (189, 195, 199)

####Message Box Style###
caption = None
style = None
MESSAGE_ERROR = {caption: "Error", style: "OK | CENTRE"}
MESSAGE_CONFIRM = None

class SetStyle():
    def __init__(self, wxObject):
        self.wxObject = wxObject
        self.printStyle = PrintStyle()

    def normal(self):
        self.wxObject.SetForegroundColour(self.printStyle.description())
    def hint(self):
        pass
    def error(self):
        pass