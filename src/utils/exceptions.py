"""Custom image processing exceptions."""


# TODO: Make __init__ accept theta_x, theta_y, theta_z, slice_num as parameters to display those to the user?
# Probably not necessary because those will be displayed in the GUI.
class ComputeCircumferenceOfInvalidSlice(Exception):
    """User attempted to compute circumference of a slice that's just noise.

    We detect this by noticing that the number of contours in the slice > 9.

    Most brain slices have only 2 or 3 detectable contours.
    
    Change the number in imgproc_helpers, then run `pytest` and examine slices given by settings in
    tests/noise_vals.txt. Some valid slices have 6 or 7 contours.
    
    See NIFTI_PATH (0, 0, 0, 151) for a valid slice with 9 contours. 9 seems like a good limit."""

    def __init__(self):
        self.message = f'You attempted to compute the circumference of an invalid brain slice. Contours detected >= ' \
                       f'10, likely just noise.'
        super().__init__(self.message)

class RemoveFromEmptyList(Exception):
    def __init__(self):
        self.message = f'You attempted to remove an image from an empty list of images.'
        super().__init__(self.message)

class RemoveFromListOfLengthOne(Exception):
    def __init__(self):
        self.message = f'You attempted to remove an image from a list of size 1 (i.e., the list would become empty after the delete).'
        super().__init__(self.message)

class RemoveAtInvalidIndex(Exception):
    """This account for the user seeing a 1-indexed list."""
    def __init__(self, index: int):
        self.message = f'You attempted to remove an image at index {index + 1}, which doesn\'t exist in the list of images.'
        super().__init__(self.message)

class RangeTooSmallForAccurateFlooredResult(Exception):
    def __init__(self, old_range, new_range):
        self.message = f'Old range {old_range} or new range {new_range} is too small for a floored result to be accurate.'
        super().__init__(self.message)

class UnexpectedNegativeNum(Exception):
    def __init__(self):
        self.message = f''
        super().__init__(self.message)
