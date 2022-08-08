import os.path

import PyPDF2
from pdf2image import convert_from_path


def pdfToImg(file_name_n_path):
    print("convert started")

    file = open(file_name_n_path, "rb")
    readpdf = PyPDF2.PdfFileReader(file)
    totalpages = readpdf.getNumPages()

    file_name = file_name_n_path.split("/")[-1].split(".")[0]
    while os.path.exists(f"../Exports/{file_name}"):
        file_name = file_name + "1"
    os.mkdir(f"../Exports/{file_name}")

    for j in range(1, totalpages + 1, 200):
        last_page = j + 199 if j + 199 < totalpages else totalpages
        print(f"converting {j} to {last_page}")
        pages = convert_from_path(file_name_n_path, first_page=j, last_page=last_page, dpi=200)

        for i, page in enumerate(pages):
            img_name = f"../Exports/{file_name}/{str(j + i)}.jpg"
            page.save(img_name, "JPEG")
            print(img_name)

    return file_name
