#!/usr/bin/python3
"""[summary]
=====================================
Jira interaction
=====================================
:Author: Vu Lam, lamtuanvuqs@gmail.com
:Date: 2019-09-16
Sources: N/A
"""
import mysql.connector
import win32com.client as win32
import os
import subprocess

from mysql.connector import errorcode
from jira import JIRA
from jira import JIRAError


class JiraHandler(JIRA):
    def __init__(self, *args, **kwargs):
        user = None
        password = None
        server = None
        basic_auth = None
        for key, value in kwargs.items():
            if key == "user":
                user = value
            elif key == "password":
                password = value
                user = value
            elif key == "server":
                server = value
        if user and password:
            basic_auth = (user, password)
        try:
            super(JiraHandler, self).__init__(server=server,
                                              basic_auth=basic_auth)
        except JIRAError as err:
            print(err.text)

    def query_issues(self, query):
        """[summary] Get the issues instance by JQL query statement

        Arguments:
            query {[string]} -- [JQL statement]
        """
        return self.search_issues(query)

    @staticmethod
    def parser_issue_info(issue):
        """[summary] Get needed information from issue's instance

        Arguments:
            issue {object} -- [issue instance]
        """
        results_dict = {}
        raw_info = issue.raw
        fields = raw_info['fields']
        results_dict["key"] = raw_info["key"]
        results_dict["summary"] = fields["summary"]
        results_dict["assignee"] = fields["assignee"]["displayName"]
        results_dict["status"] = fields["status"]['name']
        results_dict["updated"] = fields["updated"]

        return results_dict


class MySQLHandler:
    def __init__(self, user='jirapicker', password='12345678x@X',
                 host='192.168.86.151', database='testpicker'):
        try:
            self.cnx = mysql.connector.connect(user=user, password=password,
                                               host=host,
                                               database=database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.cursor = self.cnx.cursor()


class MyOutlookHandler:
    # Drafting and sending email notification to senders. You can add other senders' email in the list
    def __init__(self, to, legatoStatus, atStatus):
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(win32.constants.olTaskItem)
        mail.To = 'To address'
        mail.Subject = 'Message subject'
        mail.Body = 'Message body'
        mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional

        # To attach a file to the email (optional):
        attachment  = "Path to the attachment"
        mail.Attachments.Add(attachment)

        mail.Send()

    def create_jira_task(self, receiver, contents):
        pass

    def foward_email(self, msg):
        msg.To = self.to
        msg.Cc = "lamtuanvuqs@gmail.com;lamtuanvu92@yahoo.com"
        msg.SentOnBehalfOfName = ''
        msg.send

    def open_outlook(self):
        try:
            subprocess.call(['C:\\Program Files'
                             '\\Microsoft Office\\Office16\\Outlook.exe'])
            os.system("C:\\Program Files"
                      "\\Microsoft Office\\Office16\\Outlook.exe")
        except errorcode:
            print ("Outlook didn't open successfully")

    def check_legato_mail(self, legatoFolders):
        folder = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")

        legatoFolders = legatoFolders.split("\\")
        for legatoFolder in legatoFolders:
            folder = folder.Folders(legatoFolder)

        msgs = folder.Items
        toSend=[]
        for msg in msgs:
            if msg.unread:
                toSend.append(msg)

        answer = wx.MessageBox("There are %d message will be sent to %s.?. Do you want to process it? yes/no: " %(len(toSend), self.to), 'Confirmation', wx.YES_NO)
        if answer == wx.YES:
            for msg in toSend:
                msg.unread=False
                self.foward_email(msg)

        else:
            print "\nNothing will be sent"

    def check_AT_mail(self, atFolders):
        folder = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
        try:
            atFolders = atFolders.split("\\")
            for atFolder in atFolders:
                folder = folder.Folders(atFolder)

            msgs = folder.Items
            toSend=[]
            for msg in msgs:
                if msg.unread:
                    if msg.Attachments.Count != 0:
                        toSend.append(msg)
                    elif msg.Attachments.Count == 0:
                        print "Test case %s doesn't have attachment"
                        answer = wx.MessageBox("Test case %s doesn't have attachment. Do you want to send it anyway" %(msg.Subject), 'Confirmation', wx.YES_NO)
                        if answer == wx.YES:
                            toSend.append(msg)

            answer = wx.MessageBox("There are %d message will be sent to %s?. Do you want to process it? yes/no: " %(len(toSend), self.to), 'Confirmation', wx.YES_NO)
            if answer == wx.YES:
                for msg in toSend:
                    msg.unread=False
                    self.foward_email(msg)

            else:
                print "\nNothing will be sent"
        except:
            print "Failed to sent"
