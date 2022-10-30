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
    grayscale = False
    if sys.argv.__len__() > 2 and sys.argv[2] == "gray":
        grayscale = True
    png_folder = pdf2png(input)
    for png in progress_bar(os.listdir(png_folder), prefix = 'Progress:', suffix = 'Complete', length = 50):
        if not png.endswith(".png"):
            continue
        png_path = os.path.join(png_folder, png)
        process(png_path, input, png, png_folder, grayscale)
    write_sorted(png_folder)
    print("OK")



if __name__ == "__main__":
    main()
