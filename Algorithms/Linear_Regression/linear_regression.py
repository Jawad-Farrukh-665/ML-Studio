import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('C:/Users/HP/Documents/GitHub/ML-Studio/Algorithms/Linear Regression/processing')

from data_sanitization import reading_file

def making_matrices(props, dataframe):
    predictor_matrix = np.zeros((len(dataframe[props.target]),len(props.predictors)+1))
    for i in range(len(dataframe[props.target])):
        predictor_matrix[i, 0] = 1
    for j, predictor in enumerate(props.predictors):
        predictor_values = dataframe[predictor]
        for i, value in enumerate(predictor_values):
            predictor_matrix[i, j + 1] =  value
    props.target_matrix = np.zeros((len(dataframe[props.target]), 1))
    for i, value in enumerate(dataframe[props.target]):
        props.target_matrix[i, 0] = value
    predictor_matrix_transpose = np.transpose(predictor_matrix)
    intercept_matrix = np.dot(predictor_matrix_transpose, predictor_matrix)
    intercept_matrix = np.linalg.inv(intercept_matrix)
    intercept_matrix = np.dot(intercept_matrix, predictor_matrix_transpose)
    intercept_matrix = np.dot(intercept_matrix, props.target_matrix)
    return intercept_matrix
        
def gradient_descent(x, y, learning_rate , iterations, original_data, original_data_color, linear_regression_color):
    slope = 0
    intercept = 0
    for n in range(iterations):
        y_pred = []
        gradient_slope = 0
        gradient_intercept = 0
        for i in range(len(x)):
            y_value = (slope * x[i]) + intercept
            y_pred.append(y_value)
        for i in range(len(x)):
            gradient_slope = x[i] * (y[i] - ((slope * x[i]) + intercept))
            gradient_intercept = y[i] - ((slope * x[i]) + intercept)
        gradient_slope = (-2 / len(x)) * gradient_slope
        gradient_intercept = (-2 / len(x)) * gradient_intercept
        slope = slope - (learning_rate * gradient_slope)
        intercept = intercept - (learning_rate * gradient_intercept)
    y_values = []
    for i in range(len(x)):
        y_value = intercept + (x[i] * slope)
        y_values.append(y_value)
    plt.plot(x, y_values, label='Linear Regression After Gradient Descent', color=linear_regression_color, linestyle='-', marker='o')
    if original_data == 1:
        plt.scatter(x, y_values, label='Original Data', color=original_data_color, marker='x')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title("Linear Regression After Gradient Descent")
    plt.legend()
    plt.show()

def linear_regression(props):
    dataframe = reading_file(props.file_path)
    intercept_matrix = making_matrices(props.predictors, props.target, dataframe)
    x_points = dataframe[props.predictors[0]]
    y_points = dataframe[props.target]
    if len(props.predictors) == 1:
        x_axix = dataframe[props.predictors[0]]
        y_axis = []
        for i in range(len(x_axix)):
            y_value = intercept_matrix[0, 0] + (x_axix[i] * intercept_matrix[1, 0])
            y_axis.append(y_value)
        plt.plot(x_axix, y_axis, label='Linear Regression', color=props.linear_regression_color, linestyle='-', marker='o')
        if props.original_data == 1:
            plt.scatter(x_points, y_points, label='Original Data', color=props.original_data_color, marker='x')
        plt.xlabel(props.predictors[0])
        plt.ylabel(props.target)
        plt.title("Linear Regression")
        plt.legend()
        plt.show()
        if props.gradient_descent == 1:
            gradient_descent(x_points, y_points, props.learning_rate, props.iterations, props.original_data, props.original_data_color, props.linear_regression_color)
    if len(props.predictors) == 2:
        a = intercept_matrix[0, 0]
        a1 = intercept_matrix[1, 0]
        a2 = intercept_matrix[2, 0]
        x1 = np.linspace(dataframe[props.predictors[0]].min(), dataframe[props.predictors[0]].max(), 1000)
        x2 = np.linspace(dataframe[props.predictors[1]].min(), dataframe[props.predictors[1]].max(), 1000)
        original_x1_points = dataframe[props.predictors[0]]
        original_x2_points = dataframe[props.predictors[1]]
        original_y_points = dataframe[props.target]
        x1, x2 = np.meshgrid(x1, x2)
        y = a + a1 * x1 + a2 * x2
        fig = plt.figure()
        axis = fig.add_subplot(111, projection='3d')
        axis.plot_surface(x1, x2, y, alpha=0.5, rstride=100, cstride=100)
        axis.scatter(original_x1_points, original_x2_points, original_y_points, color='red', marker='o', label='Data Points')
        axis.set_xlabel(props.predictors[0])
        axis.set_ylabel(props.predictors[1])
        axis.set_zlabel(props.target)
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