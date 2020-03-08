
import os
import shutil
from pathlib import Path


class PhotoMover:

    def __init__(self, from_path_root: str, to_path_root: str):

        self.from_path = Path(from_path_root)
        self.to_path = Path(to_path_root)

    def build_photos_list(self):

        all_files = os.listdir(self.from_path)

        all_png_files = self.from_path.glob("**/*.png")
        all_jpg_files = self.from_path.glob("**/.jpg")

        print(all_png_files)
        print(all_jpg_files)

        #print(os.listdir(self.from_path))


if __name__ == "__main__":

    our_var = f"OLIVIA:  \n" \
        f"yrhhuhwgiyijko" \
        f"[poigyujhikrjtguujurjkoohghrgbnskhajhhi44ghyuj8jiqyiotyuhi4u81"

    print(our_var)

    from_p = "/Users/LouisT/Developer/GitHub/photo-mover/test_from_path"
    to_p = ""

    pm = PhotoMover(from_path_root=from_p, to_path_root=to_p)
    pm.build_photos_list()
