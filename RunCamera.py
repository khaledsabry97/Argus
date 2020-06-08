from System.CameraNode import CameraNode

video_id = 1529
CameraNode(video_id, 'videos/' + str(video_id) + '.mp4').startStreaming()