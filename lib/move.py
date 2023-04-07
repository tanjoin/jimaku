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

def moveLeftToRightWithVideo(video_path, img2):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return
    
    # os.makedirs(dir_path, exist_ok=True)    
    # base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    print('digit: {}'.format(digit))

    # cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = (int(width), int(height))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print('fps: {}'.format(fps))
    print('size: {}'.format(size))

    codec = cv2.VideoWriter_fourcc(*"mp4v")
    video  = cv2.VideoWriter('output.mp4', codec, fps, size)

    # 変換設定
    affines, img2 = leftToRight_FuwaFuwa(size, img2, 24)

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
        rh2 = h
    else:
        rh2 = h2
    rw2 = int(w2 * (rh2 / h2))
    img2 = img2.copy().resize((rw2, rh2))

    distance = rw2
    y = h - rh2

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

    # ふわふわ
    for j in range(fuwaloop):
        for i in range(0, 50, 1):
            target = img2.copy()
            # 回転
            rad = numpy.radians(i/10)
            r = numpy.array([
                [numpy.cos(rad), -numpy.sin(rad), i + x],
                [numpy.sin(rad),  numpy.cos(rad), 0 + y],
                [             0,               0, 1]
            ])
            affines.append(r)
        
        for i in range(50, -50, -1):
            target = img2.copy()
            # 回転
            rad = numpy.radians(i/10)
            r = numpy.array([
                [numpy.cos(rad), -numpy.sin(rad), i + x],
                [numpy.sin(rad),  numpy.cos(rad), 0 + y],
                [             0,               0, 1]
            ])
            affines.append(r)

        for i in range(-50, 0, 1):
            target = img2.copy()
            # 回転
            rad = numpy.radians(i/10)
            r = numpy.array([
                [numpy.cos(rad), -numpy.sin(rad), i + x],
                [numpy.sin(rad),  numpy.cos(rad), 0 + y],
                [             0,               0, 1]
            ])
            affines.append(r)
    
    # 退場
    for i in range(speed):
        if i == 0:
            x = w - w2
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

moveLeftToRightWithVideo('ラム.mp4', Image.open('ラム.png'))
