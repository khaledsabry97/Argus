from Joiner.joiner import convert_frames_to_video
import os
from os.path import isfile, join

"""
    Unit test for joiner, a method to collect frames into a video.
"""


def test_joiner_invalid_path():
    """
        Verify that method can handle invalid paths
    """
    pathIn = 'dont\exist'
    pathOut = 'Unit test\output'

    assert convert_frames_to_video(pathIn, pathOut, 30) == None



def test_joiner_valid_path():
    """
        Verify the method works as expected
    """

    try:
        pathIn = 'input'
        pathOut = 'output'
        convert_frames_to_video(pathIn, pathOut, 30)

        assert 1

    except:

        assert 0
