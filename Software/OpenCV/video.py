import cv2
import numpy as np
import time
import pickle
import cvzone


def stackImages(scale, imgArray):  # 一个拼接图像的函数
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height,x:x + width]
        #cv2.imshow("Stack", imgCrop)

        # 绘制轮廓
        contours, hierarchy = cv2.findContours(imgCrop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)  # 计算轮廓面积
            print(area)
            cv2.drawContours(imgContour[y:y + height,x:x + width], cnt, -1, (0, 0, 255), 3)
            #cv2.imshow("Stack", imgContour[y:y + height,x:x + width])

            if area > 200:
                peri = cv2.arcLength(cnt, True)  # 轮廓周长
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)  # 多边形逼近
                objCor = len(approx)
                x1, y1, w, h = cv2.boundingRect(approx)  # 找一个大框，框住图形

                cv2.rectangle(imgContour, (x+x1, y+y1), (x+x1 + w, y+y1 + h), (255, 255, 0), 6)  # 矩形框框住所识别物体

                if objCor > 4:
                    objectType = "Red/Blue"
                    cv2.putText(imgContour, objectType,
                                (320,40), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (0, 0, 0), 2)

                if w/h >0.9 and w/h < 1.2 :
                    # 在图像旁标注出颜色
                    cv2.putText(imgContour, f"{'Yellow'}",
                                (300, 40), cv2.FONT_HERSHEY_COMPLEX, 1.2,
                                (0, 255, 255), 2)

            #在图像旁标注出名称
            cv2.putText(imgContour,f"{'bullet color'}",
                        (50,40),cv2.FONT_HERSHEY_COMPLEX,1.2,
                        (0,0,0),2)





with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 370, 170


pTime = 0
cap = cv2.VideoCapture("C:/Users/DELL/Desktop/p/PlantsVsZombies.mp4")

while True:
    success, img = cap.read()
    #img = cv2.resize(img, (1048, 455))
    imgContour = img.copy()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    # 自适应阈值  同一幅图像上的不同部分的具有不同亮度时
    """
    参数：
    满足条件的像素点需要设置的灰度值------>255
    算法计算邻域时的领邻域大小，一般选择为3、5、7......等------>25
    每个邻域计算出阈值后再减去C作为最终阈值-------->16
    """
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)

    # 中值滤波 消除一些噪音点
    imgMedian = cv2.medianBlur(imgThreshold, 7)
    kernel = np.ones((5, 5), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    imgerison = cv2.erode(imgDilate, kernel, iterations=1)

    imgBlank = np.zeros_like(img)  # 一张纯黑的图片

    # getContours(imgDilate)
    checkParkingSpace(imgDilate)

    #帧率显示
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(imgContour, f'FPS: {int(fps)}', (30, 100), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 255, 0), 3)

    cv2.imshow("Stack", imgContour)
    if cv2.waitKey(1) & 0xFF == ord(' '):
         break


#关闭摄像头
cap.release()
# 关闭图像窗口
cv2.destroyAllWindows