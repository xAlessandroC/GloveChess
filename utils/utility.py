import numpy as np


def compositeArray(rvec, tvec):
    v = np.c_[rvec, tvec.T]
    v_ = np.r_[v, np.array([[0,0,0,1]])]
    return v_
