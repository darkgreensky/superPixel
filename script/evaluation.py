import numpy as np
from PyQt5.QtWidgets import QMessageBox


def calculate_compactness(labels):
    superpixels = np.max(labels) + 1

    perimeter = np.zeros(superpixels)
    area = np.zeros(superpixels)

    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            count = 0

            if i > 0:
                if labels[i, j] != labels[i - 1, j]:
                    count += 1
            else:
                count += 1

            if i < labels.shape[0] - 1:
                if labels[i, j] != labels[i + 1, j]:
                    count += 1
            else:
                count += 1

            if j > 0:
                if labels[i, j] != labels[i, j - 1]:
                    count += 1
            else:
                count += 1

            if j < labels.shape[1] - 1:
                if labels[i, j] != labels[i, j + 1]:
                    count += 1
            else:
                count += 1

            perimeter[labels[i, j]] += count
            area[labels[i, j]] += 1

    compactness = 0

    for i in range(superpixels):
        if perimeter[i] > 0:
            compactness += area[i] * (4 * np.pi * area[i]) / (perimeter[i] * perimeter[i])

    compactness /= labels.size

    if compactness > 1.0:
        print("Invalid compactness:", compactness)

    return compactness

def compute_intersection_matrix(labels, gt):
    superpixels = np.max(labels) + 1
    gt_segments = np.max(gt) + 1

    superpixel_sizes = np.zeros(superpixels, dtype=int)
    gt_sizes = np.zeros(gt_segments, dtype=int)

    intersection_matrix = np.zeros((gt_segments, superpixels), dtype=int)

    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            intersection_matrix[gt[i, j], labels[i, j]] += 1
            superpixel_sizes[labels[i, j]] += 1
            gt_sizes[gt[i, j]] += 1

    return intersection_matrix, superpixel_sizes, gt_sizes

def compute_undersegmentation_error(labels, gt):
    H, W = gt.shape
    N = H * W

    intersection_matrix, superpixel_sizes, gt_sizes = compute_intersection_matrix(labels, gt)

    if intersection_matrix is None:
        return None

    error = 0
    for j in range(intersection_matrix.shape[1]):
        min_diff = np.inf
        for i in range(intersection_matrix.shape[0]):
            superpixel_j_minus_gt_i = superpixel_sizes[j] - intersection_matrix[i, j]
            if superpixel_j_minus_gt_i < 0:
                print("Set difference is negative.")
            if superpixel_j_minus_gt_i < min_diff:
                min_diff = superpixel_j_minus_gt_i

        error += min_diff
    return error / N

def compute_boundary_recall(labels, gt, d=0.0025):
    H, W = gt.shape
    r = int(round(d * np.sqrt(H * H + W * W)))
    tp = 0
    fn = 0

    for i in range(H):
        for j in range(W):
            if is_4_connected_boundary_pixel(gt, i, j):
                pos = False
                for k in range(max(0, i - r), min(H - 1, i + r) + 1):
                    for l in range(max(0, j - r), min(W - 1, j + r) + 1):
                        if is_4_connected_boundary_pixel(labels, k, l):
                            pos = True
                if pos:
                    tp += 1
                else:
                    fn += 1

    if tp + fn > 0:
        return tp / (tp + fn)
    return 0


def compute_boundary_precision(labels, gt, d=0.0025):
    H, W = gt.shape
    r = round(d * np.sqrt(H * H + W * W))

    tp = 0
    fp = 0

    for i in range(H):
        for j in range(W):
            if is_4_connected_boundary_pixel(gt, i, j):

                pos = False
                # Search for boundary pixel in the supervoxel segmentation.
                for k in range(max(0, i - r), min(H - 1, i + r) + 1):
                    for l in range(max(0, j - r), min(W - 1, j + r) + 1):
                        if is_4_connected_boundary_pixel(labels, k, l):
                            pos = True

                if pos:
                    tp += 1
            elif is_4_connected_boundary_pixel(labels, i, j):
                pos = False
                # Search for boundary pixel in the supervoxel segmentation.
                for k in range(max(0, i - r), min(H - 1, i + r) + 1):
                    for l in range(max(0, j - r), min(W - 1, j + r) + 1):
                        if is_4_connected_boundary_pixel(gt, k, l):
                            pos = True

                if not pos:
                    fp += 1

    if tp + fp > 0:
        return tp / (tp + fp)

    return 0

def is_4_connected_boundary_pixel(labels, i, j):
    if i > 0:
        if labels[i, j] != labels[i - 1, j]:
            return True

    if i < labels.shape[0] - 1:
        if labels[i, j] != labels[i + 1, j]:
            return True

    if j > 0:
        if labels[i, j] != labels[i, j - 1]:
            return True

    if j < labels.shape[1] - 1:
        if labels[i, j] != labels[i, j + 1]:
            return True

    return False

def compute_achievable_segmentation_accuracy(labels, gt):
    H, W = gt.shape[:2]
    N = H * W

    intersection_matrix, superpixel_sizes, gt_sizes = compute_intersection_matrix(labels, gt)

    accuracy = 0
    for j in range(intersection_matrix.shape[1]):
        max_intersection = np.max(intersection_matrix[:, j])
        accuracy += max_intersection

    return accuracy / N