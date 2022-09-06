# import PyPDF2
# from pdf2image import convert_from_path
# import threading
# import time
#
#
# class PdfConverter(threading.Thread):
#     def __init__(self, file_name_n_path, name, start, end, dpi=200, temp_path="Exports/Temp"):
#         super().__init__()
#         self.file_name_n_path = file_name_n_path
#         self.name = name
#         self.first = int(start)
#         self.last = int(end)
#         self.dpi = int(dpi)
#         self.temp_path = temp_path
#
#     def run(self):
#         print(f"converting {self.first} to {self.last}")
#         pdfToImg(self.file_name_n_path, self.name, self.first, self.last, dpi=self.dpi, temp_path=self.temp_path)
#
#
# def getPageAmount(fileH):
#     fileH = open(fileH, "rb")
#     readpdf = PyPDF2.PdfFileReader(fileH)
#     totalpages = readpdf.getNumPages()
#     return totalpages
#
#
# def pdfToImg(file_name_n_path, name, start, end, dpi=200, temp_path="Exports/Temp"):
#
#     pagesH = convert_from_path(file_name_n_path, first_page=start, last_page=end, dpi=dpi)
#
#     for i, pageH in enumerate(pagesH):
#         img_name = f"../{temp_path}/{name}/{str(start + i)}.jpg"
#         pageH.save(img_name, "JPEG")
