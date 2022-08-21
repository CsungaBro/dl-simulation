import numpy as np
import matplotlib.pyplot as plt
import random 
import math


def main():
    x_nums = [-3, 6]
    y_nums = [-20, 10]
    
    x_nums = [0, 17]
    y_nums = [-15, 5]

    x_cords = np.linspace(x_nums[0], x_nums[1], 40)
    print(x_cords)
    x_cords_fine = np.linspace(x_nums[0]*1.5, x_nums[1]*1.5, 80)
    x_p = np.linspace(x_nums[0], x_nums[1], 100)
    y_og_cords = [og_function(x_cord) for x_cord in x_cords]
    y_og_cords_fine = [og_function(x_cord) for x_cord in x_cords_fine]

    max_error= 2
    y_error_cords = [error_value(y_cord, max_error) for y_cord in y_og_cords]
    y_error_cords_fine = [error_value(y_cord, max_error) for y_cord in y_og_cords_fine]
    # plt.plot(x_cords, y_og_cords, x_cords, y_error_cords)
    # plt.show()

    p_1 = np.poly1d(np.polyfit(x_cords, y_error_cords, 1))
    p_2 = np.poly1d(np.polyfit(x_cords, y_error_cords, 40))

    y_1 = [p_1(x_cord) for x_cord in x_p]
    y_2 = [p_2(x_cord) for x_cord in x_p]

    i = 0
    plt.figure(1)
    for x, y in zip([x_cords, x_p, x_p], [y_og_cords, y_1, y_2]):
        plt.subplot(131+i) # :D XD
        plt.plot(x_cords, y_error_cords, linestyle = 'none',  marker = '.', color='#575757')
        plt.plot(x, y, linestyle = '-', color='k')
        plt.xticks([])
        plt.yticks([])
        plt.ylim(y_nums)
        plt.xlim([x_nums[0]+1, x_nums[1]-1])
        i += 1    
    
    plt.show()

def og_function(num):
    # x_0 = 1
    # x_1 = -4.2
    # x_2 = -2.1
    # x_3 = 0.5
    x_0 = 0.2
    x_1 = -1.6
    x_2 = 1.3
    x_3 = -0.9    
    x_coeffs = [x_0, x_1, x_2, x_3]
    # return poly_func(x_coeffs, num)
    return num*math.sin(num*x_0)*x_1 + math.cos(num*x_2)

def poly_func(coeffs, num):
    val = 0
    for count, coeff in enumerate(coeffs):
        val += coeff*pow(num, count)
    return val

def error_value(num, max_error):
    const_error = random.random()*max_error
    const_error = const_error if random.random() > 0.5 else (-1)*const_error
    var_error = 0
    return num + var_error + const_error


def test_printer(x_cords, y_cords):
    for x_cord, y_cord in zip(x_cords, y_cords):
        print(x_cord, y_cord)    


def test_plotter(x_cords, y_cords):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x_cords, y_cords)
    plt.show()


if __name__ == "__main__":
    main()