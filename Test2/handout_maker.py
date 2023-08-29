from PIL import Image, ImageDraw, ImageFont

from Refractor1.classes.coord import Coord
from Refractor1.classes.data_handler import DataFileHandler, DataHandler
import os
from PIL import Image
from PIL.ImageDraw import Draw
from Refractor1.classes.coord import Coord
from Refractor1.classes.data_handler import DataHandler
# Code Structure: Entire print data is stored at HandoutLayout
# Entire page data is stored at PageLayout
# Entire problem data is stored at ProblemLayout
# they recursively exports their data to the image painter
from Refractor1.classes.pdf_converter import PdfConverter


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
        self.pageL = PageLayoutInformation()
        self.dataH = DataHandler(templateName)

        self.font = self.setFont(100)

        self.problemsArr = ProblemsArranger()
        self.setProblems()
        self.problemsArr.getStructPages()

        self.img_list = []

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

    def makeEachPage(self):
        for i in range(len(self.problemsArr.pages)):
            pgNum = i + 1
            image = Image.new("RGB", (self.pageL.width, self.pageL.height), (255, 255, 255))
            draw = ImageDraw.Draw(image)

            startP = Coord(self.pageL.margin, self.pageL.margin, self.pageL.avWidth, self.pageL.avHeight)
            startP = self.setHeaderArea(startP, draw, self.dataH.templateName)
            startP = self.setProblemsArea(startP, draw, self.problemsArr.getPage(pgNum))
            startP = self.setPageNumberArea(startP, draw, pgNum)

            self.img_list.append(image.copy())

    def setHeaderArea(self, start: Coord, draw, templateName):
        text = f"정인수학 프린트: {templateName} - 날짜: ____________ 이름: ____________ 점수: ____________"
        textSize = 100
        draw.text((start.x, start.y - textSize), text, font=self.setFont(textSize), fill=(0, 0, 0))
        return Coord(start.x, start.y, start.w, start.h)

    def setTitleArea(self, start: Coord, draw):
        text = f"날짜: ____________ 이름: ____________ 점수: ____________"
        margin = 100
        textSize = 120
        draw.text((start.x, start.y + margin), text, font=self.setFont(textSize), fill=(0, 0, 0))
        return Coord(start.x, start.y + textSize + margin, start.w, start.h - textSize - margin)

    @staticmethod
    def setProblemsArea(start: Coord, draw, page):
        gap = (page.getLeftSpace()) / (len(page.blocks))
        for block in page.blocks:
            startP = block.setArea(start, draw, gap)
        return Coord(start.x, start.h, start.w, start.h)

    def setPageNumberArea(self, start: Coord, draw, pageNum):
        if start.y != start.h:
            start.y = start.h
        draw.text((start.x, start.y), str(pageNum), font=self.setFont(100), fill=(0, 0, 0))
        return Coord(start.x, start.h, start.w, start.h)


class PageLayoutInformation:
    def __init__(self):
        self.dpm = 24
        self.width = 210 * self.dpm
        self.height = 297 * self.dpm
        self.margin = 15 * self.dpm
        self.avWidth = 180 * self.dpm
        self.avHeight = 267 * self.dpm


class LayoutHandler:
    def __init__(self, startP: Coord):
        # initialize Handout layout
        # and initialize page layout and problem layout conditionally
        self.problemH = self.ProblemHandler()
        self.pageH = self.PageHandler()
        self.handoutL = HandoutLayout()
        self.size = startP

    # add new problem and classify to layouts
    # 1. get problem from param and make problem layout
    # 2. if problem doesn't fit to their layout, make new layout
    # 3. put problem layout in page layout. if false, go next page
    def setNewProblem(self, problem):
        # is TwoProblemsLayout exist? append.
        #   and append to pageLayout
        # if not? make new layout
        #   if problem fit in to two column layout, create and add to temp
        #   if not, create a column layout and append to pageLayout
        # --pageLayout--
        # if returns false when append the layout
        #   get next page and append to it
        problemL = self.problemH.setNewProblem(problem)
        if problemL is not None:
            pageL = self.pageH.setNewProblemLayout(problemL, self.size)
            if pageL is not None:
                self.handoutL.addPageLayout(pageL)

    def setEnd(self):
        problemL = self.problemH.twoProblemsLayout
        if problemL is not None:
            pageL = self.pageH.setNewProblemLayout(problemL, self.size)
            if pageL is not None:
                self.handoutL.addPageLayout(pageL)
            else:
                self.handoutL.addPageLayout(self.pageH.pageL)

    def attachToImage(self):
        pass

    class PageHandler:
        def __init__(self):
            self.pageL = None

        # if pageL is None, set Page Layout and append problemLayout
        # else, try add Problem layout
        #   if succeed, return Nothing or true
        #   failed, return current page Layout and set new page, append.
        def setNewProblemLayout(self, problemL, coord):
            if self.pageL is None:
                self.pageL = PageLayout(coord)
                self.pageL.addProblemLayout(problemL)
            else:
                if self.pageL.addProblemLayout(problemL):
                    return None
                else:
                    past = self.pageL
                    self.pageL = PageLayout(coord)
                    self.pageL.addProblemLayout(problemL)
                    return past

    class ProblemHandler:
        def __init__(self):
            self.twoProblemsLayout = None

        def setNewProblem(self, problem):
            if problem.getRatioBetweenBook() > 0.75:
                return self.setOneColProblem(problem)
            else:
                return self.setTwoColProblem(problem)

        def setTwoColProblem(self, problem):
            if self.twoProblemsLayout is not None:
                self.twoProblemsLayout.appendProblem(problem)
                return self.twoProblemsLayout
            else:
                self.twoProblemsLayout = TwoProblemsLayout()
                self.twoProblemsLayout.appendProblem(problem)

        @staticmethod
        def setOneColProblem(problem):
            pLayout = OneProblemLayout()
            pLayout.appendProblem(problem)
            return pLayout


# Layout means it can get exact coordinates and size of any data
# HandoutLayout stores all PageLayouts
class HandoutLayout:
    # store pages
    def __init__(self):
        self.pageLayouts = []
    # make exact problem layout to append to page layout
    # get each problem and put it in a layout

    # attach layouts to image
    def attachToImage(self, imgDraw: Draw):
        for pl in self.pageLayouts:
            pl.attachToImage(imgDraw)

    # add page layout
    def addPageLayout(self, pgLayout):
        if pgLayout is None:
            raise Exception
        self.pageLayouts.append(pgLayout)


class ProblemLayout:
    def __init__(self):
        self.problemsList = []
        self.size = None

    def getMinHeight(self) -> int:
        pass

    # get exact height applied to page layout
    def getExHeight(self, height):
        return height + self.getMinHeight()

    def appendProblem(self, problem):
        pass

    def attachToImage(self, imgDraw: Draw, startP):
        pass


class PageLayout:
    def __init__(self, startP: Coord):
        self.subLayouts = []
        self.size = startP
        self.gap = 0

    def addProblemLayout(self, layout: ProblemLayout) -> bool:
        totalGap = self.gap * (len(self.subLayouts) + 1)
        if layout.getMinHeight() + totalGap <= self.getRmHeight():
            self.subLayouts.append(layout)
            return True
        return False

    def setGap(self, gap):
        if gap is not None:
            self.gap = gap
            return True
        return False

    def getGap(self):
        return self.gap

    # set layout of entire page
    def getEntirePageLayout(self):
        pass

    # get remain height of page
    def getRmHeight(self):
        minHeight = 0
        for s in self.subLayouts:
            minHeight += s.getMinHeight()
        return self.size.h - minHeight

    def attachToImage(self, imgDraw):
        cur = Coord(self.size.x, self.size.y, self.size.w, self.size.h)
        for p in self.subLayouts:
            p.attachToImage(imgDraw, cur)
            # update current
            HeightAndGap = p.getMinHeight() + self.getGap()
            cur.setHeight(cur.h - HeightAndGap)
            cur.setY(cur.y + HeightAndGap)


class TwoProblemsLayout(ProblemLayout):
    def __init__(self):
        super().__init__()

    def getMinHeight(self):
        minHeight = 0
        for p in self.problemsList:
            minHeight = max(minHeight, p.minHeight)
        return minHeight

    # def setExHeight(self, height):

    def appendProblem(self, problem):
        if len(self.problemsList) >= 2:
            raise Exception
        self.problemsList.append(problem)

    def attachToImage(self, imgDraw, startP):
        if len(self.problemsList) != 2:
            raise Exception
        coord = Coord(startP.x, startP.y, startP.w / 2, startP.h)
        self.problemsList[0].attachToImage(imgDraw, coord)
        coord = Coord(startP.x + startP.w / 2, startP.y, startP.w / 2, startP.h)
        self.problemsList[1].attachToImage(imgDraw, coord)


class OneProblemLayout(ProblemLayout):
    def __init__(self):
        super().__init__()

    def getMinHeight(self):
        if len(self.problemsList) != 1:
            raise Exception
        minHeight = self.problemsList[0].minHeight
        return minHeight

    def appendProblem(self, problem):
        if len(self.problemsList) != 0:
            raise Exception
        self.problemsList.append(problem)

    def attachToImage(self, imgDraw, startP):
        if len(self.problemsList) != 1:
            raise Exception
        self.problemsList[0].attachToImage(imgDraw, startP)


# problem dataset has conversion from information of data
class Problem:
    def __init__(self, template, file, page, number):
        self.template = template
        self.file = file
        self.page = page
        self.number = number
        self.start, self.end = self.getPoint()

    def getImagePath(self):
        imgPath = f"../Exports/Temp_Problems/{self.file}/{self.page}/{self.number}.jpg"
        if not os.path.exists(imgPath):
            raise Exception
        return imgPath

    # make image and get path stored at temp
    # def getImagePath(self) -> str:
    #     data = self.getOriginalProblemData()
    #     # check if image is not created
    #     # create image by data
    #     # return its path
    #     pass

    # load image
    def getImage(self) -> Image:
        # check if image is not created
        # return loaded image
        if not self.checkImageCreated():
            self.createImage()
        return Image.open(self.getImagePath())

    def resizeImage(self, image: Image, width) -> Image:
        image.resize(self.getSize(width))
        return image

    def checkImageCreated(self) -> bool:
        if os.path.exists(self.getImagePath()):
            return True
        return False

    def createImage(self):
        pc = PdfConverter()
        pc.setFilePath(self.file)
        imgDir = f"../../Exports/Temp_Problems/{self.file}/{self.page}"
        info = (imgDir, self.number, "jpg", "JPEG", 600)
        pc.initConvert(info)
        pc.startConvert()

    # get ratio of problem and book page
    def getRatioBetweenBook(self):
        data = self.getOriginalProblemData()
        width = data[0][0] - data[1][0]
        bookWidth = data[2][0]
        return width / bookWidth

    def getSize(self, width=None, height=None):
        ratio = (self.end.y - self.start.y) / (self.end.x - self.start.x)
        if width is not None:
            return width, width * ratio
        elif height is not None:
            return height / ratio, height

    def getPoint(self):
        data = self.getOriginalProblemData()
        self.start = Coord(data[0][0], data[0][1], data[2][0], data[2][1])
        self.end = Coord(data[1][0], data[1][1], data[2][0], data[2][1])
        return self.start, self.end

    def getOriginalProblemData(self):
        dataH = DataHandler(self.template)
        data = dataH.getCoord(self.template, self.file, self.page)
        return data[self.number]

    def attachToImage(self, imgDraw: Draw, startP):
        # convert image and get path
        # load image from path and resize
        # attach problem image to [image] correctly
        pImg = self.getImage()
        pImg = self.resizeImage(pImg, startP)
        imgDraw.paste(pImg, (startP.x, startP.y))

