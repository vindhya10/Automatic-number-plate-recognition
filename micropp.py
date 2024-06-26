import cv2
import imutils
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

testimage = input("Enter name of jpg file : ")

image = cv2.imread(testimage)
image = imutils.resize(image , width = 500)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)

edged = cv2.Canny(gray_image, 30, 200)

cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1=image.copy()
cv2.drawContours(image1,cnts,-1,(0,255,0),3)

cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
screenCnt = None
image2 = image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)

i=7
for c in cnts:
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
    if len(approx) == 4: 
        screenCnt = approx
        x,y,w,h = cv2.boundingRect(c) 
        new_img=image[y:y+h,x:x+w]
        cv2.imwrite('./'+str(i)+'.png',new_img)
        i+=1
        break

cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
Cropped_loc = './7.png'
plate = pytesseract.image_to_string(Cropped_loc, lang='eng')
print("Number plate is:", plate)

