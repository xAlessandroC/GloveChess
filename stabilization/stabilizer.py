from stabilization.buffer import *

buffer = Buffer(2)
count = 0
mean_ppm = np.empty((0,0))
last_result = np.empty((3,4))
last_center = [0,0]


def stabilized_ppm(PPM, center):
    global buffer, count, mean_ppm, last_result, last_center
    threshold = 10

    buffer.push(PPM)

    if len(buffer.getAll()) == 0:
        last_result = PPM
        last_center = center
    else:

        ##CENTER
        # center_diff = np.abs(np.array(center) - np.array(last_center))
        #     print("CENTER_DIFF:", center, last_center,center_diff)
        # if center_diff[0] > threshold  or center_diff[1] > threshold :
        #     last_center = center
        #     last_result = PPM

        ##MEDIA
        ppm_tot = np.zeros((3,4))
        for ppm in buffer.getAll():
            ppm_tot = ppm_tot + ppm

        last_result = ppm_tot / len(buffer.getAll())

        # ppm_1 = buffer.getAll()[0]
        # ppm_2 = buffer.getAll()[1]
        #
        # last_result = np.abs(ppm_1 - ppm_2)
        # count = count + 1
        # if mean_ppm.shape[0] == 0:
        #     mean_ppm = ppm_dif
        # else:
        #     mean_ppm = (mean_ppm + ppm_dif) / count
        #
        # print("MEAN:\n", mean_ppm, count)
        # print("DIFFERENCE:\n", ppm_tot)
    #
    # return PPM
    return last_result

def getLastPPM():
    global last_result

    return last_result
