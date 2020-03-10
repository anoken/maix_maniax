from lxml import etree
import math
import cv2

def writeXML(imName, faces, H, W, C):
    annotation = etree.Element('annotation')

    folder = etree.SubElement(annotation, 'folder').text='VOC2007'
    filename = etree.SubElement(annotation, 'filename').text=imName+'.jpg'
    source = etree.SubElement(annotation, 'source')

    database = etree.SubElement(source, 'database').text='The FDDB Database'
    annno = etree.SubElement(source, 'annotation').text='FDDB'
    image = etree.SubElement(source, 'image').text='Dummy'
    flickrid = etree.SubElement(source, 'flickrid').text='Dummy'

    owner = etree.SubElement(annotation, 'owner')
    flickrid2 = etree.SubElement(owner, 'flickrid').text='Dummy'
    name = etree.SubElement(owner, 'name').text='Dummy'

    size = etree.SubElement(annotation, 'size')
    width = etree.SubElement(size, 'width').text=str(W)
    height = etree.SubElement(size, 'height').text=str(H)
    depth = etree.SubElement(size, 'depth').text=str(C)

    segmented = etree.SubElement(annotation, 'segmented').text='0'

    for face in faces:
        obj = etree.SubElement(annotation, 'object')
        name2 = etree.SubElement(obj, 'name').text='face'
        pose = etree.SubElement(obj, 'pose').text='Unspecified'
        truncated = etree.SubElement(obj, 'truncated').text='0'
        difficult = etree.SubElement(obj, 'difficult').text='0'

        bndbox = etree.SubElement(obj, 'bndbox')

        xmin = etree.SubElement(bndbox, 'xmin').text=str(face[0])
        ymin = etree.SubElement(bndbox, 'ymin').text=str(face[1])
        xmax = etree.SubElement(bndbox, 'xmax').text=str(face[2])
        ymax = etree.SubElement(bndbox, 'ymax').text=str(face[3])

    tree = etree.ElementTree(annotation)
    tree.write("anno/"+imName+".xml",pretty_print=True)


f = open('./FDDB-fold-10-ellipseList.txt')
while True:
    line = f.readline()
    if not line:
        break

    line = line.strip()
    imName = line.replace('/','_')
    print('processing ' + imName)

    # '2002/08/11/big/img_591'
    im = cv2.imread('./FDDB/'+line+'.jpg')

    H, W, C = im.shape
    faceNum = int(f.readline().strip())
    faces = []

    for faceIdx in range(faceNum):
        line = f.readline().strip()
        splited = line.split()
        r1 = float(splited[0])
        r2 = float(splited[1])
        angle = float(splited[2])
        cx = float(splited[3])
        cy = float(splited[4])


        rectH = 2*r1*(math.cos(math.radians(abs(angle))))
        rectW = 2*r2*(math.cos(math.radians(abs(angle))))

        lx = int(max(0, cx - rectW/2))
        ly = int(max(0, cy - rectH/2))
        rx = int(min(W-1, cx + rectW/2))
        ry = int(min(H-1, cy + rectH/2))

        faceIdx = 0

        faces.append((lx,ly,rx,ry))

    writeXML(imName, faces, H, W, C)
    cv2.imwrite("img/"+imName+".jpg",im)



