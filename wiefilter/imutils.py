"""
Basic image utility functions

Simple info on Wiener Filters


Let's see the function in use. We are going to use numpy implementation of dft
to implement a filter called wiener filter.

Now we ask ourselves what is an image ?

An image from the point of view of frequencies is simply a random distribution
of a range of values. An image of something, some object, on the other hand, is
still a distribution of range of values but this time, we observe some form of
regularity with respect to certain frequencies.

We know from Fourier Transform that if have a frequency range that is regular
we can find the values corresponding to this range. The set of magnitude of the
signal for a given frequency range is known as the power spectrum of the signal
for given frequencies, and it is calculated as the following:

    $PS (f(x,y)) = |f'(x, y)|^2$

Let's see how we can apply this to images in order to obtain images with less
noise.

A noisy image is: $out(x,y) = in(x,y) + noise(x,y)$.

Meaning that it is the result of an original image plus some form of noise.

We observe the $out$ image, and we want to recover $in$ image.

As mentioned above, the fourier transform supports superposition:

From these information we can compute an optimum filter that would denoise our
image. This optimum filter is called Weiner filter.  For actual steps of this
computation required to derive this filter see, Szeliski 2011, p. 124.
"""

from PIL import Image
import numpy as np

from typing import List, Dict, Tuple, Optional, Union


def psf_from_image(img: np.ndarray):
    "obtain psf from image"
    # rfft2 => real valued fourier transform
    return np.abs(np.fft.rfft2(img.copy())) ** 2


def weiner(
    out_fft: np.ndarray, p_n: np.ndarray, p_s: Union[np.ndarray, List[np.ndarray]]
):
    """
    apply weiner filter using a single or multiple similar p_s values
    """
    if isinstance(p_s, np.ndarray):
        channel_coeff = 1 / (1 + (p_n / p_s))
        return out_fft * channel_coeff
    if isinstance(p_s, (list, tuple)):
        coeffs = [1 / (1 + (p_n / ps)) for ps in p_s]
        out = out_fft.copy()
        for coeff in coeffs:
            out *= coeff
        return out


def resize(
    original_size: Tuple[int, int], similars: Union[List[Image], Image]
) -> Union[List[Image], Image]:
    """
    resize similar images to original size
    """
    if not isinstance(original_size, tuple):
        raise TypeError("original size must be a tuple")
    if len(original_size) != 2:
        raise ValueError("original size must contain only a width and height value")

    def conditioned_resize(simage: Image):
        if simage.size == original_size:
            return simage
        else:
            return simage.resize(original_size)

    if isinstance(similars, Image):
        return conditioned_resize(similars)
    if isinstance(similars, (tuple, list)):
        return [conditioned_resize(similar) for similar in similars]
    else:
        raise TypeError("similar images must be a list of images or a single image")


def single_weiner_denoising(
    original_image: Image, similar_image: Image, original_fft=None, similar_noise=None
):
    """
    Weiner denoising with a single similar image
    """
    if not isinstance(similar_image, Image):
        raise TypeError("similar image must be of Image type")

    # resize images
    similar_image = resize(original_size=original_image.size, similars=similar_image)

    # transform into array
    original_arr = np.array(original_image)
    similar_arr = np.array(similar_image)

    # get noise
    if similar_noise is None:
        similar_noise = np.random.uniform(0, 255, original_arr.shape)

    # obtain psfs
    sim_img_psf = psf_from_image(similar_arr)
    psf_noise = psf_from_image(similar_noise)

    # compute ffts
    if original_fft is None:
        original_fft = np.fft.rfft2(original_arr.copy())
    weiner_out = weiner(out_fft=original_fft, p_s=sim_img_psf, p_n=psf_noise)

    # return the real part as result
    return np.fft.irfft2(weiner_out)


def multiple_weiner_denoising(
    original_image: Image,
    similar_images: List[Image],
    original_fft=None,
    similar_noise=None,
):
    """
    Weiner denoising with a multiple similar images
    """
    if not isinstance(similar_images, Image):
        raise TypeError("similar image must be of Image type")

    # resize images
    similar_images = resize(original_size=original_image.size, similars=similar_images)

    # transform into array
    original_arr = np.array(original_image)
    similar_arrs = [np.array(similar_image) for similar_image in similar_images]

    # get noise
    if similar_noise is None:
        similar_noise = np.random.uniform(0, 255, original_arr.shape)

    # obtain psfs
    sim_img_psfs = [psf_from_image(similar_arr) for similar_arr in similar_arrs]
    psf_noise = psf_from_image(similar_noise)

    # compute ffts
    if original_fft is None:
        original_fft = np.fft.rfft2(original_arr.copy())
    weiner_out = weiner(out_fft=original_fft, p_s=sim_img_psfs, p_n=psf_noise)

    # return the real part as result
    return np.fft.irfft2(weiner_out)
