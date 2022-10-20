import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity
import cv2
import os
import hashlib
import math


def normalize(data):
    return data / np.sum(data)


def hist_similarity(img1, img2, hist_size=256):
    imghistb1 = cv2.calcHist([img1], [0], None, [hist_size], [1, 254])
    imghistg1 = cv2.calcHist([img1], [1], None, [hist_size], [1, 254])
    imghistr1 = cv2.calcHist([img1], [2], None, [hist_size], [1, 254])

    imghistb2 = cv2.calcHist([img2], [0], None, [hist_size], [1, 254])
    imghistg2 = cv2.calcHist([img2], [1], None, [hist_size], [1, 254])
    imghistr2 = cv2.calcHist([img2], [2], None, [hist_size], [1, 254])

    distanceb = cv2.compareHist(normalize(imghistb1), normalize(imghistb2), cv2.HISTCMP_CORREL)
    distanceg = cv2.compareHist(normalize(imghistg1), normalize(imghistg2), cv2.HISTCMP_CORREL)
    distancer = cv2.compareHist(normalize(imghistr1), normalize(imghistr2), cv2.HISTCMP_CORREL)
    meandistance = np.mean([distanceb, distanceg, distancer])
    return meandistance


def individual_similarity(directory, cow, funcname):
    path = directory + cow + "\\"
    image_list = os.listdir(path)
    print("Processing " + str(len(image_list)) + " images...")
    result_num = len(image_list) * (len(image_list) - 1) // 2
    results = np.zeros((result_num, 3))
    count = 0
    for i in range(len(image_list)):
        img1_path = path + image_list[i]
        img1 = cv2.imread(img1_path)
        for j in range(i + 1, len(image_list)):
            img2_path = path + image_list[j]
            img2 = cv2.imread(img2_path)
            results[count, 0] = i
            results[count, 1] = j
            results[count, 2] = funcname(img1, img2)
            count += 1
    print("Similarity calculation is done.")

    np.savetxt(directory + funcname.__name__ + cow + ".txt", results, fmt='%.6f')
    print("txt is saved.\n")


def pair_similarity(directory, cow1, cow2, funcname):
    path1 = directory + cow1 + "\\"
    path2 = directory + cow2 + "\\"
    image_list1 = os.listdir(path1)
    image_list2 = os.listdir(path2)
    len_list1 = len(image_list1)
    len_list2 = len(image_list2)
    print("Processing " + str(len_list1) + " images in path1..")
    print("Processing " + str(len_list2) + " images in path2..")
    result_num = len_list1 * len_list2
    results = np.zeros((result_num, 3))
    count = 0
    for i in range(len_list1):
        img1_path = path1 + image_list1[i]
        img1 = cv2.imread(img1_path)
        for j in range(len(image_list2)):
            img2_path = path2 + image_list2[j]
            img2 = cv2.imread(img2_path)
            results[count, 0] = i
            results[count, 1] = j
            results[count, 2] = funcname(img1, img2)
            count += 1
    print("Similarity calculation is done.")

    np.savetxt(directory + funcname.__name__ + cow1 + "&" + cow2 + ".txt", results, fmt='%.6f')
    print("txt is saved.\n")


def PSNR(img1, img2):

    mse = np.mean((img1/255. - img2/255.) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 1
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))



if __name__ == '__main__':
    test_directory = "D:\\SummerProject\\Project\\Data\\RGBDCows202066\\Identification\\Depth\\"
    individuals = ['054', '069', '073', '173']
    for i in range(4):
        individual_similarity(test_directory, individuals[i], hist_similarity)
        for j in range(i+1, 4):
            pair_similarity(test_directory, individuals[i], individuals[j], hist_similarity)

