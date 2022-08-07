from pdf2image import convert_from_path

file_name = "test.pdf"
print("start")

pages = convert_from_path("../Sources/" + file_name, dpi=600)
print("pages are set up now")

for i, page in enumerate(pages):
    img_name = "../Exports/" + "test" + str(i) + ".tiff"
    page.save(img_name, "tiff")
    print(img_name)
