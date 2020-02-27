import cv2
import numpy as np
from matplotlib import pyplot as plt

id = 50
number = 2

DB = {
1: np.array([[ 180, 288 ],[ 805, 286 ],[ 29, 904 ],[ 872, 942 ]],dtype = "float32"),
2: np.array([[ 909, 881 ],[ 80, 986 ],[ 106, 380 ],[ 679, 377 ]],dtype = "float32"),
3: np.array([[ 180, 288 ],[ 805, 286 ],[ 29, 904 ],[ 872, 942 ]],dtype = "float32"),
4: np.array([[ 180, 288 ],[ 805, 286 ],[ 29, 904 ],[ 872, 942 ]],dtype = "float32"),
5: np.array([[ 180, 288 ],[ 805, 286 ],[ 29, 904 ],[ 872, 942 ]],dtype = "float32"),
6: np.array([[ 180, 288 ],[ 805, 286 ],[ 29, 904 ],[ 872, 942 ]],dtype = "float32"),
}

image = cv2.cvtColor(cv2.imread("resources/marker/image_"+str(number)+".jpg"), cv2.COLOR_BGR2RGB)
image_gray = cv2.imread("es3/chessboard.jpg", cv2.IMREAD_GRAYSCALE)
stregatto = cv2.cvtColor(cv2.imread("resources/marker/aruco/model_"+str(id)+".png"), cv2.COLOR_BGR2RGB)

stregatto_points = np.array([[0,0],[stregatto.shape[1],0],[0,stregatto.shape[0]],[stregatto.shape[1],stregatto.shape[0]]],dtype = "float32")
print(stregatto_points)
chessboard_points = DB[number]
#chessboard_points = findIntrestingCorner(image_gray)

perspective_transformation = cv2.getPerspectiveTransform(stregatto_points,chessboard_points)
result = cv2.warpPerspective(stregatto, perspective_transformation, (image.shape[1],image.shape[0]))

result[np.mean(result,axis=-1)==0]
white = np.full([stregatto.shape[0],stregatto.shape[1],3],255,dtype=np.uint8)
warp_mask = cv2.warpPerspective(white, perspective_transformation, (image.shape[1], image.shape[0]))
warp_mask = warp_mask==0
result[warp_mask] = image[warp_mask]

plt.figure(figsize=(20,10))
plt.imshow(result)
plt.show()

cv2.imwrite("resources/marker/aruco/image_"+str(number)+"_m"+str(id)+".jpg",cv2.cvtColor(result,cv2.COLOR_RGB2BGR))

###
#IMAGE1: [ 180, 288 ],[ 805, 286 ],[ 29, 904 ],[ 872, 942 ]
#IMAGE2:
#IMAGE3:
#IMAGE4:
#IMAGE5:
#IMAGE6:
