#!/usr/bin/env python
import wx
import sys

from ui.widgets import MyUltimateListCtrl
from ui.widgets import FlexTextCtrl
from ui.widgets import MyPopupMenu
from ui.frames.dialogs import AddDialog
from ui.frames.dialogs import AssignTaskDialog
from ui.frames.authentication import LoginFrame
from core.third_party_interaction import MySQLHandler
from core.third_party_interaction import JiraHandler
from core.third_party_interaction import MyOutlookHandler
from icons.iconsets import *


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

        # Define internal variables
        self._mysql = MySQLHandler()
        self._myjira = JiraHandler()
        self._statement_items = {}
        self._ulc_results = {}
        self._ulc_columns = ['Key', 'Summary', 'Assignee',
                             'Status', 'Updated', 'Action',
                             'TMA-Assignee', 'TMA-Last Assignee']
        self.users = []
        self.logged_user = None

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

        self._bind_all()
        self._initiate()

    # Bind all event
    def _bind_all(self):
        self.flex_txt_jql_statement.txt_int.Bind(wx.EVT_TEXT_ENTER,
                                                 self.on_enter_pressed)
        self.Bind(wx.EVT_BUTTON, self.on_button_pressed)
        self.window_2.Bind(wx.EVT_LISTBOX, self.on_item_selected)
        self.flex_txt_jql_statement.txt_int.Bind(wx.EVT_TEXT,
                                                 self.on_text_change)

    def _initiate(self):
        # Initiation with login dialog
        dlg = LoginFrame(self)
        if dlg.ShowModal() == wx.ID_OK:
            self.logged_user = dlg.logged_user
            dlg.Destroy()
            self.Show()
        else:
            self.Destroy()

        # Button initiate States
        self.btn_save_change.Enable(False)
        self.btn_search.SetFocus()

        # Fetch all data from database
        self.refresh_action()
        

    def on_text_change(self, evt):
        # Check the saved statements were changed or not
        current_statement = self.flex_txt_jql_statement.txt_int.GetValue()
        is_exist = False
        for k, v in self._statement_items.items():
            if v == current_statement:
                is_exist = True
        if is_exist:
            self.btn_save_change.Enable(False)
        else:
            self.btn_save_change.Enable()

    def on_enter_pressed(self, evt):
        # Process search when enter is pressed
        eid = evt.GetEventObject().GetId()
        if eid == self.flex_txt_jql_statement.txt_int.GetId():
            self.search_action(self.flex_txt_jql_statement.txt_int.GetValue(), "Search")

    def on_button_pressed(self, evt):
        eid = evt.GetEventObject().GetId()
        if eid == self.btn_search.GetId():
            """Add new notebook if not existed,
            Process search action after that
            """
            self.add_new_notebook(self.nb_result, "Search")
            self.search_action(self.flex_txt_jql_statement.txt_int.GetValue(), "Search")
        elif eid == self.btn_save_change.GetId():
            self.save_action()

    def on_item_selected(self, evt):
        self.item_selected_action()
        # self.window_2.GetStringSelection

    def item_selected_action(self):
        """[summary] Process the add new notebook action
        then query data for Jira server
        """
        selected_item = self.window_2.GetStringSelection()
        query_statement = self._statement_items[selected_item]
        if self.flex_txt_jql_statement.is_out:
            self.flex_txt_jql_statement.toggle()
        self.flex_txt_jql_statement.txt_int.SetValue(query_statement)
        self.add_new_notebook(self.nb_result, selected_item)
        self.search_action(query_statement, selected_item)

    def save_action(self):
        # Save the jql statement to database
        values = []
        statement = self.flex_txt_jql_statement.txt_int.GetValue()
        result = self._myjira.check_valid_statement(statement)
        if result:
            wx.MessageBox(result, 'Jira Error', wx.OK | wx.ICON_ERROR)
        else:
            name = None
            dlg = AddDialog(self)
            if dlg.ShowModal() == wx.ID_OK:
                name = dlg.txt_name.GetValue()
                values.append(name)
                values.append(statement)
                self._mysql.write_to_database(table='jql_statement',
                                             fields=['name', 'detail'],
                                             values=values)
                self.refresh_action()
            else:
                self.refresh_action()

    def refresh_action(self):
        # Refetch all data from database
        self._mysql.cnx.close
        self._mysql.cursor.close
        del self._mysql

        self._mysql = MySQLHandler()

        filters = self._mysql.get_data_by_fields(table='jql_statement',
                                                fields=['name', 'detail'])
        names = []
        for filter in filters:
            names.append(filter[0])
            self._statement_items[filter[0]] = filter[1]
        self.window_2.Clear()
        self.window_2.AppendItems(names)
        users = self._mysql.get_data_by_fields(table='user',
                                               fields=['username',
                                                       'first_name',
                                                       'last_name'])

        for value in users:
            user = {}
            user['username'] = value[0]
            user['displayname'] = value[1] + ' ' + value[2]
            self.users.append(user)


        # self.window_2.Append(names[0])

    def search_action(self, query_statement, name):
        """[summary] Search tickets by provided statement
        
        Arguments:
            query_statement {[string]} -- [JQL query statement]
            name {[str]} -- [Name of search statement which used
            to create notebook page]
        """
        ulc_result = self._ulc_results[name]
        ulc_result.DeleteAllItems()
        results = self._myjira.get_issue_dicts(query_statement)
        for dict in results:
            values = []
            for k, v in dict.items():
                values.append(v)
            print("len values ", values)
            self._mysql.write_to_database(table='tickets', 
                                          fields=['ticket',
                                                  'title',
                                                  'assignee',
                                                  'status',
                                                  'updated'], values=values)
            break

        self._mysql.cnx.close()

        # for k, v in self._ulc_results.items():
            # print ("List of Items: ", v.GetItemCount())

    def add_new_notebook(self, parent, name):
        """[summary] Add new page to notebook
        Check the page name
        then create a new page if note exist
        Arguments:
            parent {[wxobject]} -- [parent widget]
            name {[str]} -- [name of page]
        """
        if self.check_page_exist(name) is not None:
            self.nb_result.SetSelection(self.check_page_exist(name))
        else:
            nbpn_result = wx.Panel(parent, wx.NewIdRef())
            self.nb_result.AddPage(nbpn_result, name, True)
            hbox_ulc = wx.BoxSizer(wx.HORIZONTAL)

            self._ulc_results[name] = ResultUltimateListCtrl(nbpn_result,
                                                     based_columns=self._ulc_columns)
            hbox_ulc.Add(self._ulc_results[name], 1, wx.EXPAND, 0)
            nbpn_result.SetSizer(hbox_ulc)
            nbpn_result.Layout()

    def check_page_exist(self, page_name):
        """[summary] Check whether the page name is exist or not
        
        Arguments:
            page_name {[str]} -- [Name of the note book page]
        
        Returns:
            [boolen] -- [description]
        """
        page_list = []
        count = self.nb_result.GetPageCount()
        for i in range(count):
            page_list.append(self.nb_result.GetPageText(i))
        if page_name in page_list:
            page_index = page_list.index(page_name)
            return page_index
        else:
            return None


class FilterUltimateListCtrl(MyUltimateListCtrl):
    def __init__(self, parent):
        """[summary] Initiate the Ultimate List Ctrl
        
        Arguments:
            MyUltimateListCtrl {[type]} -- [description]
            parent {[type]} -- [description]
        """
        MyUltimateListCtrl.__init__(self, parent)
        self.index = None
        self.windows_items_dict = {}
        self.statment_dict = {}

    def configure_list_control(self):
        """[summary] This method is overriden from MyUltimateListCtrl
        """
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
        """[summary] Add new line with provided items to ULC
        
        Arguments:
            items {[List]} -- [List of item's value]
        """
        index = self.InsertStringItem(self.index, "")
        self.index = index
        btn = wx.Button(self, wx.NewIdRef(), string)
        self.windows_items_dict[btn.GetId()] = string
        self.SetItemWindow(index, 0, btn, expand=True)

    def clear_ulc(self):
        # for i in range(1, self.index):
        self.DeleteAllItems()


class ResultUltimateListCtrl(MyUltimateListCtrl):
    def __init__(self, parent, **kwargs):
        super(ResultUltimateListCtrl, self).__init__(parent, **kwargs)
        self.__index = None
        self._myoutlook = MyOutlookHandler()
        self._columns = kwargs['based_columns']

    def configure_list_control(self, columns):
        for column in reversed(columns):
            self.InsertColumn(0, column)
        # colw, colh = self.GetParent().GetSize()
        self.SetColumnWidth(0, 100)
        # self.index = self.InsertStringItem(sys.maxsize, "")

    def append_line(self, items):
        index = self.InsertStringItem(sys.maxsize, "")
        self.__index = index
        for item in items:
            if type(item) == str:
                self.SetStringItem(index, items.index(item), item)
        # btn = wx.Button(self, wx.NewIdRef(), string)
        # self.windows_items_dict[btn.GetId()] = string
        # self.SetItemWindow(index, 0, btn, expand=True)

    def assign_action(self):
        index = self.GetFirstSelected()
        users = self.GetTopLevelParent().users
        logged_user = self.GetTopLevelParent().logged_user
        logged_user_display = None
        username = []
        for user in users:
            if user.get('username') == logged_user:
                logged_user_display = user.get('displayname')
            username.append(user.get('username'))
        assignee = ''
        items_value = []
        
        for i in range(len(self._columns)):
            items = self.GetItem(index, col=i)
            items_value.append(items.GetText())
        subject = '[Jira Support]: ' + items_value[0] + ' - ' + items_value[1]
        body = "Hi ,\nPlease help to support this ticket.\n\nThanks,\n{}.".format(logged_user_display)

        dlg = AssignTaskDialog(self, username, subject, body)
        if dlg.ShowModal() == wx.ID_OK:
            # assignee = dlg.selected
            dlg.Destroy()

        print("ASsign item: ", items_value)

    def on_item_right_click(self, evt):
        print(self.GetFirstSelected())
        if self.GetFirstSelected() != -1:
            self.PopupMenu(MyPopupMenu(self), evt.GetPosition())


def test():
    app = wx.App()
    test_object = JiraPickerFrame(None, wx.ID_ANY, "")
    app.SetTopWindow(test_object)
    app.MainLoop()


if __name__ == "__main__":
    test()
