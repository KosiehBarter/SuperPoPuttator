import tkinter
import xml.etree.ElementTree as ET


class GUIObject(object):
    """
        docstring for GUIObject.
    """
    def __init__(self):
        super(GUIObject, self).__init__()

class LogicObject(object):
    """
        docstring for LogicObject.
    """
    def __init__(self):
        super(LogicObject, self).__init__()

        self.file_path = None
        self.xml_file = None
        self.xml_root = None

        self.user_name = None
        self.server_list = []
        self.server_list_str = None         # Debug

    def set_file(self, path = None):
        self.file_path = path

    def parse_xml(self):
        self.xml_file = ET.parse(self.file_path)

    def get_xml_root(self):
        self.xml_root = self.xml_file.getroot()

    def separate_servers(self, in_str):
        self.server_list = in_str.split(" ")

    def append(self, in_address, in_port, in_id, in_host, in_proto,
               in_user, in_folder = None, putty_session = None):
        if in_folder is not None:
            in_id = in_folder + "/" + in_id
        if putty_session is None:
            putty_session = "Default Settings"
        self.xml_root.append(ET.Element("SessionData", {"ExtraArgs": "", "Host": str(in_address),
                                                        "Port": str(in_port), "Username": in_user,
                                                        "ImageKey": "computer", "SessionId": in_id,
                                                        "SessionName": in_host, "Proto": in_proto,
                                                        "PuttySession": putty_session}))

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

if __name__ == '__main__':
    main()
