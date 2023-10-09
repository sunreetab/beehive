import os
import subprocess
import sys

import numpy as np
from PIL import Image

import inklimit


INKLIMIT_PROGRAM = 'inklimit.py'
OUTPUT_DIR = 'testout'


def check_output_dir(out_dirname):
    if os.path.isdir(out_dirname):
        return

    print(f'Creating output directory {out_dirname}')
    os.makedirs(out_dirname)


def make_command_list(input_filename, output_filename, limit, method):
    return [sys.executable, INKLIMIT_PROGRAM, input_filename, output_filename,
            str(limit), str(method)]


def make_pixel(c, m, y, k):
    assert 0 <= c <= 255, f'c must be in range [0, 255]; got {c}'
    assert 0 <= m <= 255, f'm must be in range [0, 255]; got {m}'
    assert 0 <= y <= 255, f'y must be in range [0, 255]; got {y}'
    assert 0 <= k <= 255, f'k must be in range [0, 255]; got {k}'
    return np.array([c, m, y, k], dtype=np.uint8)


def make_image(x: int, y: int, pixel: np.ndarray) -> np.ndarray:
    assert x > 0 and y > 0
    assert len(pixel.shape) == 1 and pixel.shape[0] == 4
    return np.broadcast_to(pixel, (x, y, pixel.shape[0])).copy()


def compare_images(source_file, target_file, limit, listErrors=False):
    assert os.path.isfile(source_file), \
        f"Source file {source_file} doesn't exist"
    assert os.path.isfile(target_file), \
        f"Target file {target_file} doesn't exist"

    with Image.open(source_file) as im_src:
        with Image.open(target_file) as im_tgt:
            assert im_src.size == im_tgt.size

            arr = np.asarray(im_tgt)
            arr = arr.astype(float)
            arr = arr * 100.0 / 255.0
            arr = arr.astype(int)

            sums = np.sum(arr, axis=-1)
            overlimit = np.count_nonzero(sums > limit)
            if listErrors and overlimit > 0:
                for i in range(sums.shape[0]):
                    for j in range(sums.shape[1]):
                        if sums[i, j] > limit:
                            print(f'sums[{i}, {j}] = {sums[i, j]}')

    assert overlimit == 0, \
        f'Found {overlimit} pixels over specified limit of {limit}%'

def almost_equal(a, b) -> bool:
    return abs(a - b) < 0.000001

def do_ink_limit_test(limit, to_test):
    input_image = make_image(2, 2, make_pixel(255, 255, 255, 255))
    input_image[0, 0, :] = make_pixel(10, 10, 10, 10)   # under ink limit
    input_image[0, 1, :] = make_pixel(0, 255, 255, 255) # case where UCR fails
    output_image = to_test(input_image, limit)
    max_pixel = np.max(np.sum(output_image, axis=-1))
    assert max_pixel <= int(limit * 255. / 100.), \
        f"Failed to limit {input_image} to {limit}; got a max of {max_pixel}"

def test_unit_inklimit_proportional():
    do_ink_limit_test(240., inklimit.ink_limit_proportional)

# def test_unit_inklimit_ucr():
#     do_ink_limit_test(240., inklimit.ink_limit_ucr)

def test_e2e_convert_testimage():
    check_output_dir(OUTPUT_DIR)
    out_filename = os.path.join(OUTPUT_DIR, 'testout.tiff')
    subprocess.run(make_command_list('balloons.tiff', out_filename, 240, 0))

    compare_images('balloons.tiff', out_filename, 240)

def test_e2e_invalid_arg_help():
    check_output_dir(OUTPUT_DIR)
    out_filename = os.path.join(OUTPUT_DIR, 'testout.tiff')
    result = subprocess.run(
        make_command_list('balloons.tiff', out_filename, 240, 1000),
        capture_output=True,
        text=True)
    assert result.returncode == 1
    assert result.stdout == inklimit.help_text + "\n"


if __name__ == "__main__":
    test_unit_inklimit_proportional()
    # def test_unit_inklimit_ucr():
    # test_e2e_convert_testimage()
    # test_e2e_invalid_arg_help()
