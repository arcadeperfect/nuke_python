def getErrorFrames(n):

    nodeClass = n.Class()

    if nodeClass not in ['Read']:
        raise TypeError("expect a read node")


    first = n['first'].value()
    last = n['last'].value()

    badFrames = []

    for i in range(first, last):
        nuke.frame(i)
        if n.error():
            print(f"{i} is a bad frame")
            badFrames.append(i)
            
    return(badFrames)

def getGoodFrames(n):

    nodeClass = n.Class()

    if nodeClass not in ['Read']:
        raise TypeError("expect a read node")


    first = n['first'].value()
    last = n['last'].value()

    print(f"first: {first} last: {last}")
    

    goodFrames = []

    for i in range(first, last):
        nuke.frame(i)
        if n.error():
            print(f"{i} is a bad frame")
        else:
            goodFrames.append(i)
            
    return(goodFrames)


def generateFrameHoldNearestGoodFrame(readNode):
    
    try:
        if(readNode.Class() != "Read"):
            raise TypeError("select 1 read node")
    except:
        raise TypeError(f"this expects single read node, receieved a {type(readNode)}")


    first = int(readNode['first'].getValue())
    last = int(readNode['last'].getValue())
    
    frames = nearestGoodFrame(getGoodFrames(readNode), first, last)

    frameHold = nuke.createNode("FrameHold")
    value = frameHold["firstFrame"]
    value.setAnimated()
    for frame in frames:

        value.setValueAt(frame[1], frame[0])



def nearestGoodFrame(frameList, first, last):

    result = []

    for frame in range(first, last):
        closest = min(frameList, key=lambda x: abs(x - frame))
        result.append((frame, closest))

    return result