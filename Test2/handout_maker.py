import json
from PIL import Image
import os, shutil

from Tests import pdf_convert


class CoordData:
    def __init__(self, template_name):
        self.template_name = template_name
        self.data = {}
        self.workspace = "Exports/Temp_Handout"
        self.outputSpace = "Exports/Temp_Problems"
        self._reset_dir()
        self.data_init()

    def data_init(self):
        with open(f"../Data/templates.json", "r") as f:
            self.data = json.load(f)

    def get_data(self):
        return self.data[self.template_name]

    def _reset_dir(self):
        shutil.rmtree(f"../{self.workspace}")
        os.mkdir(f"../{self.workspace}")
        shutil.rmtree(f"../{self.outputSpace}")
        os.mkdir(f"../{self.outputSpace}")


class FileHandler:
    def __init__(self, file_path, coordData: CoordData):
        self.workspace = coordData.workspace
        self.outputSpace = coordData.outputSpace
        self.file = file_path
        self.data = coordData.get_data()[file_path]
        self.imgNum = 0

    def isImported(self):
        return self.file != ''

    # 1 mm 당 24 pixel -> 610 ppi

    def exportImages(self):
        file_name = self.file.split("/")[-1].split(".")[0]
        if not os.path.exists(f"../{self.workspace}/{file_name}"):
            os.mkdir(f"../{self.workspace}/{file_name}")
        if not os.path.exists(f"../{self.outputSpace}/{file_name}"):
            os.mkdir(f"../{self.outputSpace}/{file_name}")

        thread_list = []
        for page in self.data.keys():
            t = pdf_convert.PdfConverter(self.file, file_name, page, page, dpi=600, temp_path=self.workspace)
            thread_list.append(t)
            t.start()
            if len(thread_list) == 8:
                for thread in thread_list:
                    thread.join()
                thread_list = []

        for t in thread_list:
            t.join()

        for page in self.data.keys():
            img_name = f"../{self.workspace}/{file_name}/{str(page)}.jpg"
            for i, coord in enumerate(self.data[page]):
                img = Image.open(img_name)
                width, height = img.size
                x1, y1 = coord[0][0] / coord[2][0] * width, coord[0][1] / coord[2][1] * height
                x2, y2 = coord[1][0] / coord[2][0] * width, coord[1][1] / coord[2][1] * height
                cropped = img.crop((x1, y1, x2, y2))
                imgPath = f"../{self.outputSpace}/{file_name}/{str(page)}"
                if not os.path.exists(imgPath):
                    os.mkdir(imgPath)
                cropped.save(f"{imgPath}/{str(i + 1)}.jpg")
                print(f"saved: {imgPath}/{str(i + 1)}.jpg")


class HandoutMaker:
    def __init__(self):
        self.width = 5040
        self.height = 7128
        self.img_list = []

    def create_collage(self):
        pass

    def layout_img(self, img):
        pass


class ImageLayout:
    def __init__(self, file_path, r_width, r_height):
        self.file = file_path
        self.width, self.height = self.get_size()
        self.resized_width = r_width
        self.resized_height = r_height

    def get_size(self):
        img = Image.open(self.file)
        return img.size




def main():
    data = CoordData("Sample Template")
    for file in data.get_data().keys():
        f = FileHandler(file, data)
        if f.isImported():
            f.exportImages()


main()
