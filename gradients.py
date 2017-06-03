from scipy import stats
import matplotlib.pyplot as plt
from numpy import genfromtxt, float, amax


def read_format_data(filename):
    points = genfromtxt(filename, delimiter=",", dtype=float, names=["Force", "Deflection"])

    points["Force"] = [(x / 1000) * 9.81 for x in points["Force"]]
    points["Deflection"] = [x * 0.0254 for x in points["Deflection"]]

    return points


def regression(points):
    (m_value, b_value, r_value, tt, stderr) = stats.linregress(points["Deflection"], points["Force"])
    print('regression: a=%.4f b=%.4f, r=%.2f, std error= %.3f' % (m_value, b_value, r_value, stderr))
    return [m_value, b_value, r_value, stderr]


def f(x, m, b):
    return m * x + b


def predicted_behavior(x, name):
    a_dict = {"Aluminum": 0.00100244817509536687068067880237,
              "Steel": 0.000317289348955451921911238594,
              "Wood": 0.001996995255847980609924630}
    return x / a_dict[name]


def plot_values(title_name, points, reg_values):
    x_max = amax(points["Deflection"])
    y_max = amax(points["Force"])

    spacing_x = x_max + x_max / 5
    spacing_y = y_max + y_max / 5

    plt.plot(points["Deflection"], points["Force"], "ko")

    plt.title("Force-Deflection Plot for " + title_name)

    plt.xlabel("Deflection (m {} 2.54E-6)".format(u"\u00B1"))
    plt.ylabel("Force (N {} 9.81E-5)".format(u"\u00B1"))

    plt.axis([0, spacing_x, 0, spacing_y])
    plt.text(spacing_x * 0.05, spacing_y * 0.8,
             "Linear Fit Equation: \ny ={0:.3f}x + {1:.3f} N/m \nr = {2:.2f} \nstd error = {3:.2f}".format(
                 reg_values[0],
                 reg_values[1],
                 reg_values[2],
                 reg_values[3]))

    plt.plot(points["Deflection"], f(points["Deflection"], reg_values[0], reg_values[1]), "k--",
             label="Linear Fit")

    plt.plot(points["Deflection"], predicted_behavior(points["Deflection"], title_name), label="Predicted Behavior")

    plt.legend(loc=4, borderaxespad=0.)

    plt.show()


def create_graph(name):
    points = read_format_data(name + ".csv")
    reg_values = regression(points)
    plot_values(name, points, reg_values)


create_graph("Aluminum")

create_graph("Steel")

create_graph("Wood")

plt.close("all")
