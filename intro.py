import pathlib
import argparse
from tkinter import W

__prog_name__ = "extract-highlight"
__version__ = "0.1.1"

from hext import  process
from utils import pdf2png, text2file, filename, progress_bar, write_sorted
import sys, os


def main():

    input = sys.argv[1]

    png_folder = pdf2png(input)
    # Do stuff...
    for png in progress_bar(os.listdir(png_folder), prefix = 'Progress:', suffix = 'Complete', length = 50):
        if not png.endswith(".png"):
            continue
        png_path = os.path.join(png_folder, png)
        #print("Working on %s" % filename(png_path))
        process(png_path, input, png)
    write_sorted(input)
    print("OK")



if __name__ == "__main__":
    main()
