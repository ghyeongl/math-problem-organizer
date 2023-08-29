import cv2


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(x) + ', ' + str(y)
        cv2.putText(img, strXY, (x, y), font, 0.5, (255, 0, 0), 2)
        cv2.imshow('image', img)


events = [i for i in dir(cv2) if 'EVENT' in i]
print(events)

click = False
x1, y1 = -1, -1


def draw_rectangle(event, x, y, flags, param):
    global x1, y1, click

    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
        print("사각형의 왼쪽위 설정 : (" + str(x1) + ", " + str(y1) + ")")
        cv2.imshow('image', img)

    # elif event == cv2.EVENT_MOUSEMOVE:
    #     if click:
    #         cv2.rectangle(img, (x1, y1), (x, y), (255, 0, 0), -1)
    #         print("(" + str(x1) + ", " + str(y1) + "), (" + str(x) + ", " + str(y) + ")")

    elif event == cv2.EVENT_LBUTTONUP:
        cv2.rectangle(img, (x1, y1), (x, y), (255, 0, 0), 3)
        cv2.imshow('image', img)


img = cv2.imread('../Exports/test84.tiff', 1)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rectangle)


cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
