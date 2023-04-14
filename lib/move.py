from PIL import Image, ImageDraw, ImageFont
import numpy
import cv2
import os

class ExImage:    
    def pilTocv2(pil_image):
        pil_image.save('.tmp.png', quality = 100)
        return cv2.imread('.tmp.png')

    def cv2ToPil(cv2_image):
        cv2.imwrite('.tmp.png', cv2_image)
        return Image.open('.tmp.png')

def moveLeftToRightWithVideo(video_path, img2, output):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return
    
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    print('digit: {}'.format(digit))

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = (int(width), int(height))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print('fps: {}'.format(fps))
    print('size: {}'.format(size))

    codec = cv2.VideoWriter_fourcc(*"mp4v")
    video  = cv2.VideoWriter(output, codec, fps, size)

    # 変換設定
    speed = 24
    affines, img2 = leftToRight_FuwaFuwa(size, img2, speed)

    print("motion count: {}".format(len(affines)))

    for a in affines:
        ret, frame = cap.read()
        if ret:
            frame = ExImage.cv2ToPil(frame)
            affine = a
            affine_tuple = tuple(numpy.linalg.inv(affine).flatten())
            target = img2.copy().transform(
                size,
                Image.AFFINE,
                affine_tuple,
                Image.NEAREST,
                1,
                None
            )
            print(a)
            two_padded = Image.new('RGBA', size, (255, 255, 255, 0))
            two_padded.paste(target, (0, 0))
            frame.putalpha(alpha=255)
            tmp2 = Image.alpha_composite(frame, two_padded)
            mat = ExImage.pilTocv2(tmp2)
            video.write(mat)
        else:
            return

    # while True:
    #     ret, frame = cap.read()
    #     if ret:
    #         cv2.imwrite('{}.{}'.format(str(n).zfill(digit), ext), frame)
    #         n += 1
    #     else:
    #         return

def leftToRight_FuwaFuwa(size, img2, speed, fuwaloop = 2):
    affines = []

    w, h = size
    w2, h2 = img2.size
    if h < h2:
        rh2 = int(h / 2)
    else:
        rh2 = int(h2 / 2)
    rw2 = int(w2 * (rh2 / h2))
    img2 = img2.copy().resize((rw2, rh2))

    distance = rw2
    y = h - rh2 - 10

    # 入場
    for i in range(speed):
        if i == 0:
            x = w
        else:
            x = w - int(rw2 * (i / (speed - 1)))
        
        affines.append((
            [1, 0, x],
            [0, 1, y],
            [0, 0, 1]
        ))

    print("x : ", x)

    # ふわふわ
    count = 400
    for i in range(0, count, 1):
        # 回転
        if (i < count / 2):
            radz = numpy.radians(10 * i / count)
        else:
            radz = numpy.radians(10 * (count - i) / count)
        d = numpy.sqrt(rh2**2 + rw2**2)
        f = d / (2 * numpy.sin(radz) if numpy.sin(radz) != 0 else 1)
        rz = numpy.array([
            [numpy.cos(radz), -numpy.sin(radz), 0, 0],
            [numpy.sin(radz),  numpy.cos(radz), 0, 0],
            [              0,                0, 1, 0],
            [              0,                0, 0, 1]
        ])
        rady = numpy.radians(360 * i / 200)
        ry = numpy.array([
            [numpy.cos(rady), 0, - numpy.sin(rady), 0],
            [              0, 1,                 0, 0],
            [numpy.sin(rady), 0,   numpy.cos(rady), 0],
            [              0, 0,                 0, 1]
        ])
        r = numpy.dot(ry, rz)
        t = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, f],
            [0, 0, 0, 1]
        ])
        a1 = numpy.array([ 
            [1, 0,  1],                
            [0, 1,  1],
            [0, 0,  1],
            [0, 0,  1]
        ])
        a2 = numpy.array([
            [1, 0, x - numpy.cos(rady) * rw2 / 2 + rw2 / 2, 0],
            [0, 1, y, 0],
            [0, 0, 1, 0]
        ])
                
        s = numpy.dot(a2, numpy.dot(t, numpy.dot(r, a1)))
        affines.append(s)
    
    # 退場
    for i in range(speed):
        if i == 0:
            x = w - rw2
        else:
            x = w - rw2 + int(rw2 * (i / (speed - 1)))
        
        affines.append((
            [1, 0, x],
            [0, 1, y],
            [0, 0, 1]
        ))

    return affines, img2

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

    tmp = Image.new('RGBA', img.size, (255, 255, 255, 0))
    tmp.paste(img)

    for i in range(speed):        
        if i == 0:
            x = w
        else:
            x = w - int(distance * (i / (speed - 1)))
            x = int(x * (i / (speed - 1)))
        print(w, h, w2, h2, rw2, rh2, x, y)
        # tmp.paste(img2, (x, h))

        two_padded = Image.new('RGBA', tmp.size, (255, 255, 255, 0))
        two_padded.paste(img2, (x, y))
        tmp2 = Image.alpha_composite(tmp, two_padded)
        tmp2.save(".tmp.png", quality=100)
        mat = cv2.imread(".tmp.png")
        video.write(mat)

    for i in range(0, 50, 1):
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

        two_padded = Image.new('RGBA', tmp.size, (255, 255, 255, 0))
        two_padded.paste(target, (x, y))
        tmp2 = Image.alpha_composite(tmp, two_padded)
        tmp2.save(".tmp.png", quality=100)
        mat = cv2.imread(".tmp.png")
        video.write(mat)
    
    for i in range(50, -50, -1):
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

        two_padded = Image.new('RGBA', tmp.size, (255, 255, 255, 0))
        two_padded.paste(target, (x, y))
        tmp2 = Image.alpha_composite(tmp, two_padded)
        tmp2.save(".tmp.png", quality=100)
        mat = cv2.imread(".tmp.png")
        video.write(mat)

    for i in range(-50, 0, 1):
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

        two_padded = Image.new('RGBA', tmp.size, (255, 255, 255, 0))
        two_padded.paste(target, (x, y))
        tmp2 = Image.alpha_composite(tmp, two_padded)
        tmp2.save(".tmp.png", quality=100)
        mat = cv2.imread(".tmp.png")
        video.write(mat)

    video.release()

# moveLeftToRight(Image.open('res/screen.png'), Image.open('res/sample/target.png'))

moveLeftToRightWithVideo('山郷.mp4', Image.open('山郷.png'), 'output山郷.mp4')
