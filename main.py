import cv2
import numpy as np

def keypoints_detector(image, out='gray_im'):
    gray_im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints, features = sift.detectAndCompute(image, None)
    keypoints_image = cv2.drawKeypoints(
        gray_im, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    if out == 'keypoints_im':
        out_im = keypoints_image
    elif out == 'gray_im':
        out_im = gray_im
    else:
        raise TypeError(f'{out}, Invalid out type.')
    return keypoints, features, out_im

def matching(features_left, features_right, ratio=0.6):
    good = []
    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(features_right, features_left, k=2)
    
    for m, n in matches:
        if m.distance < ratio*n.distance:
            good.append(m)

    return good

def stitching(left_image, right_image):
    keypoints_left, features_left, _ = keypoints_detector(left_image)
    keypoints_right, features_right, _ = keypoints_detector(right_image)

    mathches = matching(features_left, features_right)

    if len(mathches) > 4:
        points_left = np.float32(
            [keypoints_left[m.trainIdx].pt for m in mathches]).reshape(-1, 1, 2)
        points_right = np.float32(
            [keypoints_right[m.queryIdx].pt for m in mathches]).reshape(-1, 1, 2)
        M, _ = cv2.findHomography(points_right, points_left, cv2.RANSAC, 5.0)
        warp_im = cv2.warpPerspective(right_image, M, (left_image.shape[1] + right_image.shape[1], right_image.shape[0]))
        seam_im = warp_im.copy()
        seam_im[0:left_image.shape[0], 0:left_image.shape[1]] = left_image[0:seam_im.shape[0], 0:seam_im.shape[1]]
        
        left_image = left_image[0:warp_im.shape[0], 0:warp_im.shape[1]]
        rows, cols, _ = left_image.shape
        for col in range(0, cols):
            if left_image[:, col].any() and warp_im[:, col].any():
                left = col
                break
        for col in range(cols-1, 0, -1):
            if left_image[:, col].any() and warp_im[:, col].any():
                right = col
                break

        tmp = np.zeros([rows, cols, 3], np.uint8)
        
        for row in range(0, rows):
            for col in range(0, cols):
                if not left_image[row, col].any():
                    tmp[row, col] = warp_im[row, col]
                elif not warp_im[row, col].any():
                    tmp[row, col] = left_image[row, col]
                else:
                    srcImgLen = float(abs(col - left))
                    testImgLen = float(abs(col - right))
                    alpha = srcImgLen / (srcImgLen + testImgLen)
                    tmp[row, col] = np.clip(left_image[row, col] * (1-alpha) + warp_im[row, col] * alpha, 0, 255)

        warp_im[0:left_image.shape[0], 0:left_image.shape[1]] = tmp
        
        return warp_im, seam_im
    else:
        return None