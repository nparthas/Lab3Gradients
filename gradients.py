from scipy import stats
import matplotlib.pyplot as plt
from numpy import genfromtxt, float, amax


def read_format_data(filename):
    points = genfromtxt(filename, delimiter=",", dtype=float, names=["Strain", "Stress"])
    name = filename.replace('.csv', "")

    l_0 = {
        "as_received": 32.033333333333333,
        "annealed": 31.113333333333,
        "cold_rolled": 19.4
    }
    csa = {
        "as_received": 1.15759 * 10**-5,
        "cold_rolled": 7.9576 * 10**-6,
        "annealed": 1.5616 * 10**-5
    }
    points["Strain"] = [(x / l_0[name]) for x in points["Strain"]]
    points["Stress"] = [(x * 9.80665)/csa[name] for x in points["Stress"]]

    return points


def regression(data_x, data_y):
    (m_value, b_value, r_value, tt, stderr) = stats.linregress(data_x, data_y)
    print('regression: a=%.4f b=%.4f, r=%.2f, std error= %.3f' % (m_value, b_value, r_value, stderr))
    return [m_value, b_value, r_value, stderr]


def f(x, m, b):
    return m * x + b


def offset(x, m, b):
    x_0 = (-b / m) + 0.02
    new_b = -1 * x_0 * m
    print(b)
    print(new_b)
    return m * x + new_b


def plot_values(title_name, points, reg_values):
    x_max = amax(points['Strain'])
    y_max = amax(points["Stress"])

    spacing_x = x_max + x_max / 10
    spacing_y = y_max + y_max / 4

    plt.plot(points["Strain"], points['Stress'], "ko")

    plt.title("Stress-Strain Plot for {} Aluminum".format(title_name))

    plt.xlabel("Strain")
    plt.ylabel("Stress (Pa)")

    plt.axis([0, spacing_x, 0, spacing_y])

    plt.text(spacing_x * 0.04, spacing_y * 0.85,
             "Linear Fit Equation for Elastic Region: \ny ={0:.3f}E9x + {1:.3f}E6 Pa \nr = {2:.2f}"
             .format(
                 (reg_values[0]/10**9),
                 (reg_values[1]/10**6),
                 reg_values[2]))

    plt.plot(points["Strain"][:7], f(points["Strain"][:7], reg_values[0], reg_values[1]), "k--",
             label="Linear Fit")

    plt.plot(points["Strain"][:9], offset(points["Strain"][:9], reg_values[0], reg_values[1]), label="0.2% offset")

    plt.legend(loc=4, borderaxespad=0.)

    plt.show()


points = read_format_data("annealed.csv")
reg_values = regression(points["Strain"][:6], points["Stress"][:6])
plot_values("Annealed", points, reg_values)



