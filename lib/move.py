from PIL import Image, ImageDraw, ImageFont
import numpy
import cv2

def moveLeftToRight(img, img2):
    w, h = img.size
    w2, h2 = img2.size
    if h < h2:
        rh2 = h
    else:
        rh2 = h2
    rw2 = int(w2 * (rh2 / h2))
    img2 = img2.resize((rw2, rh2))
    fps = 24
    speed = 24
    codec = cv2.VideoWriter_fourcc(*"mp4v")
    video  = cv2.VideoWriter('output.mp4', codec, fps, (w, h))

    distance = rw2
    y = h - rh2

    for i in range(speed):
        tmp = img.copy()
        if i == 0:
            x = w
        else:
            x = w - int(distance * (i / (speed - 1)))
            x = int(x * (i / (speed - 1)))
        print(w, h, w2, h2, rw2, rh2, x, y)
        # tmp.paste(img2, (x, h))

        tmp.paste(img2, (x, y))
        tmp.save(".tmp.png", quality=100)
        mat = cv2.imread(".tmp.png")
        video.write(mat)

    for i in range(0, 50, 1):
        tmp = img.copy()
        target = img2.copy()
        # 回転
        rad = numpy.radians(i/10)
        r = numpy.array([
            [numpy.cos(rad), -numpy.sin(rad), i],
            [numpy.sin(rad),  numpy.cos(rad), 0],
            [             0,               0, 1]
        ])
        affine = r
        affine_tuple = tuple(numpy.linalg.inv(affine).flatten())
        target = target.transform(
            img.size,
            Image.AFFINE,
            affine_tuple,
            Image.NEAREST,
            1,
            None
        )

        tmp.paste(img2, (x, y))
        tmp.save(".tmp.png", quality=100)
        mat = cv2.imread(".tmp.png")
        video.write(mat)
    
    for i in range(50, -50, -1):
        tmp = img.copy()
        target = img2.copy()
        # 回転
        rad = numpy.radians(i/10)
        r = numpy.array([
            [numpy.cos(rad), -numpy.sin(rad), i],
            [numpy.sin(rad),  numpy.cos(rad), 0],
            [             0,               0, 1]
        ])
        affine = r
        affine_tuple = tuple(numpy.linalg.inv(affine).flatten())
        target = target.transform(
            img.size,
            Image.AFFINE,
            affine_tuple,
            Image.NEAREST,
            1,
            None
        )

        tmp.paste(img2, (x, y))
        tmp.save(".tmp.png", quality=100)
        mat = cv2.imread(".tmp.png")
        video.write(mat)

    for i in range(-50, 0, 1):
        tmp = img.copy()
        target = img2.copy()
        # 回転
        rad = numpy.radians(i/10)
        r = numpy.array([
            [numpy.cos(rad), -numpy.sin(rad), i],
            [numpy.sin(rad),  numpy.cos(rad), 0],
            [             0,               0, 1]
        ])
        affine = r
        affine_tuple = tuple(numpy.linalg.inv(affine).flatten())
        target = target.transform(
            img.size,
            Image.AFFINE,
            affine_tuple,
            Image.NEAREST,
            1,
            None
        )

        tmp.paste(img2, (x, y))
        tmp.save(".tmp.png", quality=100)
        mat = cv2.imread(".tmp.png")
        video.write(mat)

    video.release()

moveLeftToRight(Image.open('res/screen2.png'), Image.open('res/sample/target.png'))