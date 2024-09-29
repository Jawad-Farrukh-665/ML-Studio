import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('C:/Users/HP/Documents/GitHub/ML-Studio/Algorithms/Linear Regression/processing')

from data_sanitization import reading_file

def making_matrices(predictors, target, dataframe):
    predictor_matrix = np.zeros((len(dataframe[target]),len(predictors)+1))
    for i in range(len(dataframe[target])):
        predictor_matrix[i, 0] = 1
    for j, predictor in enumerate(predictors):
        predictor_values = dataframe[predictor]
        for i, value in enumerate(predictor_values):
            predictor_matrix[i, j + 1] =  value
    target_matrix = np.zeros((len(dataframe[target]), 1))
    for i, value in enumerate(dataframe[target]):
        target_matrix[i, 0] = value
    predictor_matrix_transpose = np.transpose(predictor_matrix)
    intercept_matrix = np.dot(predictor_matrix_transpose, predictor_matrix)
    intercept_matrix = np.linalg.inv(intercept_matrix)
    intercept_matrix = np.dot(intercept_matrix, predictor_matrix_transpose)
    intercept_matrix = np.dot(intercept_matrix, target_matrix)
    return intercept_matrix
        

def linear_regression(file_path, target, predictors):
    dataframe = reading_file(file_path)
    intercept_matrix = making_matrices(predictors, target, dataframe)
    x_points = dataframe[predictors[0]]
    y_points = dataframe[target]
    if len(predictors) == 1:
        x_axix = dataframe[predictors[0]]
        y_axis = []
        for i in range(len(x_axix)):
            y_value = intercept_matrix[0, 0] + (x_axix[i] * intercept_matrix[1, 0])
            y_axis.append(y_value)
        plt.plot(x_axix, y_axis, label='Linear Regression', color='#16423C', linestyle='-', marker='o')
        plt.scatter(x_points, y_points, label='Original Data', color='red', marker='x')
        plt.xlabel(predictors[0])
        plt.ylabel(target)
        plt.title("Linear Regression")
        plt.legend()
        plt.show()
    if len(predictors) == 2:
        a = intercept_matrix[0, 0]
        a1 = intercept_matrix[1, 0]
        a2 = intercept_matrix[2, 0]
        x1 = np.linspace(dataframe[predictors[0]].min(), dataframe[predictors[0]].max(), 1000)
        x2 = np.linspace(dataframe[predictors[1]].min(), dataframe[predictors[1]].max(), 1000)
        original_x1_points = dataframe[predictors[0]]
        original_x2_points = dataframe[predictors[1]]
        original_y_points = dataframe[target]
        x1, x2 = np.meshgrid(x1, x2)
        y = a + a1 * x1 + a2 * x2
        fig = plt.figure()
        axis = fig.add_subplot(111, projection='3d')
        axis.plot_surface(x1, x2, y, alpha=0.5, rstride=100, cstride=100)
        axis.scatter(original_x1_points, original_x2_points, original_y_points, color='red', marker='o', label='Data Points')
        axis.set_xlabel(predictors[0])
        axis.set_ylabel(predictors[1])
        axis.set_zlabel(target)
        axis.set_title("Linear Regression")
        plt.show()
    equation = "y = "
    for i in range(intercept_matrix.shape[0]):
        if equation and intercept_matrix[i, 0] > 0 and i > 0:
            equation += " + "
        else:
            equation += " - "
        equation += str(intercept_matrix[i, 0])
        if i > 0 :
            equation += f"x{i}"
    return equation    