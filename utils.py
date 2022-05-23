import pathlib
import os

import fitz  # PyMuPDF
import sys
import fitz  # import the bindings


def progress_bar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function

    def print_progress_bar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Initial Call
    print_progress_bar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        print_progress_bar(i + 1)
    # Print New Line on Complete
    print()


def filename(path):
    indexslash = path.__str__().rfind("\\") + 1
    indexdot = path.__str__().rfind(".")
    filename = path.__str__()[indexslash:indexdot]
    return filename


def on_done_list(path, name):
    index = path.__str__().rfind("\\") + 1
    filename = path.__str__()[index:]
    with open("done.txt", "a+", encoding="utf-8") as f:
        f.write("\n")
        f.write(name+"\n")
        f.write(filename + "\n")
        f.close()


def already_worked_on(path, name):
    index = path.__str__().rfind("\\") + 1
    newpath = path.__str__()[index:]
    with open('done.txt') as f:
        for line in f:
            if newpath == line.strip() or line.strip() == name:
                return True
    return False


def pdf2png(pdf_path):
    """turns your pdf into a bunch of separate pngs

    Args:
        pdf_path (WindowsPath): path to the pdf

    Returns:
        WindowsPath: path to the folder with the pngs
    """
    doc = fitz.open(pdf_path)  # open document
    fil = filename(pdf_path)
    result_folder_path = pathlib.Path(".\%s" % fil)
    try:
        os.makedirs(fil, exist_ok=False)
    except FileExistsError:
        return result_folder_path

    for page in doc:  # iterate through the pages
        # print("Creating .\%s\page-%i.png" % (fil, page.number))
        pix = page.get_pixmap()  # render page to an image
        pix.save(".\%s\page-%i.png" % (fil, page.number))
    return result_folder_path


def get_num(arr):
    result = arr[0]
    indexslash = result.__str__().rfind("-") + 1
    indexdot = result.__str__().rfind(".")
    number = result[indexslash:indexdot]
    return int(number)


def order(path):
    result = []
    current_arr = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("###"):
                if len(current_arr) > 0:
                    result.append(current_arr)
                    current_arr = []
                current_arr.append(line)
                current_arr.append([])
            else:
                current_arr[1].append(line)
        f.close()
    result.sort(key=get_num)
    return result


def write_sorted(path):
    folder = filename(path)
    text_path = pathlib.Path(r'.\%s\result.md' % (folder))
    arr = order(text_path)
    with open(text_path, "a+", encoding="utf-8") as f:
        f.truncate(0)
        for tuple in arr:
            title = tuple[0]
            f.write(title)
            text = tuple[1]
            for line in text:
                f.write(line)
        f.close()


def text2file(str_arr, pdf_path, title):
    if str_arr is None or len(str_arr) == 0:
        return
    folder = filename(pdf_path)
    path = pathlib.Path(r'.\%s\result.md' % (folder))
    with open(path, "a+", encoding="utf-8") as f:
        f.write("####")
        f.write(title)
        f.write(":")
        f.write("\n")
        for arr in str_arr:
            for str in arr:
                f.write(str)
                f.write(" ")
            f.write("\n")
        f.close()
    return path
