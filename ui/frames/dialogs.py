import wx
import wx.adv

from core.third_party_interaction import MyOutlookHandler

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


class AssignTaskDialog(wx.Dialog):
    def __init__(self, parent, *args):
        wx.Dialog.__init__(self, parent, style=wx.DEFAULT_DIALOG_STYLE)
        _to = args[0]
        _subject = args[1]
        _body = args[2]
        self.SetTitle("Task Creation...")
        self.SetSize((800, 600))

        self.myoutlook = MyOutlookHandler()

        vbox_main = wx.BoxSizer(wx.VERTICAL)
        hbox_function = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_send = wx.Button(self, wx.NewIdRef(), label="Send")
        self.btn_send.SetBitmap(wx.Bitmap('D:\\Workspace\\jirapicker\\icons\\icons8-email-send-20.png', wx.BITMAP_TYPE_ANY), wx.BOTTOM)
        # self.btn_send.SetBitmapMargins((1, 1))
        hbox_function.Add(self.btn_send, 0, wx.ALL, 5)

        vbox_option = wx.BoxSizer(wx.VERTICAL)
        hbox_to = wx.BoxSizer(wx.HORIZONTAL)
        hbox_subject = wx.BoxSizer(wx.HORIZONTAL)
        hbox_startdate = wx.BoxSizer(wx.HORIZONTAL)
        hbox_duedate = wx.BoxSizer(wx.HORIZONTAL)

        lbl_to = wx.StaticText(self, wx.ID_ANY, label="To")
        lbl_to.SetMinSize((60, -1))
        hbox_to.Add(lbl_to, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        self.cb_to = wx.Choice(self, wx.NewIdRef(), choices=_to)
        hbox_to.Add(self.cb_to, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        vbox_option.Add(hbox_to, 0, wx.EXPAND | wx.ALL, 5)

        lbl_subject = wx.StaticText(self, wx.ID_ANY, label="Subject")
        lbl_subject.SetMinSize((60, -1))
        hbox_subject.Add(lbl_subject, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        self.txt_subject = wx.TextCtrl(self, wx.NewIdRef())
        hbox_subject.Add(self.txt_subject, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
        self.txt_subject.SetValue(_subject)

        vbox_option.Add(hbox_subject, 0, wx.EXPAND | wx.ALL, 5)

        lbl_startdate = wx.StaticText(self, wx.ID_ANY, label="Start Date")
        lbl_startdate.SetMinSize((60, -1))
        hbox_startdate.Add(lbl_startdate, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        self.dpk_statedate = wx.adv.DatePickerCtrl(self, wx.NewIdRef(), style=wx.adv.DP_DROPDOWN)
        hbox_startdate.Add(self.dpk_statedate, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        lbl_status = wx.StaticText(self, wx.ID_ANY, label="Status")
        hbox_startdate.Add(lbl_status, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        self.cb_status = wx.Choice(self, wx.NewIdRef(), choices=['Not Started',
                                                                 'In Progress',
                                                                 'Completed',
                                                                 'Waiting for someone else'])
        hbox_startdate.Add(self.cb_status, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
        self.cb_status.SetStringSelection("Not Started")

        vbox_option.Add(hbox_startdate, 0, wx.EXPAND | wx.ALL, 5)

        lbl_duedate = wx.StaticText(self, wx.ID_ANY, label="Due Date")
        lbl_duedate.SetMinSize((60, -1))
        hbox_duedate.Add(lbl_duedate, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        self.dpk_duedate = wx.adv.DatePickerCtrl(self, wx.NewIdRef(), style=wx.adv.DP_DROPDOWN)
        hbox_duedate.Add(self.dpk_duedate, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        lbl_priority = wx.StaticText(self, wx.ID_ANY, label="Priority")
        hbox_duedate.Add(lbl_priority, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        self.cb_priority = wx.Choice(self, wx.NewIdRef(),
                                     choices=['High', 'Normal', 'Low'])
        hbox_duedate.Add(self.cb_priority, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)
        self.cb_priority.SetStringSelection('Normal')

        lbl_complete = wx.StaticText(self, wx.ID_ANY, label="% Complete")
        hbox_duedate.Add(lbl_complete, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        self.sp_complete = wx.SpinCtrl(self, wx.NewIdRef())
        hbox_duedate.Add(self.sp_complete, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        vbox_option.Add(hbox_duedate, 0, wx.EXPAND | wx.ALL, 5)

        self.ckb_kupdate = wx.CheckBox(self, wx.NewIdRef(),
                                       label="Keep an updated copy of this task on my task list")
        vbox_option.Add(self.ckb_kupdate, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        self.ckb_gstatus = wx.CheckBox(self, wx.NewIdRef(),
                                       label="Send me a status report when this task is complete")
        vbox_option.Add(self.ckb_gstatus, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        hbox_function.Add(vbox_option, 1, wx.ALL | wx.EXPAND, 5)

        vbox_main.Add(hbox_function, 0, wx.ALL | wx.EXPAND, 5)

        self.txt_main = wx.TextCtrl(self, wx.NewIdRef(), style=wx.TE_MULTILINE)

        vbox_main.Add(self.txt_main, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 5)

        self.txt_main.SetValue(_body)

        """
        self.lstb_choose = wx.ListBox(self, wx.NewIdRef(), choices=choices)
        vbox.Add(self.lstb_choose, 1, wx.EXPAND, 0)"""
        self.SetSizer(vbox_main)
        self.Layout()
        self.Center(wx.BOTH)
        # self.Fit()

        self.selected = None

        self.Bind(wx.EVT_BUTTON, self.on_button_pressed)

        # self.lstb_choose.Bind(wx.EVT_LISTBOX_DCLICK, self.on_lstb_click)

    def on_lstb_click(self, evt):
        self.selected = self.lstb_choose.GetStringSelection()
        self.EndModal(wx.ID_OK)

    def on_button_pressed(self, evt):
        to = self.cb_to.GetStringSelection() + '@tma.com.vn'
        subject = self.txt_subject.GetValue()
        body = self.txt_main.GetValue()
        startdate = self.dpk_statedate.GetValue()
        duedate = self.dpk_statedate.GetValue()
        status = self.cb_status.GetStringSelection()
        priority = self.cb_priority.GetStringSelection()
        startdate
        contents = {}
        contents['To'] = to
        contents['Subject'] = subject
        contents['Body'] = body
        contents['Startdate'] = startdate
        contents['Duedate'] = duedate
        contents['Status'] = status
        contents['Priority'] = priority

        print(contents)

        msg = self.myoutlook.create_task(contents)
        msg.Save()
        self.EndModal(wx.ID_OK)

    def action_update():
        pass


def test():
    app = wx.App()
    dlg = AssignTaskDialog(None)
    dlg.ShowModal()
    app.MainLoop()


if __name__ == "__main__":
    test()