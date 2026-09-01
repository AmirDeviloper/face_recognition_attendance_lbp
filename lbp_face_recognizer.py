import cv2 as cv
import numpy as np
import os
import sys
from collections import Counter
from settings import PERSON_NOT_FOUND

class Image:
    def __init__(self, path: str, person_name: str = '?'):
        self.img = self.__get_grayscale_image(path)
        self.person_name = person_name.replace('_', ' ')
        self.histogram_value = None
    
    def compute_lbp_histogram(self):
        temp_array = np.zeros(self.img.shape, np.uint8)
        row, col = temp_array.shape
        for i in range(1, row - 1):
            for j in range(1, col - 1):
                temp_array[i, j] = self.__bin_2_decimal(self.__calc_lbp(self.img, i, j))

        hist = cv.calcHist([temp_array], [0], None, [256], [0, 256])
        self.histogram_value = cv.normalize(hist, hist)
        return self.histogram_value
    
    def compute_3x3_lbp_histogram(self):
        hist_parts_list = []
        for part_img in self.__crop_img(self.img):
            temp_array = np.zeros(part_img.shape, np.uint8)
            row, col = temp_array.shape
            for i in range(1, row - 1):
                for j in range(1, col - 1):
                    temp_array[i, j] = self.__bin_2_decimal(self.__calc_lbp(part_img, i, j))
            
            hist = cv.calcHist([temp_array], [0], None, [256], [0, 256])
            hist_parts_list.extend(cv.normalize(hist, hist))
        
        return hist_parts_list
    
    def __calc_lbp(self, image, i, j):
        sum_lbp = []
        center_pixel = image[i, j]

        sum_lbp.append(self.__lbp_condition(image[i - 1, j], center_pixel))
        sum_lbp.append(self.__lbp_condition(image[i - 1, j + 1], center_pixel))
        sum_lbp.append(self.__lbp_condition(image[i, j + 1], center_pixel))
        sum_lbp.append(self.__lbp_condition(image[i + 1, j + 1], center_pixel))
        sum_lbp.append(self.__lbp_condition(image[i + 1, j], center_pixel))
        sum_lbp.append(self.__lbp_condition(image[i + 1, j - 1], center_pixel))
        sum_lbp.append(self.__lbp_condition(image[i, j - 1], center_pixel))
        sum_lbp.append(self.__lbp_condition(image[i - 1, j - 1], center_pixel))
        return sum_lbp
    
    @staticmethod
    def __crop_img(image, row_size: int = 30, col_size: int = 30):
        windows = []
        row, col = image.shape
        for r in range(0, row - row_size, row_size):
            for c in range(0, col - col_size, col_size):
                windows.append(image[r:r + row_size, c:c + col_size])
        return windows
    
    @staticmethod
    def __lbp_condition(pixel, pixel_c):
        return 1 if pixel > pixel_c else 0

    @staticmethod
    def __bin_2_decimal(binary):
        res = 0
        bit_num = 0
        for i in binary[::-1]:
            res += i << bit_num
            bit_num += 1
        return res

    @staticmethod
    def __get_grayscale_image(path: str):
        return cv.cvtColor(cv.imread(path), cv.COLOR_BGR2GRAY)


class LBPRrecognation:
    def __init__(self, path: str, hardness: int):
        self.__img_3x3_histogram_list = []
        self.__path = path
        self.__get_all_3x3_image_inputs()
        self._hardness = hardness # lower value is harder detection.

    def __get_all_3x3_image_inputs(self):
        for subdir, _, files in os.walk(self.__path):
            images_per_category = []
            for file in files:
                if file.endswith('.pgm'):
                    img = Image(os.path.join(subdir, file), os.path.basename(subdir))
                    img.histogram_value = img.compute_3x3_lbp_histogram()
                    images_per_category.append(img)
            
            if len(images_per_category) > 0:
                self.__img_3x3_histogram_list.append(images_per_category)
                print(f'compution for [{img.person_name}] completed.')
    
    # initialize_3x3
    def find(self, test_image: str, k_neighbors: int):
        predict = self.__find_person(self.__img_3x3_histogram_list, test_image, k_neighbors)
        return predict

    # __generate_confusion_matrix
    def __find_person(self, in_list: list, test_img_path: str, k_neighbors: int):

        trainings = in_list

        test_img = Image(test_img_path)
        
        test_img.histogram_value = test_img.compute_3x3_lbp_histogram()

        test_result = []
                
        for trainings_list in trainings:
            for training_img in trainings_list:
                distance = self.chi2_distance(
                    test_img.histogram_value, 
                    training_img.histogram_value
                )
                test_result.append((distance, training_img.person_name))
        
        test_result = sorted(test_result, key=lambda x: x[0])
        k_neighbors = min(k_neighbors, len(test_result))
        nearest_neighbors = test_result[:k_neighbors]
                
        neighbor_categories = [person_name for _, person_name in nearest_neighbors]
                
        print(test_img_path.split('\\')[-1].split('-')[0].replace('_', ' '), end = ' - ')
        if neighbor_categories:
            names_counts = Counter(neighbor_categories)
            most_common_name, find_counts = names_counts.most_common(1)[0]

            winner_vote_count = find_counts
            votes_needed_for_confidence = k_neighbors - self._hardness

            return PERSON_NOT_FOUND if winner_vote_count < votes_needed_for_confidence else most_common_name
        else:
            return None

    @staticmethod
    def chi2_distance(vector_a, vector_b):
        eps = sys.float_info.epsilon
        return 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(vector_a, vector_b)])
