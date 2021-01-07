from boxes.yoloFiles import loadFile

"""
    Unit test for yoloFiles.
    args: file path
    return: list of lists
"""

def test_loadFiles_wrong_path():
    """
        Make sure the method can handle invalid paths
    """
    assert loadFile('videos/noneExistingVideo.mp4') == None

def test_loadFiles_read():
    """
        Verify that the behaviour of the function is as expected
    """

    ret = [['truck', 50.268692, 123.1192, 92.78042, 167.10449, 0.67817026],
            ['car', 229.48555, 240.26302, 30.206844, 38.74132, 0.31249338],
            ['car', 180.17868, 204.20567, 51.409515, 73.122986, 0.86208504],
            ['car', 188.7847, 208.52684, 71.53062, 94.43666, 0.9535593]]

    res = loadFile('videos/1501.mp4')
    assert res[0] == ret

def test_loadFiles_types():
    """
        Verify the types returned by the function
    """

    res = loadFile('videos/1500.mp4')[0][0]
    flag = (type(res[0]) == str and type(res[1]) == float and type(res[2]) == float
           and type(res[3]) == float and type(res[4]) == float and type(res[5]) == float)
    assert flag
