#!/usr/bin/python3

import os
import numpy as np
np.set_printoptions(threshold=np.nan, linewidth=250)
import multiprocessing as mp
import time

def get_image_array(phi, theta, omega=2*np.pi, sidelength=200):
    ll, rr, cc = np.indices([sidelength, sidelength, sidelength], dtype=np.int)
    a_x = cc
    a_y = rr
    a_z = ll

    cosphi, sinphi = np.cos(phi), np.sin(phi)
    costheta, sintheta = np.cos(theta), np.sin(theta)

    a_r = (a_x * cosphi + a_y * sinphi) * sintheta + a_z * costheta

    return np.sin(a_r)


def get_convolution(a_img, c_thread, c_conv, return_dict):
    a_fft = a_img.copy()
    for i in range(len(a_img.shape)):
        a_fft = np.fft.fft(a_fft, axis=i)
    a_fft = np.fft.fftshift(a_fft)
    return_dict[(c_thread, c_conv)] = a_fft


def convolutions(sidelength=100, n_threads=1, n_convolutions=1):
    a_img = get_image_array(phi=5. * np.pi / 180., theta=45. * np.pi / 180., sidelength=sidelength)

    list_proc = []
    return_dict = mp.Manager().dict()
    for c_thread in range(n_threads):
        for c_conv in range(n_convolutions):
            proc = mp.Process(target=get_convolution, args=(a_img, c_thread, c_conv, return_dict))
            list_proc.append(proc)
            proc.start()

    for proc in list_proc:
        proc.join()

    list_writeMBps = []
    list_readMBps = []
    for key in sorted(return_dict.keys()):
        a_fft = return_dict[key]
        print(key, a_fft.dtype, a_fft.shape)

        filepath_out = 'a_fft_%d_%d.dat' % (key[0], key[1])

        now = time.time()
        a_fft.tofile(filepath_out)
        elapsed = time.time() - now
        try:
            writeMBps = int(np.round((a_fft.size * 128 / (1024 * 1024 * 8)) / elapsed))
        except Exception:
            writeMBps = 0
        list_writeMBps.append(writeMBps)
        print('write: %dMB/s' % writeMBps)

        now = time.time()
        a_fft = np.fromfile(filepath_out, dtype=np.complex)
        elapsed = time.time() - now
        try:
            readMBps = int(np.round((a_fft.size * 128 / (1024 * 1024 * 8)) / elapsed))
        except Exception:
            readMBps = 0
        list_readMBps.append(readMBps)
        print('read: %dMB/s' % readMBps)

        print()

        try:
            os.remove(filepath_out)
        except OSError:
            pass

    return np.array(list_writeMBps), np.array(list_readMBps)


def main():
    a_writeMBps, a_readMBps = convolutions(sidelength=150, n_threads=2, n_convolutions=10)

    print('max_write: %.1fMB/s' % a_writeMBps.max())
    print('avg_write: %.1fMB/s' % a_writeMBps.mean())
    print('std_write: %.1fMB/s' % a_writeMBps.std())
    print('max_read: %.1fMB/s' % a_readMBps.max())
    print('avg_read: %.1fMB/s' % a_readMBps.mean())
    print('std_read: %.1fMB/s' % a_readMBps.std())


if __name__ == '__main__':
    main()
