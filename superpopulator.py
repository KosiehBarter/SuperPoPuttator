import tkinter
import xml.etree.ElementTree as ET
import os
import sys

class GUIObject(tkinter.Frame):
    """
        docstring for GUIObject.
    """
    def __init__(self):
        #super(GUIObject, self).__init__()
        self.root_obj = tkinter.Tk()
        self.variable = tkinter.IntVar()
        tkinter.Frame.__init__(self, self.root_obj)

        tkinter.Label(self.root_obj, text = 'XML File path Override').grid(column = 0, row = 0, padx = 10)
        tkinter.Label(self.root_obj, text = 'User name').grid(column = 0, row = 1, padx = 10)
        tkinter.Label(self.root_obj, text = 'Port').grid(column = 0, row = 2, padx = 10)
        tkinter.Label(self.root_obj, text = 'Domain name / Address - Only W/ hostnames').grid(column = 0, row = 3)
        tkinter.Label(self.root_obj, text = 'Server / Host names').grid(columnspan = 2, row = 8, padx = 10)
        tkinter.Label(self.root_obj, text = 'Protocol').grid(columnspan = 2, row = 4, padx = 20)

        tkinter.Radiobutton(self.root_obj, text = "SSH", variable = self.variable, value = "SSH").grid(column = 0, row = 5, sticky = tkinter.W)
        tkinter.Radiobutton(self.root_obj, text = "Telnet", variable = self.variable, value = "Telnet").grid(column = 1, row = 5, sticky = tkinter.W)
        tkinter.Radiobutton(self.root_obj, text = "Serial", variable = self.variable, value = "Serial").grid(column = 0, row = 6, sticky = tkinter.W)
        tkinter.Radiobutton(self.root_obj, text = "Cygterm", variable = self.variable, value = "Cygterm").grid(column = 1, row = 6, sticky = tkinter.W)
        tkinter.Radiobutton(self.root_obj, text = "Minty", variable = self.variable, value = "Minty").grid(column = 0, row = 7, sticky = tkinter.W)
        tkinter.Radiobutton(self.root_obj, text = "RLogin", variable = self.variable, value = "RLogin").grid(column = 1, row = 7, sticky = tkinter.W)

        tkinter.Entry(self.root_obj).grid(column = 1, row = 0, sticky = tkinter.W+tkinter.E)
        tkinter.Entry(self.root_obj).grid(column = 1, row = 1, sticky = tkinter.W+tkinter.E)
        tkinter.Entry(self.root_obj).grid(column = 1, row = 2, sticky = tkinter.W+tkinter.E)
        tkinter.Entry(self.root_obj).grid(column = 1, row = 3, sticky = tkinter.W+tkinter.E)
        tkinter.Text(self.root_obj).grid(columnspan = 2, rowspan = 3, sticky = tkinter.W+tkinter.E+tkinter.S+tkinter.N)

        process_btn = tkinter.Button(self.root_obj, text = "Process", command = self.process_machines).grid(columnspan = 3, sticky = tkinter.W+tkinter.E)
        exit_btn = tkinter.Button(self.root_obj, text = "Exit program", command = self.exit_prog).grid(columnspan = 3, sticky = tkinter.W+tkinter.E)
        self.root_obj.title("SuperPoPuttator")

    def exit_prog(self):
        sys.exit(0)

    def process_machines(self):
        pass

    def load_xml(self):
        pass

class LogicObject(object):
    """
        This is logic designed for actual process.
    """
    def __init__(self):
        super(LogicObject, self).__init__()

        self.file_path = None
        self.xml_file = None
        self.xml_root = None

        self.user_name = None
        self.port = None
        self.domain = None
        self.subfolder = None
        self.proto = None
        self.putty_session = "Default Settings"
        self.extra_args = None

    def set_file(self, path = None):
        self.file_path = path

    def parse_xml(self):
        self.xml_file = ET.parse(self.file_path)

    def get_xml_root(self):
        self.xml_root = self.xml_file.getroot()

    def separate_servers(self, in_str):
        if self.port is None:
            self.port = "22"
        if self.proto is None:
            self.proto = "SSH"
        if self.extra_args is None:
            self.extra_args = ""

        for inc in in_str.split(" "):
            self.append(inc, self.subfolder)

    def append(self, in_host, in_folder):
        if in_folder is not None:       # Neat hack for folders
            in_id = in_folder + "/" + in_host
        else:
            in_id = in_host

        self.xml_root.append(ET.Element("SessionData", {"SessionId": in_id, "SessionName": in_host, "ImageKey": "computer",
                                                        "Host": in_host + "." + self.domain, "Port": self.port, "Proto": self.proto,
                                                        "PuttySession": self.putty_session, "Username": self.user_name, "ExtraArgs": self.extra_args}))

    def write_xml(self, out_file = None):
        self.indent(self.xml_root)
        if out_file is not None:
            self.file_path = out_file
        self.xml_file.write(self.file_path)

    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        j = "\n" + (level-1)*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                self.indent(subelem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem

################################################################################
def main():
    guiobject = GUIObject()
    guiobject.root_obj.mainloop()

if __name__ == '__main__':
    main()
