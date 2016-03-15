#!/usr/bin/python3

import sys
import numpy as np
np.set_printoptions(threshold=np.nan, linewidth=250)
import matplotlib.pyplot as plt

def get_image_array(phi, theta, omega=2*np.pi, sidelength=200):
    ll, rr, cc = np.indices([sidelength, sidelength, sidelength], dtype=np.int)
    a_x = cc# - sidelength // 2
    a_y = rr# - sidelength // 2
    a_z = ll# - sidelength // 2

    cosphi, sinphi = np.cos(phi), np.sin(phi)
    costheta, sintheta = np.cos(theta), np.sin(theta)

    a_r = (a_x * cosphi + a_y * sinphi) * sintheta + a_z * costheta

    return np.sin(a_r)


def get_convolution(a_img):
    a_fft = a_img.copy()
    for i in range(len(a_img.shape)):
        a_fft = np.fft.fft(a_fft, axis=i)
    a_fft = np.fft.fftshift(a_fft)
    return a_fft


def main():
    sidelength = int(sys.argv[1])
    n_convolutions = int(sys.argv[2])

    a_img = get_image_array(phi=5. * np.pi / 180., theta=45. * np.pi / 180., sidelength=sidelength)

    for i in range(n_convolutions):
        a_img = get_convolution(a_img)

    if 0 < n_convolutions:
        a_img = np.absolute(a_img)

    # fig = plt.figure(facecolor='white', figsize=(16, 9), dpi=50)

    # ax = fig.add_subplot(2, 2, 1)
    # ax.set_title('z=0')
    # ax.set_ylabel('y')
    # ax.set_xlabel('x')
    # im = ax.imshow(a_img[0, :, :])
    # cb = plt.colorbar(im)

    # ax = fig.add_subplot(2, 2, 2)
    # ax.set_title('y=0')
    # ax.set_ylabel('z')
    # ax.set_xlabel('x')
    # im = ax.imshow(a_img[:, 0, :])
    # cb = plt.colorbar(im)

    # ax = fig.add_subplot(2, 2, 3)
    # ax.set_title('x=0')
    # ax.set_ylabel('z')
    # ax.set_xlabel('y')
    # im = ax.imshow(a_img[:, :, 0])
    # cb = plt.colorbar(im)

    # plt.show()


if __name__ == '__main__':
    main()
