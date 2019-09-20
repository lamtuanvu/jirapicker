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
        if not server:
            server = 'https://jira.atlassian.com'
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
        issues = None
        try:
            issues = self.search_issues(query)
        except JIRAError as err:
            print(err.text)
            return None
        return issues
    
    def check_valid_statement(self, query):
        """[summary] Check validity of JQL statement
        
        Arguments:
            query {[type]} -- [description]
        """
        try:
            self.search_issues(query)
        except JIRAError as err:
            return err.text
        return None

    def get_issue_dicts(self, query):
        """[summary] Get the list of issues as dictionary format
        
        Arguments:
            query {[string]} -- [description]
        Return: dictionary for list of issues
        """
        issues = self.query_issues(query)
        issue_dict_list = []
        if issues:
            for issue in issues:
                issue_dict_list.append(self.parser_issue_info(issue))
        return issue_dict_list

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
    def __init__(self, user='testpicker', password='12345678x@X',
                 host='192.168.86.151', database='jirapicker'):
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

    def write_to_database(self, table="tickets", fields=[], values=[]):
        fields_string = ', '.join(['`%s`']*len(fields)) % tuple(fields)
        values_string = ', '.join(['%s']*len(values))
        command = """INSERT INTO `tickets`(`ticket id`, `type`, `title`,
                     `reporter`, `created_date`)
                     VALUES ([value-1],[value-2],[value-3],[value-4],[value-5])
                  """
        if len(fields) != len(values):
            print("Length of values and fields does not match")

        cmd = """INSERT INTO `%s`(%s)
                 VALUES (%s)""" % (table, fields_string, values_string)

        print("Executed command:, ", cmd)
        try:
            self.cursor.execute(cmd, tuple(values))
            self.cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                return "Duplicated"
            else:
                return err.msg
        return True
            # return "Error happens: {}".format(err)
        # return True

    def get_data_by_fields(self, table="ticket", fields=[]):
        fields_string = ', '.join(['`%s`']*len(fields)) % tuple(fields)
        cmd = """SELECT %s FROM `%s`""" % (fields_string, table)
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def get_data_by_id(self, table="", fields=[], field="", id=""):
        fields_string = ', '.join(['`%s`']*len(fields)) % tuple(fields)
        cmd = """SELECT %s FROM `%s`
                 WHERE `%s` = '%s'""" % (fields_string, table, field, id)
        print("COMMAND: ", cmd)
        self.cursor.execute(cmd, id)
        return self.cursor.fetchall()


class MyOutlookHandler:
    def __init__(self):
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(win32.constants.olTaskItem)
        mail.To = 'To address'
        mail.Subject = 'Message subject'
        mail.Body = 'Message body'
        mail.HTMLBody = '<h2>HTML Message body</h2>'

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
