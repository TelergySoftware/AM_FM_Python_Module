from scipy.fftpack import fft
import numpy as np


def calc_fft(array: np.ndarray, size: int, fs: float) -> (np.ndarray, np.ndarray):
    """
    Calculates the Fast Fourier Transform and the new x axis values
    :param array: np.ndarray
    :param size: int
    :param fs: float
    :return: tuple with the format (np.ndarray, np.ndarray)
    """
    yf = fft(array.reshape(size))
    k = np.arange(size)
    t = size / fs
    frq = k / t

    return frq, yf
