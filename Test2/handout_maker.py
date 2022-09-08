from PIL import Image, ImageDraw, ImageFont

from Refractor1.classes.coord import Coord
from Refractor1.classes.data_handler import DataFileHandler, DataHandler


# class CoordData:
#     def __init__(self, template_name):
#         self.template_name = template_name
#         self.data = {}
#         self.workspace = "Exports/Temp_Handout"
#         self.outputSpace = "Exports/Temp_Problems"
#         self._reset_dir()
#         self.data_init()
#
#     def data_init(self):
#         with open(f"../Data/templates.json", "r") as f:
#             self.data = json.load(f)
#
#     def get_data(self):
#         return self.data[self.template_name]
#
#     def _reset_dir(self):
#         shutil.rmtree(f"../{self.workspace}")
#         os.mkdir(f"../{self.workspace}")
#         shutil.rmtree(f"../{self.outputSpace}")
#         os.mkdir(f"../{self.outputSpace}")
#
#
# class FileHandler:
#     def __init__(self, file_path, coordData: CoordData):
#         self.workspace = coordData.workspace
#         self.outputSpace = coordData.outputSpace
#         self.file = file_path
#         self.data = coordData.get_data()[file_path]
#         self.imgNum = 0
#
#     def isImported(self):
#         return self.file != ''
#
#     # 1 mm 당 24 pixel -> 610 ppi
#
#     def exportImages(self):
#         file_name = self.file.split("/")[-1].split(".")[0]
#         if not os.path.exists(f"../{self.workspace}/{file_name}"):
#             os.mkdir(f"../{self.workspace}/{file_name}")
#         if not os.path.exists(f"../{self.outputSpace}/{file_name}"):
#             os.mkdir(f"../{self.outputSpace}/{file_name}")
#
#         thread_list = []
#         for page in self.data.keys():
#             t = pdf_convert.PdfConverter(self.file, file_name, page, page, dpi=600, temp_path=self.workspace)
#             thread_list.append(t)
#             t.start()
#             if len(thread_list) == 8:
#                 for thread in thread_list:
#                     thread.join()
#                 thread_list = []
#
#         for t in thread_list:
#             t.join()
#
#         for page in self.data.keys():
#             img_name = f"../{self.workspace}/{file_name}/{str(page)}.jpg"
#             for i, coord in enumerate(self.data[page]):
#                 img = Image.open(img_name)
#                 width, height = img.size
#                 x1, y1 = coord[0][0] / coord[2][0] * width, coord[0][1] / coord[2][1] * height
#                 x2, y2 = coord[1][0] / coord[2][0] * width, coord[1][1] / coord[2][1] * height
#                 cropped = img.crop((x1, y1, x2, y2))
#                 imgPath = f"../{self.outputSpace}/{file_name}/{str(page)}"
#                 if not os.path.exists(imgPath):
#                     os.mkdir(imgPath)
#                 cropped.save(f"{imgPath}/{str(i + 1)}.jpg")
#                 print(f"saved: {imgPath}/{str(i + 1)}.jpg")


class HandoutMaker:
    def __init__(self, templateName):
        self.pageL = PageLayout()
        self.dataH = DataHandler(templateName)

        self.image = Image.new("RGB", (self.pageL.width, self.pageL.height), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

        self.problemsArr = ProblemsArranger()
        self.setProblems()
        self.problemsArr.getStructPages()

        self.img_list = []
        self.image.show()

    def setFont(self, size):
        self.font = ImageFont.truetype("../../Data/Pretendard-Medium.otf", size)
        return self.font

    def setProblems(self):
        data = self.dataH.getData()
        for t in data:
            for f in data[t]:
                for i, page in enumerate(data[t][f]):
                    p = Problem(t, f, page, i)
                    self.problemsArr.appendProblem(p)

    def setHeaderArea(self, start: Coord, templateName):
        text = f"정인수학 프린트: {templateName}"
        textSize = 100
        self.draw.text((start.x, start.y), text, font=self.setFont(textSize), fill=(0, 0, 0))
        return Coord(start.x, start.y + textSize, start.w, start.h - textSize)

    def setTitleArea(self, start: Coord, title):
        text = f"날짜: ____________ 이름: ____________ 점수: ____________"
        margin = 100
        textSize = 120
        self.draw.text((start.x, start.y + margin), text, font=self.setFont(textSize), fill=(0, 0, 0))
        return Coord(start.x, start.y + textSize + margin, start.w, start.h - textSize - margin)

    def setProblemArea(self, start: Coord, problem):
        for i in range(len(self.problemsArr.pages)):
            page = self.problemsArr.getPage(i)
            for b in page.blocks:
                pass


class PageLayout:
    def __init__(self):
        self.dpm = 24
        self.width = 210 * self.dpm
        self.height = 297 * self.dpm
        self.margin = 15 * self.dpm
        self.avWidth = 180 * self.dpm
        self.avHeight = 267 * self.dpm


class ProblemsArranger:
    def __init__(self):
        # Problem : (template, file, page, number)
        self.problemsList = []
        self.pages = set()
        self.pageL = PageLayout()
        self.start = Coord(self.pageL.margin, self.pageL.margin, self.pageL.avWidth, self.pageL.avHeight)

    def getPage(self, pageNum):
        for pg in self.pages:
            if pg.num == pageNum:
                return pg

    def appendProblem(self, problem):
        self.problemsList.append(problem)

    def getStructPages(self):
        page = Page(1, self.start)
        self.arrangeProblems(self.problemsList, Block(page.space), page)

    def arrangeProblems(self, seq: list, block, page):
        if seq[0].col == 2:
            if block.append(seq[0]):
                self.arrangeProblems(seq[1:], block, page)
            elif page.getLeftWithBlock(block) < seq[0].adjHeight + block.gap:
                nextPage = Page(page.num + 1, self.start)
                self.arrangeProblems(seq, Block(nextPage.space), nextPage)
                # 이후 페이지 리스트에 추가
            elif block.col == 1:
                newBlock = Block(page.space)
                self.arrangeProblems(seq, newBlock, page)
            else:
                print("Unexpected Arrangement")
        elif seq[0].col == 1:
            if block.append(seq[0]):
                self.arrangeProblems(seq[1:], block, page)
            elif page.getLeftWithBlock(block) < seq[0].adjHeight + block.gap:
                nextPage = Page(page.num + 1, self.start)
                self.arrangeProblems(seq, Block(nextPage.space), nextPage)
            elif block.col == 2:
                newBlock = Block(page.space)
                self.arrangeProblems(seq, newBlock, page)
        page.addBlock(block)
        self.pages.add(page)


class Page:
    def __init__(self, num, start: Coord):
        self.blocks = set()
        self.num = num
        self.space = start.h
        self.start = start

    def nextPage(self):
        self.num += 1

    def addBlock(self, block):
        self.blocks.add(block)

    def getLeftSpace(self):
        leftSpace = self.space
        for b in self.blocks:
            leftSpace -= b.minHeight
        return leftSpace

    def getLeftWithBlock(self, block):
        return self.getLeftSpace() - block.minHeight


class Problem:
    def __init__(self, template, file, page, number):
        self.template = template
        self.file = file
        self.page = page
        self.number = number
        self.start, self.end = self.getCoord()
        self.col = self.setColumn()
        self.height = self.end.y - self.start.y
        self.width = self.end.x - self.start.x
        self.ratio = self.height / self.width

    def setColumn(self):
        percent = (self.end.x - self.start.x) / self.start.w
        if percent > 0.75:
            self.col = 1
        else:
            self.col = 2
        return self.col

    def getAdjHeight(self, width):
        if self.col == 1:
            return self.ratio * width
        elif self.col == 2:
            # 중간 여백은 10을 기준으로 함
            return self.ratio * (width / 2 - 5)

    def getCoord(self):
        data = self.getProblemCoord()
        self.start = Coord(data[0][0], data[0][1], data[2][0], data[2][1])
        self.end = Coord(data[1][0], data[1][1], data[2][0], data[2][1])
        return self.start, self.end

    def getProblemCoord(self):
        dataH = DataHandler(self.template)
        data = dataH.getCoord(self.template, self.file, self.page)
        return data[self.number]


class Block:
    def __init__(self, maxHeight):
        self.problems = []
        self.minHeight = 0
        self.maxHeight = maxHeight

    def getMinHeight(self):
        return self.minHeight

    def getMaxHeight(self):
        return self.maxHeight

    def append(self, problem):
        if self.minHeight + problem.adjHeight < self.maxHeight:
            self.minHeight += problem.adjHeight
            self.problems.append(problem)
            return True
        else:
            return False


# def main():
#     data = CoordData("Sample Template")
#     for file in data.get_data().keys():
#         f = FileHandler(file, data)
#         if f.isImported():
#             f.exportImages()


# main()
handout = HandoutMaker("Sample Template")
