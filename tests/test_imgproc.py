"""Test stuff in Playground.imgproc.

We use == for float comparison instead of |a-b|<epsilon when the numbers should be *exactly* the same."""

import SimpleITK as sitk
import numpy as np
import cv2
import pytest
import pathlib
from src.utils.imgproc import contour, length_of_contour
import src.utils.exceptions as exceptions
from src.utils.globs import EXAMPLE_IMAGES, EXAMPLE_DATA_DIR, NUM_CONTOURS_IN_INVALID_SLICE

EPSILON: float = 0.001
"""Used for `float` comparisons."""
READER: sitk.ImageFileReader = sitk.ImageFileReader()

@pytest.mark.skip(reason="Doesn't need to run again for a while")
def test_all_images_min_value_0_max_value_less_than_1600():
    for img in EXAMPLE_IMAGES:
        img_np: np.ndarray = sitk.GetArrayFromImage(img.base_img)
        assert img_np.min() == 0 and img_np.max() < 1600


@pytest.mark.skip(reason="Doesn't need to run again")
def test_dimensions_of_np_array_same_as_original_image_but_transposed():
    """Probably not needed but just in case.
    
    The dimensions of the numpy array are the same as the original image.
     
    Additionally, PNG files generated from numpy arrays (no metadata) look the same as slices of the original image (i.e., spacing correct).
    
    Pretty sure that means the arc length generated from the numpy array is the arc length of the original image, with the same units as the original image."""
    for img in EXAMPLE_IMAGES:
        for slice_z in range(img.get_size()[2] // 5):
            slice = img.base_img[:, :, slice_z]
            # Transposed
            np_slice = sitk.GetArrayFromImage(slice)

            assert slice.GetSize()[0] == np_slice.shape[1]
            assert slice.GetSize()[1] == np_slice.shape[0]


@pytest.mark.skip(reason="Doesn't need to run again")
def test_numpy_2D_slice_array_is_transpose_of_sitk_2D_slice_array():
    """Confirm that the numpy matrix representation of a 2D slice is the transpose of the sitk matrix representation of a slice.

    Can ignore this test later."""
    for img in EXAMPLE_IMAGES:
        for z_slice in range(img.get_size()[2] // 5):
            slice_sitk: sitk.Image = img.base_img[:, :, z_slice]
            slice_np: np.ndarray = sitk.GetArrayFromImage(slice_sitk)

            for i in range(slice_np.shape[0]):
                for j in range(slice_np.shape[1]):
                    assert slice_np[i][j] == slice_sitk.GetPixel(j, i)


@pytest.mark.skip(reason="Doesn't need to run for a while")
def test_contour_doesnt_mutate_slice():
    """Test that contour() doesn't mutate its argument."""
    for img in EXAMPLE_IMAGES:
        for slice_z in range(img.get_size()[2] // 3):
            rotated_slice: sitk.Image = img.resample_hardcoded(0, 0, 0, slice_z)
            rotated_slice_copy: sitk.image = img.resample_hardcoded(0, 0, 0, slice_z)
            contour(rotated_slice)
            for i in range(rotated_slice.GetSize()[0]):
                for j in range(rotated_slice.GetSize()[1]):
                    assert rotated_slice.GetPixel(i, j) == rotated_slice_copy.GetPixel(i, j)

@pytest.mark.skip(reason="Doesn't need to run again")
def test_contour_returns_binary_slice():
    """Test that the contour function always returns a binary (0|1) slice."""
    for img in EXAMPLE_IMAGES:
        for slice_z in range(img.get_size()[2] // 5):
            rotated_slice = img.resample_hardcoded(0, 0, 0, slice_z)
            contour_slice_np: np.ndarray = contour(rotated_slice)
            assert contour_slice_np.min() <= 1 and contour_slice_np.max() <= 1


@pytest.mark.skip(reason="Doesn't need to run again")
def test_contour_retranspose_has_same_dimensions_as_original_image():
    for img in EXAMPLE_IMAGES:
        for theta_x in range(0, 30, 15):
            for theta_y in range(0, 30, 15):
                for theta_z in range(0, 30, 15):
                    for slice_z in range(img.get_size()[2] // 3):
                        rotated_slice = img.resample_hardcoded(theta_x, theta_y, theta_z, slice_z)
                        contour_slice: np.ndarray = contour(rotated_slice, True)
                        assert contour_slice.shape[0] == img.get_size()[0] and contour_slice.shape[1] == img.get_size()[1]


@pytest.mark.skip(reason="This should be run again later")
def test_length_of_contour_doesnt_mutate_contour():
    for img in EXAMPLE_IMAGES:
        for slice_z in range(img.get_size()[2] // 10):
            rotated_slice: sitk.Image = img.resample_hardcoded(0, 0, 0, slice_z)
            contour_slice: np.ndarray = contour(rotated_slice)
            contour_slice_copy: np.ndarray = contour_slice.copy()
            length_of_contour(contour_slice, False)
            assert np.array_equal(contour_slice, contour_slice_copy)


@pytest.mark.skip(reason="Doesn't need to run again")
def test_contours_0_is_always_parent_contour_if_no_islands():
    """Assuming there are no islands in the image, then contours[0] results in the parent contour.
    
    See documentation on our wiki page about hierarchy. tl;dr hierarchy[0][i] returns information about the i'th contour.
    hierarchy[0][i][3] is information about the parent contour of the i'th contour. So if hierarchy[0][0][3] = -1, then the 0'th contour is the parent."""
    for img in EXAMPLE_IMAGES:
        for slice_z in range(img.get_size()[2] // 7):
            rotated_slice: sitk.Image = img.resample_hardcoded(0, 0, 0, slice_z)
            # contour removes islands
            contour_slice: np.ndarray = contour(rotated_slice)
            contours, hierarchy = cv2.findContours(contour_slice, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            assert hierarchy[0][0][3] == -1


@pytest.mark.skip(reason="Doesn't need to run again")
def test_arc_length_of_copy_after_transpose_same_as_no_copy_after_transpose():
    """Test arc length of two re-transposed arrays is the same when calling .copy() on one but not the other."""
    for img in EXAMPLE_IMAGES:
        for theta_x in range(0, 30, 15):
            for theta_y in range(0, 30, 15):
                for theta_z in range(0, 30, 15):
                    for slice_z in range(0, img.get_size()[2], img.get_size()[2] // 10):
                        rotated_slice: sitk.Image = img.resample_hardcoded(theta_x, theta_y, theta_z, slice_z)
                        contour_slice_retransposed_not_copied = contour(rotated_slice)
                        # The below duplicates work but it's to be safe
                        contour_slice_retransposed_copied = contour(rotated_slice).copy()

                        # Assumes it's a closed curve but it might not be
                        length_of_not_copied = length_of_contour(contour_slice_retransposed_not_copied, False)
                        length_of_copied = length_of_contour(contour_slice_retransposed_copied, False)
                        assert length_of_not_copied == length_of_copied


@pytest.mark.skip(reason="length_of_contour now re-transposes the result of sitk.GetArrayFromImage by default.")
def test_arc_length_of_transposed_matrix_is_same_except_for_invalid_slice():
    """Per discussion here https://github.com/COMP523TeamD/HeadCircumferenceTool/commit/a230a6b57dc34ec433e311d760cc53841ddd6a49,

    Test that the arc length of a contour and its transpose is the same in a specific case. It probably generalizes to the general case.

    Specifically, for a matrix and its transpose, cv2.findContours will return [ [[x0 y0]] [[x1 y1]] [[x2 y2]] ... ] and [ [[y0 x0]], [[y1 x1]] [[y2 x2]] ... ]

    But cv2.arcLength will apply the distance formula to these contours and that will return the same result.

    However, if pixel spacing is off (non-square pixels), then the distance formula would need a scaling factor for one of the dimensions. Then we'd have to account for this.

    But the pixel spacing of the underlying `np.ndarray` passed into cv2.findContours *seems* to be fine. See discussion in the GH link.
    
    TODO: Unit test with pre-computed circumferences to really confirm this."""
    # Write settings of slices that cause ComputeCircumferenceOfInvalidSlice to a file to make sure they actually are just noise and not brain slices.
    f = open(pathlib.Path('tests') / 'noise_vals.txt', 'w')
    f.write(f'Write settings of slices that cause ComputeCircumferenceOfInvalidSlice (>= {NUM_CONTOURS_IN_INVALID_SLICE} contours detected)\nto this file to make sure they actually are invalid brain slices\n\n')
    f.write('From test_arc_length_of_transposed_matrix_is_same\n\n')

    for img in EXAMPLE_IMAGES:
        f.write(f'{EXAMPLE_DATA_DIR.name}/{img.path.name}\n')
        for theta_x in range(0, 31, 15):
            for theta_y in range(0, 31, 15):
                for theta_z in range(0, 31, 15):
                    for slice_z in range(0, img.get_size()[2]):
                        rotated_slice: sitk.Image = img.resample_hardcoded(theta_x, theta_y, theta_z, slice_z)
                        contour_slice: np.ndarray = contour(rotated_slice, True)
                        # .copy() probably isn't needed if above test passes
                        contour_slice_transposed: np.ndarray = np.transpose(contour_slice)
                        try:
                            length_1 = length_of_contour(contour_slice)
                            length_2 = length_of_contour(contour_slice_transposed)
                            assert length_1 == length_2
                        except exceptions.ComputeCircumferenceOfInvalidSlice:
                            f.write(f'{theta_x, theta_y, theta_z, slice_z}\n')
    f.close()