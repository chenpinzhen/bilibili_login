import cv2 as cv

img = cv.imread('captcha.png', 0)
img1 = cv.imread('captcha1.png', 0)

print(img)
print(img1)
for x in range(len(img)):
    for y in range(80, len(img[0])):
        if img[x][y] != img1[x][y] and abs(int(img[x][y]) - int(img1[x][y])) > 20:
            print(x, y)
            print(img[x][y], img1[x][y], '----')
            return y