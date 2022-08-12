import PyPDF2
from pdf2image import convert_from_path
import threading
import time


class PdfConverter(threading.Thread):
    def __init__(self, file_name_n_path, name, start, end, dpi=200):
        super().__init__()
        self.file_name_n_path = file_name_n_path
        self.name = name
        self.first = start
        self.last = end
        self.dpi = dpi

    def run(self):
        print(f"converting {self.first} to {self.last}")
        pdfToImg(self.file_name_n_path, self.name, self.first, self.last, self.dpi)


def getPageAmount(file):
    file = open(file, "rb")
    readpdf = PyPDF2.PdfFileReader(file)
    totalpages = readpdf.getNumPages()
    return totalpages


def pdfToImg(file_name_n_path, name, start, end, dpi=200):

    pages = convert_from_path(file_name_n_path, first_page=start, last_page=end, dpi=dpi)

    for i, page in enumerate(pages):
        img_name = f"../Exports/Temp/{name}/{str(start + i)}.jpg"
        page.save(img_name, "JPEG")
