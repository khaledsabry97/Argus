def loadFile(videoName):
    videoName =  videoName.split('/')
    videoName = videoName[len(videoName) - 1]
    videoName = 'boxes/' + videoName.split('.')[0] + '.txt'
    print(videoName)
    f = open(videoName, "r")
    lines = f.readlines()
    f.close()
    lines = [x.strip() for x in lines]
    lines.pop(0)

    temp = []
    res = []

    for l in lines:
        if l == '--':
            res.append(temp)
            temp = []
            continue
        x = l.split()
        if x[0] == 'traffic' or x[0] == 'fire' or x[0] == 'stop' or x[0] == 'parking' or x[0] == 'sports' or\
                x[0] == 'baseball' or x[0] == 'tennis' or x[0] == 'wine' or x[0] == 'hot' or x[0] == 'cell' or\
                x[0] == 'teddy' or x[0] == 'hair':
            x[0] = x[0] + x[1]
            x.pop(1)

        temp.append([x[0], float(x[1]), float(x[2]), float(x[3]), float(x[4]), float(x[5])])

    return res

# loadFile('videos/Easy.mp4')