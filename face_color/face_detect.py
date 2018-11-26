import cv2

from sklearn.cluster import KMeans
import imutils
import numpy as np

import os


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist


def plot_colors2(hist, centroids):

    result = []

    for (percent, color) in zip(hist, centroids):
        result.append((percent, color))

    # return the bar chart
    return result


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)


def face_with_image(image, face_frame):
    img_copy = imutils.resize(image, width=600)
    (x, y, w, h) = face_frame
    crop_img = img_copy[y:y + h, x:x + w]
    return crop_img


def draw_plain_color(width=50, height=50, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image


def dnn_get_face(image):

    protoPath = "deploy.prototxt"
    modelPath = "res10_300x300_ssd_iter_140000.caffemodel"
    detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

    image = imutils.resize(image, width=600)
    (h, w) = image.shape[:2]

    # construct a blob from the image
    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    # apply OpenCV's deep learning-based face detector to localize
    # faces in the input image
    detector.setInput(imageBlob)
    detections = detector.forward()

    found_shape = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections
        if confidence > 0.6:
            # compute the (x, y)-coordinates of the bounding box for the
            # face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI
            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                continue

            width = endX - startX
            height = endY - startY
            found_shape.append((startX, startY, width, height))

    return found_shape


def draw_square_on_image(image, face_frame):
    (x, y, w, h) = face_frame
    image = imutils.resize(image, width=600)
    cv2.rectangle(image, (x, y), (x+w, y+h),
                  (0, 0, 255), 2)
    return image


def get_dominate_colors(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))  # represent as row*column,channel number
    clt = KMeans(n_clusters=3)  # cluster number
    clt.fit(img)
    hist = find_histogram(clt)
    highest_colors = plot_colors2(hist, clt.cluster_centers_)
    return highest_colors


def get_highest_color(colors):
    h_c = None
    h_p = None
    for (persentage, color_result) in highest_colors:
        if h_p is None:
            h_p = persentage
            h_c = color_result
        elif h_p < persentage:
            h_p = persentage
            h_c = color_result
    return h_c


if __name__ == '__main__':

    use_camera = False

    if use_camera:
        cam = cv2.VideoCapture(0)

        while True:
            ret, img_col = cam.read()

            shapes_found = dnn_get_face(img_col)
            face = face_with_image(img_col, shapes_found[0])
            cv2.imshow("face", face)

            origin_i = draw_square_on_image(img_col, shapes_found[0])
            cv2.imshow("origin", origin_i)


            highest_colors = get_dominate_colors(face)
            h = get_highest_color(highest_colors)

            plain_image_2 = draw_plain_color(rgb_color=h)
            cv2.imshow("highest", plain_image_2)

            waitkey = cv2.waitKey(5)
            if waitkey != -1:
                break

    else:

        test2 = cv2.imread('../image_asset/071249078747_T4.jpg')
        img_col = test2
        shapes_found = dnn_get_face(img_col)
        face = face_with_image(img_col, shapes_found[0])
        cv2.imshow("face", face)

        origin_i = draw_square_on_image(img_col, shapes_found[0])
        cv2.imshow("origin", origin_i)

        highest_colors = get_dominate_colors(face)
        h = get_highest_color(highest_colors)

        plain_image_2 = draw_plain_color(rgb_color=h)
        cv2.imshow("highest", plain_image_2)

        cv2.waitKey()
