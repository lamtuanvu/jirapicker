#!/usr/bin/python3
"""[summary]
=====================================
wx.UltimateListCtrl customization
=====================================
:Author: Vu Lam, lamtuanvuqs@gmail.com
:Date: 2019-09-16
Sources: N/A
"""
import wx
import re

from wx.lib.agw import ultimatelistctrl as ULC

from ui.styles import *


class MyUltimateListCtrl(ULC.UltimateListCtrl):
    def __init__(self, parent, id=wx.NewIdRef(), pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0,
                 agwStyle=ULC.ULC_REPORT |
                 ULC.ULC_VRULES |
                 ULC.ULC_HRULES |
                 ULC.ULC_SINGLE_SEL |
                 ULC.ULC_HAS_VARIABLE_ROW_HEIGHT,
                 validator=wx.DefaultValidator, name='UltimateListCtrl',
                 **kwargs):
        ULC.UltimateListCtrl.__init__(self, parent, id=id, pos=pos,
                                      size=size, style=style,
                                      agwStyle=agwStyle,
                                      validator=validator,
                                      name=name)
        self.configure_list_control()
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_item_right_click)
        self.Bind(wx.EVT_CHAR, self.on_key_pressed)
        self.Bind(wx.EVT_BUTTON, self.on_button_pressed)

    def configure_list_control(self):
        pass

    def on_button_pressed(sefl, evt):
        pass

    def on_item_right_click(self, evt):
        pass

    def on_key_pressed(self, evt):
        pass


class MyTextCtrl(wx.TextCtrl):
    def __init__(self, parent, hint=None, password=False, *args, **kwargs):
        self.is_password = password
        kwargs['style'] = kwargs.get('style', 0) | wx.TE_PROCESS_ENTER
        if self.is_password:
            kwargs['style'] = kwargs.get('style', 0) | wx.TE_PASSWORD
        super(MyTextCtrl, self).__init__(
            parent, wx.NewIdRef(), *args, **kwargs)
        if hint:
            self.SetForegroundColour(COLOR_HIDE)
            self.SetValue(hint)

        # self.Bind(wx.EVT_TEXT, self.on_text_change)
        # self.Bind(wx.EVT_SET_FOCUS, self.on_text_focus)
        # self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter)

    # def on_text_change(self, evt):
    #     pass

    # def on_text_focus(self, evt):
    #     pass

    # def on_text_enter(self, evt):
    #     pass


class FlexTextCtrl(wx.Panel):
    def __init__(self, *args, **kwargs):
        hint = None
        password = None
        for k, v in kwargs.items():
            if k == 'hint':
                print(k)
                hint = kwargs['hint']
            elif k == 'password':
                print(k)
                password = kwargs['password']
        if hint:
            kwargs.pop('hint')
        if password is not None:
            kwargs.pop('password')
        super(FlexTextCtrl, self).__init__(*args, **kwargs)

        self.is_out = True
        self.hint = hint
        self.input = None

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        if password:
            self.txt_out = MyTextCtrl(self, hint=hint, password=False)
            self.txt_int = MyTextCtrl(self, hint=None, password=password)
        else:
            self.txt_out = MyTextCtrl(self, hint=hint, password=False)
            self.txt_int = MyTextCtrl(self, hint=None, password=False)
        self.vbox.Add(self.txt_int, 1, wx.EXPAND, 0)
        # self.txt_int.Disable()
        self.txt_int.Hide()
        self.vbox.Add(self.txt_out, 1, wx.EXPAND, 0)
        self.vbox.Layout()
        self.SetSizer(self.vbox)
        self.Layout()
        # self.txt_out.SetFocus()

        self.txt_int.Bind(wx.EVT_TEXT, self.on_text_change)
        self.txt_out.Bind(wx.EVT_TEXT, self.on_text_change)
        # self.txt_out.SetFocus()
        # self.txt_out.SetFocusFromKbd()

    def on_text_change(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.txt_int.GetId():
            if self.txt_int.GetValue() == "":
                # self.is_out = True
                self.toggle()
        else:
            self.input = self.txt_out.GetValue()
            # self.is_out = False
            self.toggle()

    def toggle(self):
        """
        Toggle change text ctrl
        :return: None
        """
        if self.is_out:
            self.txt_out.Hide()
            self.txt_int.Show()
            # self.vbox.Layout()
            self.Layout()
            if self.input:
                pattern = self.hint + "(.*)"
                self.input = ''.join(re.findall(pattern, self.input))
                self.txt_int.AppendText(self.input)
            self.is_out = False
            self.txt_int.SetFocus()

        else:
            self.txt_int.Hide()
            self.txt_out.SetValue(self.hint)
            self.txt_out.Show()
            self.is_out = True
            # self.vbox.Layout()
            self.Layout()
            # self.txt_out.SetFocus()
            
    def txt_activation(self):
        if self.is_out:
            self.toggle()
