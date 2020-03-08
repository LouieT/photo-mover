
import os
import re
import shutil
import platform
from pathlib import Path
from datetime import datetime


class PhotoMover:

    def __init__(self, from_path_root: str, to_path_root: str):

        self.from_path = Path(from_path_root)
        self.to_path = Path(to_path_root)
        self.date_format = "YYYY-MM-DD"

    def build_photos_list(self):

        all_files = os.listdir(self.from_path)
        print(all_files)

        all_png_files = list(self.from_path.glob("**/*.png"))
        all_jpg_files = list(self.from_path.glob("**/*.jpg"))

        print(all_png_files)
        print(all_jpg_files)

        #print(os.listdir(self.from_path))

    #########################################################################################################
    @staticmethod
    def get_file_creation_date_from_system(file):
        """
        The “ctime” as reported by the operating system. On some systems (like Unix) is the time of the last
        metadata change, and, on others (like Windows), is the creation time (see platform documentation for
        details). Mac should have a "st_birthtime" property for creation time but Linux does not.

        :param file: The full path including file name of the file to check

        :return: the datetime of the file creation time
        """

        data = os.stat(file)

        if platform.system() == "Windows":
            return datetime.fromtimestamp(data.st_ctime)
        else:
            try:
                return datetime.fromtimestamp(data.st_birthtime)
            except AttributeError:
                return datetime.fromtimestamp(data.st_ctime)

    #########################################################################################################
    def build_date_format_regex(self, date_format):
        """
        Check th input date format and build a regex from it to be used to search matching date formats
        :param date_format:
        :return:
        """

        regex_string = ""

        for c in date_format:
            if c.isalnum():
                regex_string += r"\d"
            else:
                regex_string += c

        return re.compile(regex_string)

    #########################################################################################################
    def get_file_date_from_path(self, file, date_format):

        reg_ex = self.build_date_format_regex(date_format=date_format)

        dt = reg_ex.search(str(file))

        if dt is None:
            return dt
        else:
            return dt.group()

    #########################################################################################################
    def move_file(self, from_path, to_path):

        moved_file = shutil.move(from_path, to_path)
        return moved_file

    #########################################################################################################
    def get_file_times(self):

        all_jpg_files = list(self.from_path.glob("**/*.png"))

        for file in all_jpg_files:

            dt = self.get_file_date_from_path(file, "YYYY-MM-DD")

            if dt is None:
                print("No date found.")
            else:
                print(f"FILE DATE: {dt}")


if __name__ == "__main__":

    from_p = "/Users/LouisT/Developer/GitHub/photo-mover/test/test_from_path"
    to_p = "/Users/LouisT/Developer/GitHub/photo-mover/test/test_to_path"

    pm = PhotoMover(from_path_root=from_p, to_path_root=to_p)

    # reg = pm.get_file_date_from_path("f", "df")

    # pm.build_photos_list()

    # pm.get_file_creation_data(file=from_p + "/seahawks-classic.png")

    pm.get_file_times()

    '''
    pm.move_file(from_path=from_p + "/seahawks-classic.png",
                 to_path=to_p + "/seahawks-classic.png")
    '''
