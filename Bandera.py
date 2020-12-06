'''         Image processing and computer vision
                  Pedro Elí Ruiz Zárate
               Electronic engineering student
              Pontificia Universidad Javeriana
                      Bogotá - 2020
'''
#import numpy library
import cv2
import numpy as np
import sys
import os
from hough import *
from sklearn.cluster import KMeans


class Bandera: #create the class

    def __init__(self, path = None): #Initialize the class
        if path is None: #If the user does not enter the path, one is left by default
            self.path = sys.argv[1] #Default path
        else:
            self.path = route
        image_name = input("What is the name of the image? ")
        path_file = os.path.join(self.path, image_name)
        self.image = cv2.imread(path_file) #Save the image in self


    def Colores(self): #displayProperties method
        rows, cols, ch = self.image.shape
        assert ch == 3
        self.image_array = np.reshape(self.image, (rows * cols, ch))
        model = KMeans(n_clusters = 4, random_state = 0).fit(self.image_array)
        self.labels = model.predict(self.image_array)
        self.min_labels = min(self.labels)
        self.max_labels = max(self.labels)
        self.n_of_colors = (self.max_labels + 1) - self.min_labels
        print("The number of colors in the image is: ", self.n_of_colors)

    def Porcentaje(self):
        colors = np.arange(self.min_labels, self.max_labels + 1)
        n = np.zeros_like(colors)
        for i in range(len(self.labels)):
            for j in range(len(colors)):
                if self.labels[i] == colors[j]:
                    n[j] += 1
        for k in range(len(colors)):
            perc = np.divide(n[k], len(self.labels)) * 100
            print("Color ", colors[k], "occupies ", perc, "% of the image.")

    def Orientacion(self):
        high_thresh = 300
        bw_edges = cv2.Canny(self.image, high_thresh * 0.3, high_thresh, L2gradient=True)

        hough_a = hough(bw_edges)
        accumulator = hough_a.standard_HT()

        acc_thresh = 50
        N_peaks = 11
        nhood = [25, 9]
        peaks = hough_a.find_peaks(accumulator, nhood, acc_thresh, N_peaks)
        [_, cols] = self.image.shape[:2]
        image_draw = np.copy(self.image)
        for i in range(len(peaks)):
            rho = peaks[i][0]
            theta_ = hough_a.theta[peaks[i][1]]
            theta_pi = np.pi * theta_ / 180
            theta_ = theta_ - 180

            if (np.abs(theta_) in range(0, 2)) or (np.abs(theta_) in range(178, 182)):
                print("vertical")
            elif (np.abs(theta_) in range(88, 92)) or (np.abs(theta_) in range(268, 272)):
                print("Horizontal")
            else:
                print("mixta")