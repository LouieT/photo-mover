
import os
import re
import shutil
import platform
import calendar
import concurrent.futures
from pathlib import Path
from datetime import datetime
from pprint import pprint


class PhotoMover:

    def __init__(self, from_path_root: str, to_path_root: str, date_format: str, file_extensions: list):

        self.from_path = Path(from_path_root)
        self.to_path = Path(to_path_root)
        self.date_format = date_format
        self.datetime_format = "%Y-%m-%d"
        self.file_extensions = file_extensions

    #########################################################################################################
    def build_photos_list(self, file_extenstions: list):

        all_files_lol = []
        all_files_list = []

        for ext in file_extenstions:
            ext_path = f"**/*{ext}"
            all_files_lol.append(list(self.from_path.glob(ext_path)))

        for fl in all_files_lol:
            all_files_list = all_files_list + list(set(fl) - set(all_files_list))

        all_files_list.sort()

        return all_files_list


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
    # TODO - come back to this, for now there id only 1 date format in file path
    def build_dattime_str_from_date_format(self, date_format):

        date_f = date_format.lower()

        datetime_str = ""

        year_in_date = False
        year = None
        month_in_date = False
        month = "%m"
        day_in_date = False
        day = "%d"

        if "y" in date_f:
            year_in_date = True
            y_count = date_f.count("y")
            if y_count <= 2:
                year = "%y"
            else:
                year = "%Y"

        if "m" in date_f:
            month_in_date = True

    #########################################################################################################
    def parse_date_parts(self, date, datetime_format):
        """
        Pas in the datetime format and the date string and return date parts
        :param date_format: datetime date formatting string
        :param date: date a date string
        :return:  year, month, day
        """

        # date = "2019-07-11"
        # date_format = "%Y-%m-%d"

        # date = "7/11/2019"
        # date_format = "%m/%d/%Y"

        d = datetime.strptime(date, datetime_format)

        day = d.day
        month = d.month
        year = d.year

        # print(f"YEAR: {year}  MONTH: {month}  DAY:  {day}")

        return year, month, day

    #########################################################################################################
    def get_file_date_from_path(self, file):

        reg_ex = self.build_date_format_regex(date_format=self.date_format)

        dt = reg_ex.search(str(file))

        if dt is None:
            return dt
        else:
            return dt.group()

    #########################################################################################################
    def move_file(self, from_path, to_path):

        tp_dir = Path(to_path).parent

        # must pass in pathlib path
        exists = Path.exists(tp_dir)

        # If full path does not exist add all non existing directories
        if exists is False:
            tp_dir.mkdir(parents=True, exist_ok=True)

        moved_file = shutil.move(from_path, to_path)
        print(moved_file)

        return moved_file

    #########################################################################################################
    def move_file_from_dict(self, file_data):

        from_path = file_data["original_path"]
        to_path = file_data["new_path"]

        return self.move_file(from_path=from_path, to_path=to_path)

    #########################################################################################################
    '''
    def get_file_times(self):

        all_jpg_files = list(self.from_path.glob("**/*.png"))

        for file in all_jpg_files:

            print(file)
            print(file.name)

            dt = self.get_file_date_from_path(file)

            if dt is None:
                print("No date found.")
            else:
                print(f"FILE DATE: {dt}")
    '''

    #########################################################################################################
    def build_photos_detailed_list(self):

        apl = self.build_photos_list(self.file_extensions)
        all_photos = []

        for file in apl:
            print(file)
            print(file.name)

            date = self.get_file_date_from_path(file=file)
            year, month, day = self.parse_date_parts(date=date, datetime_format=self.datetime_format)

            to_path = self.to_path

            if year is not None:
                to_path = to_path.joinpath(str(year) + "/")
            if month is not None:
                to_path = to_path.joinpath(str(calendar.month_name[month]) + "/")
            if day is not None:
                to_path = to_path.joinpath(str(day) + "/")

            photos = {"file_name": file.name,
                      "original_path": file,
                      "new_path": to_path.joinpath(file.name),
                      "date_string": date,
                      "year": year,
                      "month": month,
                      "day": day
                      }

            pprint(photos, indent=2)

            all_photos.append(photos)

        return all_photos

    #########################################################################################################
    def main(self):

        photos_list = self.build_photos_detailed_list()
        pprint(photos_list, indent=2)

        with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
            result = executor.map(self.move_file_from_dict, photos_list)
            print(result)


if __name__ == "__main__":

    # TODO - Switch this to argparse
    from_p = "/Users/LouisT/Developer/GitHub/photo-mover/test/test_from_path"
    to_p = "/Users/LouisT/Developer/GitHub/photo-mover/test/test_to_path"
    date_format = "YYYY-MM-DD"
    extensions_list = [".png", ".heic"]

    pm = PhotoMover(from_path_root=from_p,
                    to_path_root=to_p,
                    date_format=date_format,
                    file_extensions=[".png", ".jpg", ".heic"])

    pm.main()

