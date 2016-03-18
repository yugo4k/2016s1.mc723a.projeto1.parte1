#!/usr/bin/python3

import numpy as np
np.set_printoptions(threshold=np.nan, linewidth=250)
import matplotlib.pyplot as plt
import multiprocessing as mp
import time

# import line_profiler as lp

# def do_profile(follow=[]):
#     def inner(func):
#         def profiled_func(*args, **kwargs):
#             try:
#                 profiler = lp.LineProfiler()
#                 profiler.add_function(func)
#                 for f in follow:
#                     profiler.add_function(f)
#                 profiler.enable_by_count()
#                 return func(*args, **kwargs)
#             finally:
#                 profiler.print_stats()
#         return profiled_func
#     return inner


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


# @do_profile(follow=[get_convolution])
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

        now = time.time()
        a_fft.tofile('/tmp/a_fft_%d_%d.dat' % (key[0], key[1]))
        elapsed = time.time() - now
        writeMBps = int(np.round((a_fft.size * 128 / (1024 * 1024 * 8)) / elapsed))
        list_writeMBps.append(writeMBps)
        print('write: %dMB/s' % writeMBps)

        now = time.time()
        a_fft = np.fromfile('/tmp/a_fft_%d_%d.dat' % (key[0], key[1]), dtype=np.complex)
        elapsed = time.time() - now
        readMBps = int(np.round((a_fft.size * 128 / (1024 * 1024 * 8)) / elapsed))
        list_readMBps.append(readMBps)
        print('read: %dMB/s' % readMBps)

        print()

    return np.array(list_writeMBps), np.array(list_readMBps)

    # if 0 < n_convolutions:
    #     a_img = np.absolute(a_img)

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


# import cProfile as cp

def main():
    # prof = cp.Profile()
    # try:
    #     prof.enable()
    #     convolutions(sidelength=250, n_threads=4, n_convolutions=1)
    #     prof.disable()
    # finally:
    #     prof.print_stats()

    # prof = lp.LineProfiler()
    a_writeMBps, a_readMBps = convolutions(sidelength=150, n_threads=2, n_convolutions=5)

    print('max_write:', a_writeMBps.max())
    print('avg_write:', a_writeMBps.mean())
    print('std_write:', a_writeMBps.std())
    print('max_read:', a_readMBps.max())
    print('avg_read:', a_readMBps.mean())
    print('std_read:', a_readMBps.std())


if __name__ == '__main__':
    main()
