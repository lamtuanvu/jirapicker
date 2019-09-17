#!/usr/bin/env python
import wx
import sys

from ui.widgets import MyUltimateListCtrl
from ui.widgets import FlexTextCtrl


class JiraPickerFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: JiraPickerFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((894, 649))
        self.SetTitle("Jira Picker")
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUBAR))

        vbox_main = wx.BoxSizer(wx.VERTICAL)

        main_w, main_h = self.GetSize()

        self.pn_top = wx.Panel(self, wx.NewIdRef())
        vbox_main.Add(self.pn_top, 0, wx.EXPAND, 0)

        hbox_top = wx.BoxSizer(wx.HORIZONTAL)

        static_text_1 = wx.StaticText(
            self.pn_top, wx.NewIdRef(), "Details of JQL statment")
        hbox_top.Add(static_text_1, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)

        # self.txt_jql_statment = wx.TextCtrl(self.pn_top, wx.NewIdRef(), "")
        self.flex_txt_jql_statement = FlexTextCtrl(self, hint="Enter your statement", password=False)
        hbox_top.Add(self.flex_txt_jql_statement, 1, wx.ALIGN_CENTER, 5)

        self.btn_search = wx.Button(self.pn_top, wx.NewIdRef(), "Search")
        hbox_top.Add(self.btn_search, 0, wx.ALIGN_CENTER, 5)

        self.btn_save_change = wx.Button(self.pn_top, wx.NewIdRef(),
                                         "Save Change")
        hbox_top.Add(self.btn_save_change, 0, wx.ALIGN_CENTER, 5)

        hbox_middle = wx.BoxSizer(wx.HORIZONTAL)
        vbox_main.Add(hbox_middle, 1, wx.EXPAND, 0)

        self.pn_left = wx.Panel(self, wx.NewIdRef())
        self.pn_left.SetMinSize((200, -1))
        hbox_middle.Add(self.pn_left, 0, wx.EXPAND, 0)

        # self.pn_left.SetSize((150, -1))

        hbox_filter = wx.StaticBoxSizer(wx.StaticBox(
            self.pn_left, wx.NewIdRef(), "Filters"), wx.HORIZONTAL)

        self.window_2 = FilterUltimateListCtrl(self.pn_left)
        hbox_filter.Add(self.window_2, 1, wx.EXPAND, 0)

        self.pn_right = wx.Panel(self, wx.NewIdRef())
        hbox_middle.Add(self.pn_right, 1, wx.EXPAND, 0)

        hbox_result = wx.StaticBoxSizer(wx.StaticBox(
            self.pn_right, wx.NewIdRef(), "Results"), wx.HORIZONTAL)

        self.nb_result = wx.Notebook(self.pn_right, wx.NewIdRef())
        hbox_result.Add(self.nb_result, 1, wx.EXPAND, 0)

        self.pn_right.SetSizer(hbox_result)

        self.pn_left.SetSizer(hbox_filter)

        self.pn_top.SetSizer(hbox_top)

        self.SetSizer(vbox_main)

        self.Layout()
        self.Center(wx.BOTH)
        # end wxGlade

        self.flex_txt_jql_statement.txt_int.Bind(wx.EVT_TEXT_ENTER, self.on_enter_pressed)
        self.Bind(wx.EVT_BUTTON, self.on_button_pressed)

    def on_enter_pressed(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.flex_txt_jql_statement.txt_int.GetId():
            self.search_action()

    def on_button_pressed(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.btn_search.GetId():
            self.search_action()

    def search_action(self):
        print("search")

    def add_new_notebook(self, parent, name):
        nbpn_result = wx.Panel(parent, wx.NewIdRef())
        self.nb_result.AddPage(nbpn_result, name)
        hbox_ulc = wx.BoxSizer(wx.HORIZONTAL)

        self.ulc_result = ResultUltimateListCtrl(nbpn_result)
        hbox_ulc.Add(self.ulc_result, 1, wx.EXPAND, 0)
        nbpn_result.SetSizer(hbox_ulc)
        nbpn_result.Layout()


class FilterUltimateListCtrl(MyUltimateListCtrl):
    def __init__(self, parent):
        MyUltimateListCtrl.__init__(self, parent)
        self.index = None
        self.windows_items_dict = {}
        self.statment_dict = {}

    def configure_list_control(self):
        self.InsertColumn(0, "Saved Filters")
        colw, colh = self.GetParent().GetSize()
        self.SetColumnWidth(0, 190)
        self.btn_add_filter = wx.Button(self, wx.NewIdRef(), "Add Filter",
                                        style=wx.BORDER_NONE)
        self.btn_add_filter.SetToolTip(u"Add Filter")
        self.index = self.InsertStringItem(sys.maxsize, "")
        self.SetItemWindow(self.index, 0, self.btn_add_filter, expand=True)

    def on_button_pressed(self, evt):
        evt_id = evt.GetEventObject().GetId()
        if evt_id == self.btn_add_filter.GetId():
            self.button_add_action()


    def button_add_action(self):
        dlg = AddDialog(self.btn_add_filter)
        item_id = wx.NewId()
        print(type(item_id))
        if dlg.ShowModal() == wx.ID_OK:
            self.statment_dict[dlg.filter_name] = dlg.filter_statement
            dlg.Destroy()
            self.windows_items_dict[item_id] = self.statment_dict
            print("Save new filter:", self.windows_items_dict)
        # parent = self.GetTopLevelParent()
        # parent.add_new_notebook(parent.nb_result, "hello")

    def append_line(self, windows_item):
        index = self.InsertStringItem(self.index, "")
        self.index = index
        btn = wx.Button(self, wx.NewIdRef(), string)
        self.windows_items_dict[btn.GetId()] = string
        self.SetItemWindow(index, 0, btn, expand=True)
  

class ResultUltimateListCtrl(MyUltimateListCtrl):
    def __init__(self, parent):
        super(ResultUltimateListCtrl, self).__init__(parent)

    def configure_list_control(self):
        self.InsertColumn(0, "Filters")
        colw, colh = self.GetParent().GetSize()
        self.SetColumnWidth(0, colw)
        self.btn_add_line = wx.Button(self, wx.NewIdRef(), "Add Filter")
        self.btn_add_line.SetToolTip(u"Add Field")


class AddDialog(wx.Dialog):
    def __init__(self, parent, tooltip="Double Click To Select Your Field"):
        wx.Dialog.__init__(self, parent, style=wx.BORDER_NONE)
        self.SetPosition(self.GetParent().GetPosition())
        self.SetSize((600, 25))
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_statement = wx.TextCtrl(self, id=wx.NewIdRef())
        self.txt_name = wx.TextCtrl(self, id=wx.NewIdRef())
        self.btn_save = wx.Button(self, id=wx.NewIdRef(), label="Save")
        self.btn_cancel = wx.Button(self, id=wx.NewIdRef(), label="Cancel")
        # self.txt_name.SetMinSize((150, -1))
        vbox.Add(self.txt_statement, 1, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 0)
        vbox.Add(self.txt_name, 0, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 0)
        vbox.Add(self.btn_cancel, 0, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 0)
        vbox.Add(self.btn_save, 0, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 0)

        self.filter_name = None
        self.filter_statement = None
        self.SetSizer(vbox)
        # vbox.Fit(self)
        self.Center(wx.BOTH)
        self.Layout()
        self.Bind(wx.EVT_BUTTON, self.on_button_pressed)

        # self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_item_clicked, self.lstb_fields)

    def on_button_pressed(self, evt):
        e_id = evt.GetEventObject().GetId()
        if e_id == self.btn_cancel.GetId():
            self.button_cancel_action()
        elif e_id == self.btn_save.GetId():
            self.filter_name = self.txt_name.GetValue()
            self.filter_statement = self.txt_statement.GetValue()
            self.EndModal(wx.ID_OK)

    def button_cancel_action(self):
        self.EndModal(wx.ID_CANCEL)
        self.Destroy()
        
class MyApp(wx.App):
    def OnInit(self):
        self.jirapickerframe = JiraPickerFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.jirapickerframe)
        self.jirapickerframe.Show()
        return True

# end of class MyApp


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()