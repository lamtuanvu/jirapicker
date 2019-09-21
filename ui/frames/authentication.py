#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.9pre on Wed Sep 18 23:31:09 2019
#

import wx
import re
import os

from core.third_party_interaction import MySQLHandler
from core.authenticator_engine import verify_password
from core.authenticator_engine import hash_password
from ui.widgets import FlexTextCtrl
from icons.iconsets import *
from ui.styles import *

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class LoginFrame(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: LoginFrame.__init__
        kwds["style"] = kwds.get(
            "style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.FRAME_NO_TASKBAR
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle("Login")
        self.SetIcon(jira_32px.GetIcon())

        self.mysql = MySQLHandler()
        self.username = None
        self.email = None
        self.authorize_by_pc = False
        self.logged_user = None

        vbox_main = wx.BoxSizer(wx.VERTICAL)

        blbl_main = wx.StaticBitmap(self, wx.ID_ANY,
                                    icons8_name_64.GetBitmap())

        vbox_main.Add(blbl_main, 0, wx.ALL | wx.EXPAND, 5)

        hbox_user = wx.BoxSizer(wx.HORIZONTAL)
        vbox_main.Add(hbox_user, 0, wx.ALL | wx.EXPAND, 5)

        blbl_user = wx.StaticBitmap(self, wx.ID_ANY,
                                    icons8_account_32.GetBitmap())
        hbox_user.Add(blbl_user, 0, wx.ALL | wx.EXPAND, 0)

        # self.txt_user = FlexTextCtrl(self, hint='Enter Your UserName')
        self.txt_user = wx.TextCtrl(self, wx.NewIdRef(), "")
        self.txt_user.SetMinSize((-1, -1))
        hbox_user.Add(self.txt_user, 1, wx.ALIGN_CENTER, 0)

        hbox_password = wx.BoxSizer(wx.HORIZONTAL)
        vbox_main.Add(hbox_password, 0, wx.ALL | wx.EXPAND, 5)

        blbl_password = wx.StaticBitmap(self, wx.ID_ANY, icons8_lock_32.GetBitmap())
        hbox_password.Add(blbl_password, 0, 0, 0)

        # self.txt_password = FlexTextCtrl(self, hint='Enter Your Password', password=True)
        self.txt_password = wx.TextCtrl(self, wx.ID_ANY, "",
                                        style=wx.TE_PASSWORD |
                                        wx.TE_PROCESS_ENTER)
        self.txt_password.SetMinSize((-1, -1))
        hbox_password.Add(self.txt_password, 1, wx.ALIGN_CENTER, 0)
        self.txt_password.Enable(False)

        self.btn_login = wx.Button(
            self, wx.ID_ANY, "LOGIN", style=wx.BORDER_NONE)
        self.btn_login.SetMinSize((-1, -1))
        vbox_main.Add(self.btn_login, 0, wx.ALL | wx.EXPAND, 5)
        self.btn_login.Enable(False)

        self.btn_login_by_pc = wx.Button(
            self, wx.ID_ANY, "LOGIN BY YOUR PC", style=wx.BORDER_NONE)
        vbox_main.Add(self.btn_login_by_pc, 0, wx.ALL | wx.EXPAND, 5)

        hbox_remember = wx.BoxSizer(wx.HORIZONTAL)
        vbox_main.Add(hbox_remember, 0, wx.ALL | wx.EXPAND, 5)

        self.ckbox_remember_me = wx.CheckBox(self, wx.ID_ANY, "Remember me")
        self.ckbox_remember_me.SetMinSize((-1, -1))
        hbox_remember.Add(self.ckbox_remember_me, 1, 0, 0)

        self.btn_forgot_pass = wx.Button(
            self, wx.ID_ANY, "Forgot your password?", style=wx.BORDER_NONE)
        self.btn_forgot_pass.SetMinSize((-1, -1))
        hbox_remember.Add(self.btn_forgot_pass, 1, 0, 0)

        self.btn_register = wx.Button(self, wx.ID_ANY, "REGISTER")
        self.btn_register.SetMinSize((-1, -1))
        vbox_main.Add(self.btn_register, 0, wx.ALL | wx.EXPAND, 5)

        self.lbl_status = wx.StaticText(self, wx.NewIdRef(), "")
        vbox_main.Add(self.lbl_status, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(vbox_main)
        vbox_main.Fit(self)

        # blbl_main.SetFocus()
        self.Layout()
        self.Center(wx.BOTH)

        # end wxGlade

        self.Bind(wx.EVT_BUTTON, self.on_button_pressed)
        self.Bind(wx.EVT_TEXT, self.on_text_change)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_enter_pressed)
        self.check_valid_pc()

    def on_text_change(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.txt_user.GetId():
            if self.txt_user.GetValue() != "":
                self.txt_password.Enable()
            else:
                self.txt_password.Enable(False)
        elif eid == self.txt_password.GetId():
            if self.txt_password.GetValue() != "":
                self.btn_login.Enable()
            else:
                self.btn_login.Enable(False)

    def on_enter_pressed(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.txt_password.GetId():
            self.login_action()

    def on_button_pressed(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.btn_register.GetId():
            self.register_action()

        elif eid == self.btn_login.GetId():
            self.login_action()

        elif eid == self.btn_login_by_pc.GetId():
            self.login_by_pc_action()

    def login_action(self):
        user = self.txt_user.GetValue()
        self.logged_user = user
        password = self.txt_password.GetValue()
        result = self.mysql.get_data_by_id(
            'user', ['password'], 'username', user)
        if result:
            database_password = result[0][0]
            if verify_password(database_password, password):
                self.EndModal(wx.ID_OK)
            else:
                wx.MessageBox("Invalid UserName or Password",
                              "Login Error", wx.ICON_ERROR)
        else:
            wx.MessageBox("Invalid UserName",
                          "Login Error", wx.ICON_ERROR)

    def register_action(self):
        dlg = RegisterFrame(self)
        if dlg.ShowModal() == wx.ID_OK:
            del self.mysql
            self.mysql = MySQLHandler()

    def login_by_pc_action(self):
        self.authorize_by_pc = True
        user = self.txt_user.GetValue()
        self.logged_user = user
        result = self.mysql.get_data_by_id('user', ['username'], 'username', user)
        print ("Result username: ", result)
        if result:
            if user == result[0][0]:
                self.EndModal(wx.ID_OK)
        else:
            if wx.MessageBox("Your username can't be found in database. Would you like to create one?",
                            "Creation Notification", wx.ICON_QUESTION | wx.YES_NO) == wx.YES:
                self.register_action()

    def check_valid_pc(self):
        self.username = os.environ.get("USERNAME")
        domain = os.environ.get("USERDNSDOMAIN").lower()
        self.email = self.username + '@' + domain
        if domain != "tma.com.vn":
            # wx.MessageBox("Your PC is not authorized. Please use your TMA's PC", "Authorized Error", style=wx.ICON_ERROR)
            self.lbl_status.SetForegroundColour(COLOR_ERROR)
            self.lbl_status.SetLabel("TMA's PC is required for PC authorization")
            self.btn_login_by_pc.Enable(False)
            self.Layout()
        else:
            self.lbl_status.SetForegroundColour(COLOR_SUCCESS)
            self.lbl_status.SetLabel("Username: {}. Email: {}".format(self.username, self.email))
            self.txt_user.SetValue(self.username)
            self.Layout()

class RegisterFrame(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)

        self.SetTitle("Register Your Account")
        # self.SetSize(self.GetParent().GetSize())
        parent = self.GetParent()

        self.mysql = MySQLHandler()

        vbox_main = wx.BoxSizer(wx.VERTICAL)

        blbl_main = wx.StaticBitmap(self, wx.ID_ANY,
                                    icons8_subscription_64.GetBitmap())

        vbox_main.Add(blbl_main, 0, wx.ALL | wx.EXPAND, 5)

        hbox_name = wx.BoxSizer(wx.HORIZONTAL)

        vbox_first_name = wx.BoxSizer(wx.VERTICAL)
        vbox_last_name = wx.BoxSizer(wx.VERTICAL)

        lbl_first_name = wx.StaticText(self, wx.ID_ANY, label="First Name")
        vbox_first_name.Add(lbl_first_name, 0, wx.EXPAND, 0)

        self.txt_first_name = wx.TextCtrl(self, wx.NewIdRef())
        vbox_first_name.Add(self.txt_first_name, 0, wx.EXPAND, 0)

        hbox_name.Add(vbox_first_name, 1, wx.EXPAND | wx.RIGHT, 5)

        lbl_last_name = wx.StaticText(self, wx.ID_ANY, label="Last Name")
        vbox_last_name.Add(lbl_last_name, 0, wx.EXPAND, 0)

        self.txt_last_name = wx.TextCtrl(self, wx.NewIdRef())
        vbox_last_name.Add(self.txt_last_name, 0, wx.EXPAND, 0)

        hbox_name.Add(vbox_last_name, 1, wx.EXPAND | wx.LEFT, 5)

        vbox_main.Add(hbox_name, 0, wx.EXPAND | wx.ALL, 5)

        vbox_username = wx.BoxSizer(wx.VERTICAL)

        lbl_username = wx.StaticText(self, wx.ID_ANY, label="User Name")
        vbox_username.Add(lbl_username, 0, wx.EXPAND, 0)

        self.txt_username = wx.TextCtrl(self, wx.NewIdRef())
        vbox_username.Add(self.txt_username, 0, wx.EXPAND, 0)


        vbox_main.Add(vbox_username, 0, wx.EXPAND | wx.ALL, 5)

        vbox_email = wx.BoxSizer(wx.VERTICAL)

        lbl_email = wx.StaticText(self, wx.ID_ANY, label="Your Email")
        vbox_email.Add(lbl_email, 0, wx.EXPAND, 0)

        self.txt_email = wx.TextCtrl(self, wx.NewIdRef())
        vbox_email.Add(self.txt_email, 0, wx.EXPAND, 0)
        self.txt_email.Enable(False)

        vbox_main.Add(vbox_email, 0, wx.EXPAND | wx.ALL, 5)

        hbox_passwords = wx.BoxSizer(wx.HORIZONTAL)

        vbox_password = wx.BoxSizer(wx.VERTICAL)

        vbox_confirm_pw = wx.BoxSizer(wx.VERTICAL)

        lbl_password = wx.StaticText(self, wx.ID_ANY, label="Password")
        vbox_password.Add(lbl_password, 0, wx.EXPAND, 0)

        self.txt_password = wx.TextCtrl(
            self, wx.NewIdRef(), style=wx.TE_PASSWORD)
        vbox_password.Add(self.txt_password, 0, wx.EXPAND, 0)
        self.txt_password.Enable(False)

        hbox_passwords.Add(vbox_password, 1, wx.EXPAND | wx.RIGHT, 5)

        lbl_confirm_pw = wx.StaticText(
            self, wx.ID_ANY, label="Confirm Password")
        vbox_confirm_pw.Add(lbl_confirm_pw, 0, wx.EXPAND, 0)

        self.txt_confirm_pw = wx.TextCtrl(self, wx.NewIdRef(),
                                          style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        vbox_confirm_pw.Add(self.txt_confirm_pw, 0, wx.EXPAND, 0)
        self.txt_confirm_pw.Enable(False)

        hbox_passwords.Add(vbox_confirm_pw, 1, wx.EXPAND | wx.LEFT, 5)

        vbox_main.Add(hbox_passwords, 0, wx.EXPAND | wx.ALL, 5)

        self.btn_register = wx.Button(self, wx.NewIdRef(), label="Register")
        self.btn_register.Enable(False)

        vbox_main.Add(self.btn_register, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(vbox_main)

        self.Layout()
        self.Fit()
        self.Center(wx.BOTH)

        self.Bind(wx.EVT_BUTTON, self.on_button_pressed)
        self.Bind(wx.EVT_TEXT, self.on_text_change)
        self.txt_confirm_pw.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter)

        if parent.authorize_by_pc:
            self.txt_username.SetValue(parent.username)
            self.txt_email.SetValue(parent.email)
        else:
            pass

    def on_button_pressed(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.btn_register.GetId():
            self.register_action()

    def on_text_change(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.txt_confirm_pw.GetId():
            if self.txt_confirm_pw.GetValue() == self.txt_password.GetValue():
                self.btn_register.Enable()
            else:
                self.btn_register.Enable(False)
        elif eid == self.txt_username.GetId():
            if self.txt_username.GetValue() != "":
                self.txt_email.Enable()
            else:
                self.txt_email.Enable(False)
                self.btn_register.Enable(False)
        elif eid == self.txt_email.GetId():
            result = self.txt_email.GetValue()
            email_pattern = "[^@]+@tma.com.vn"
            if re.match(email_pattern, result):
                self.txt_password.Enable()
            else:
                self.txt_password.Enable(False)
        elif eid == self.txt_password.GetId():
            if self.txt_password.GetValue() != "":
                self.txt_confirm_pw.Enable()
            else:
                self.txt_confirm_pw.Enable(False)

    def on_text_enter(self, evt):
        if self.txt_confirm_pw.GetValue() == self.txt_password.GetValue():
            self.register_action()
        else:
            wx.MessageBox("Please enter your correct password", "Confirm Password Error", style=wx.ICON_ERROR | wx.OK)

    def register_action(self):
        first_name = self.txt_first_name.GetValue()
        last_name = self.txt_last_name.GetValue()
        email = self.txt_last_name.GetValue()
        username = self.txt_username.GetValue()
        password = hash_password(self.txt_password.GetValue())
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        values = [first_name, last_name, email, username, password]
        result = self.mysql.write_to_database('user',
                                              fields=fields,
                                              values=values)
        if result == "Duplicated":
            wx.MessageBox("User Name Is Existed", "Register Error",
                          wx.ICON_ERROR)
        self.EndModal(wx.ID_OK)
        self.mysql.cnx.close()
        self.Destroy()


def test():
    app = wx.App()
    test_object = LoginFrame(None, wx.ID_ANY, "")
    test_object.ShowModal()
    app.SetTopWindow(test_object)
    app.MainLoop()


if __name__ == "__main__":
    test()
