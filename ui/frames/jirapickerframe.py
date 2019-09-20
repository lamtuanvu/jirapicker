#!/usr/bin/env python
import wx
import sys

from ui.widgets import MyUltimateListCtrl
from ui.widgets import FlexTextCtrl
from ui.widgets import MyPopupMenu
from core.third_party_interaction import MySQLHandler
from core.third_party_interaction import JiraHandler
from icons.iconsets import *
from ui.frames.authentication import LoginFrame


class JiraPickerFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: JiraPickerFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((894, 649))
        self.SetTitle("Jira Picker")
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUBAR))
        
        self.SetIcon(jira_32px.GetIcon())

        self.mysql = MySQLHandler()
        self.myjira = JiraHandler()
        self.statement_items = {}
        vbox_main = wx.BoxSizer(wx.VERTICAL)

        main_w, main_h = self.GetSize()

        self.pn_top = wx.Panel(self, wx.NewIdRef())
        vbox_main.Add(self.pn_top, 0, wx.EXPAND, 0)

        hbox_top = wx.BoxSizer(wx.HORIZONTAL)

        static_text_1 = wx.StaticText(
            self.pn_top, wx.NewIdRef(), "Details of JQL statment")
        hbox_top.Add(static_text_1, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)

        # self.txt_jql_statment = wx.TextCtrl(self.pn_top, wx.NewIdRef(), "")
        self.flex_txt_jql_statement = FlexTextCtrl(self.pn_top, 
                                                   hint="Enter your statement",
                                                   password=False)
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

        self.window_2 = wx.ListBox(self.pn_left)
        # self.window_2 = FilterUltimateListCtrl(self.pn_left)
        hbox_filter.Add(self.window_2, 1, wx.EXPAND, 0)

        self.pn_right = wx.Panel(self, wx.NewIdRef())
        hbox_middle.Add(self.pn_right, 1, wx.EXPAND, 0)

        hbox_result = wx.StaticBoxSizer(wx.StaticBox(
            self.pn_right, wx.NewIdRef(), "Results"), wx.HORIZONTAL)

        self.nb_result = wx.Notebook(self.pn_right, wx.NewIdRef())
        hbox_result.Add(self.nb_result, 1, wx.EXPAND, 0)

        self.pn_top.SetSizer(hbox_top)

        self.pn_right.SetSizer(hbox_result)

        self.pn_left.SetSizer(hbox_filter)

        self.SetSizer(vbox_main)

        self.Layout()
        self.Center(wx.BOTH)
        # end wxGlade

        self.flex_txt_jql_statement.txt_int.Bind(wx.EVT_TEXT_ENTER,
                                                 self.on_enter_pressed)
        self.Bind(wx.EVT_BUTTON, self.on_button_pressed)
        self.btn_search.SetFocus()
        self.window_2.Bind(wx.EVT_LISTBOX, self.on_item_selected)
        self.refresh_action()
        
        dlg = LoginFrame(self)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
            self.Show()
        else:
            pass
            
    def on_enter_pressed(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.flex_txt_jql_statement.txt_int.GetId():
            self.search_action()

    def on_button_pressed(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.btn_search.GetId():
            self.search_action()
        elif eid == self.btn_save_change.GetId():
            self.save_action()

    def on_item_selected(self, evt):
        self.item_selected_action()
        self.window_2.GetStringSelection

    def item_selected_action(self):
        selected_item = self.window_2.GetStringSelection()
        query_statement = self.statement_items[selected_item]
        if self.flex_txt_jql_statement.is_out:
            self.flex_txt_jql_statement.toggle()
        self.flex_txt_jql_statement.txt_int.SetValue(query_statement)
        self.add_new_notebook(self.nb_result, selected_item)
        self.search_action(query_statement)

    def save_action(self):
        values = []
        statement = self.flex_txt_jql_statement.txt_int.GetValue()
        result = self.myjira.check_valid_statement(statement)
        if result:
            wx.MessageBox(result, 'Jira Error', wx.OK | wx.ICON_ERROR)
        else:
            name = None
            dlg = AddDialog(self)
            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.txt_name.GetValue()
                values.append(name)
                values.append(statement)
                self.mysql.write_to_database(table='jql_statement',
                                             fields=['name', 'detail'],
                                             values=values)
                self.refresh_action()
            else:
                self.refresh_action()

    def refresh_action(self):
        filters = self.mysql.get_data_by_fields(table='jql_statement',
                                                fields=['name', 'detail'])
        names = []
        for filter in filters:
            names.append(filter[0])
            self.statement_items[filter[0]] = filter[1]
        self.window_2.AppendItems(names)
        # self.window_2.Append(names[0])
        
    def search_action(self, query_statement):
        results = self.myjira.get_issue_dicts(query_statement)
        for dict in results:
            values = []
            for k, v in dict.items():
                values.append(v)
            self.ulc_result.append_line(values)

    def add_new_notebook(self, parent, name):
        page_list = []
        count = self.nb_result.GetPageCount()
        for i in range(count):
            page_list.append(self.nb_result.GetPageText(i))
        if name not in page_list:
            nbpn_result = wx.Panel(parent, wx.NewIdRef())
            self.nb_result.AddPage(nbpn_result, name, True)
            hbox_ulc = wx.BoxSizer(wx.HORIZONTAL)

            self.ulc_result = ResultUltimateListCtrl(nbpn_result,
                                                     based_columns=['Key',
                                                                    'Summary',
                                                                    'Assignee',
                                                                    'Status',
                                                                    'Updated',
                                                                    'Action'])
            hbox_ulc.Add(self.ulc_result, 1, wx.EXPAND, 0)
            nbpn_result.SetSizer(hbox_ulc)
            nbpn_result.Layout()
        else:
            self.nb_result.SetSelection(page_list.index(name))


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

    def append_line(self, items):
        index = self.InsertStringItem(self.index, "")
        self.index = index
        btn = wx.Button(self, wx.NewIdRef(), string)
        self.windows_items_dict[btn.GetId()] = string
        self.SetItemWindow(index, 0, btn, expand=True)
  

class ResultUltimateListCtrl(MyUltimateListCtrl):
    def __init__(self, parent, **kwargs):
        super(ResultUltimateListCtrl, self).__init__(parent, **kwargs)
        self.index = None

    def configure_list_control(self, columns):
        for column in reversed(columns):
            self.InsertColumn(0, column)
        # colw, colh = self.GetParent().GetSize()
        self.SetColumnWidth(0, 100)
        # self.index = self.InsertStringItem(sys.maxsize, "")

    def append_line(self, items):
        index = self.InsertStringItem(sys.maxsize, "")
        self.index = index
        for item in items:
            if type(item) == str:
                self.SetStringItem(index, items.index(item), item)
        # btn = wx.Button(self, wx.NewIdRef(), string)
        # self.windows_items_dict[btn.GetId()] = string
        # self.SetItemWindow(index, 0, btn, expand=True)

    def on_item_right_click(self, evt):
        self.PopupMenu(MyPopupMenu(self), evt.GetPosition())


class AddDialog(wx.Dialog):
    def __init__(self, parent, tooltip="Double Click To Select Your Field"):
        wx.Dialog.__init__(self, parent, style=wx.BORDER_NONE)
        self.SetPosition(self.GetParent().GetPosition())
        self.SetSize((500, 30))
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_detail = wx.StaticText(self, id=wx.NewIdRef(),
                                        label="Enter Filter Name")
        self.txt_name = wx.TextCtrl(self, id=wx.NewIdRef())
        self.btn_save = wx.Button(self, id=wx.NewIdRef(), label="OK")
        self.btn_cancel = wx.Button(self, id=wx.ID_CANCEL, label="Cancel")
        # self.btn_cancel.Hide()
        # self.txt_name.SetMinSize((150, -1))
        vbox.Add(self.lbl_detail, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        vbox.Add(self.txt_name, 1, wx.ALL | wx.ALIGN_CENTER, 5)
        vbox.Add(self.btn_cancel, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        vbox.Add(self.btn_save, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.filter_name = None
        # self.filter_statement = None
        self.SetSizer(vbox)
        # vbox.Fit(self)
        self.Center(wx.LEFT)
        self.Layout()
        self.Bind(wx.EVT_BUTTON, self.on_button_pressed)
        # self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)
        self.btn_cancel.SetFocus()
        self.SetFocus()
        # self.Bind(wx.EVT_LISTBOX_DCLICK, self.on_item_clicked, self.lstb_fields)

    def on_button_pressed(self, evt):
        e_id = evt.GetEventObject().GetId()
        if e_id == self.btn_save.GetId():
            self.filter_name = self.txt_name.GetValue()
            # self.filter_statement = self.txt_statement.GetValue()
            self.EndModal(wx.ID_OK)
        elif e_id == wx.ID_CANCEL:
            self.button_cancel_action()

    def button_cancel_action(self):
        # self.EndModal(wx.ID_CANCEL)
        self.Destroy()

    
class MyApp(wx.App):
    def OnInit(self):
        self.jirapickerframe = JiraPickerFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.jirapickerframe)
        # self.jirapickerframe.Show()
        return True

# end of class MyApp


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
