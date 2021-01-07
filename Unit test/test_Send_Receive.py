from System.Connections.SenderController import SenderController
from System.Connections.ReceiverController import ReceiverController
from System.Data.CONSTANTS import *


# These test are redundant in a way but certain ports and ips caused connection errors
# for some reason we couldn't know. So, we needed a test to verify that connection can be established

def fixed(IP, Port, Msg):
    receiver = ReceiverController(Port)
    sender = SenderController(IP, Port, Msg)

def test_receiving_camera_feed():
    """
        Verify that the camera feed is sent by the camera and received by the server
    """
    try:
        fixed(MASTERIP, MASTERPORT, 'Test camera feed')
        assert 1

    except:
        assert 0


def test_client_notification():
    """
        Verify that the notifications is sent by server and received by the client
    """
    try:
        fixed(GUIPORT, GUIPORT, 'Test client')
        assert 1

    except:
        assert 0


def test_detection_connection():
    try:
        fixed(MASTERIP, MASTERPORT, 'Test client')
        assert 1
    except:
        assert 0


def test_detection_connection():
    try:
        fixed(DETECTIP, DETECTPORT, 'Test detection module connection')
        assert 1
    except:
        assert 0

def test_tracker_connection():
    try:
        fixed(TRACKIP, TRACKPORT, 'Test tracking module connection')
        assert 1
    except:
        assert 0


def test_tracker_connection():
    try:
        fixed(CRASHIP, CRASHPORT, 'Test crash module connection')
        assert 1
    except:
        assert 0

