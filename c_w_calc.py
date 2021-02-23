import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lmfit import Model
import sys
import os


# Args are later going to be paths to .csv files
def calcFromPositionAndTime(path):
    raw_data = pd.read_csv(path, sep=";")
    raw_data = raw_data.dropna()

    # Convert danish numbers to english numbers
    for col in raw_data.columns:
        raw_data[col] = raw_data[col].str.replace(",", ".")
        # raw_data[col] = raw_data[col].str.replace("-", "")


    raw_data = raw_data.astype(float)
    raw_data.columns = ["time", "position", "velocity", "acceleration"]

    time_list = raw_data["time"].to_list()
    position_list = raw_data["position"].to_list()

    for j in range(5):
        for i, pos in enumerate(position_list):
            diff = math.fabs(pos - position_list[i-1])
            if i == 0:
                continue
            elif diff > 0.15 or diff < 0.05:
                del position_list[i]
                del time_list[i]
                continue

    for i, pos in enumerate(position_list):
        if i == 0:
            continue
        elif math.fabs(pos - position_list[i-1]) > 0.15:
            position_list = position_list[:i-1]
            time_list = time_list[:i-1]
            break

    del time_list[0]
    del position_list[0]

    polyline = np.poly1d(np.polyfit(time_list, position_list, 1))

    velocity = polyline.c[0]

    # plt.plot(time_list, polyline(time_list))

    # plt.plot(time_list, position_list, "bo")

    # plt.show()

    return velocity

def calcAngleAndCw(radius_original, cutout_angle, k):
    rho_air = 1.204

    part = 1.0 - cutout_angle / 360.0

    radius_new = part * radius_original

    area = (math.pi * radius_new**2.0) / 10000

    open_angle = (2.0 * math.asin(radius_new / radius_original)) * (180.0 / math.pi)

    c_w = (2.0 * k) / (rho_air * area)

    return open_angle, c_w



def template(x, a, b):
    return a * x**2 + b

def calcK(x, y):
    pmodel = Model(template)
    params = pmodel.make_params(a=1, b=0)

    params["b"].vary = False

    result = pmodel.fit(y, params, x=x)

    xnew = np.linspace(-0.01, x[-1]+x[-1]/10, 100)
    ynew = result.eval(x=xnew)

    plt.plot(x, y, "bo")
    # plt.plot(x, result.best_fit, "k-")
    plt.plot(xnew, ynew, "r-")
    # plt.grid(True)
    plt.xlabel("Velocity (m/s)")
    plt.ylabel("Air Resistance (N)")

    return result.best_values["a"]

def calculator():
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = "./"
    files_in_path = sorted(os.listdir(path))

    data_sets_and_weight = []

    radius = float(input("\nRadius of original circle in cm: "))
    cutout_angle = float(input("\nAngle of cutout: "))
    
    print("\n'y' for yes and 'n' for no\n")
    for f in files_in_path:
        if ".csv" in f:
            answer = input(f"Use {f} ?: ")
            if answer == "y":
                weight = float(input("Weight in grams: "))
                print("\n")
                data_sets_and_weight.append((f, weight))
            elif answer != "n":
                sys.exit()

    velocity_list = []
    airRes_list = []

    for fw in data_sets_and_weight:
        velocity_list.append(calcFromPositionAndTime(f"{path}{fw[0]}"))
        
        weight = fw[1] / 1000 # Convert grams to kg
        airRes = weight * 9.82

        airRes_list.append(airRes)

    k = calcK(velocity_list, airRes_list)

    open_angle, c_w = calcAngleAndCw(radius, cutout_angle, k)
    print(open_angle, c_w)

if __name__ == "__main__":
    calculator()
