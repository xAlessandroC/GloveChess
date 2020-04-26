import numpy as np

last_rvec = []
last_tvec = []

def getCorrectVectors(rvec, tvec):
    global last_rvec, last_tvec

    if len(rvec) == 0 and len(tvec) == 0:
        return (last_rvec, last_tvec)

    elif isSimilar(np.array([rvec,tvec]), np.array([last_rvec, last_tvec])):
        return (last_rvec, last_tvec)

    else:
        last_rvec = rvec
        last_tvec = tvec
        return (rvec, tvec)


def isSimilar(vec, old_vec):
    similar_cnt = 0
    dissimilar_cnt = 0
    threshold = 0.05

    if len(old_vec[0]) == 0 and len(old_vec[1]) == 0:
        return False

    result = np.absolute(np.subtract(vec, old_vec))
    print("VEC RISULTANTE: ", result, result.shape)

    for k in range(len(result)):
        for i in range(len(result[k])):
            for j in range(len(result[k][i])):
                if result[k][i][j] < threshold:
                    similar_cnt += 1
                else:
                    dissimilar_cnt +=1

    if similar_cnt >= dissimilar_cnt:
        return True
    else:
        return False
