import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lmfit import Model
import sys
import os

fig, axis = plt.subplots(2, 3, sharex=True, sharey=True)
plots = []

def calcFromPositionAndTime(path, i):
    raw_data = pd.read_csv(path, sep=";")
    raw_data = raw_data.dropna()

    # Convert danish numbers to english numbers
    for col in raw_data.columns:
        raw_data[col] = raw_data[col].str.replace(",", ".")


    raw_data = raw_data.astype(float)
    raw_data.columns = ["time", "position", "velocity", "acceleration"]

    time_list = raw_data["time"].to_list()
    position_list = raw_data["position"].to_list()

    for j in range(3):
        for i, pos in enumerate(position_list):
            diff = pos - position_list[i-1]
            if i == 0:
                continue
            elif diff > 0.09:
                del position_list[i]
                del time_list[i]
                continue

    

    for i, pos in enumerate(position_list):
        diff = pos - position_list[i-1]
        diff = math.fabs(diff)
        if i == 0:
            continue
        elif diff > 0.06:
            position_list = position_list[i+1:]
            time_list = time_list[i+1:]
            break

    for i, pos in enumerate(position_list):
        diff = pos - position_list[i-1]
        if i == 0:
            continue
        elif pos > position_list[i-1] * 1.5 or math.fabs(diff) < 0.05:
            position_list = position_list[:i-1]
            time_list = time_list[:i-1]
            break

    polyline = np.poly1d(np.polyfit(time_list, position_list, 1))

    velocity = polyline.c[0]

    plots.append(((time_list, polyline(time_list)), (time_list, position_list)))

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

    k = result.best_values["a"]

    xnew = np.linspace(-0.01, x[-1]+x[-1]/10, 100)
    ynew = result.eval(x=xnew)

    plt.figure()
    plt.plot(x, y, "bo")
    plt.plot(xnew, ynew, "r-")
    plt.suptitle(f"F_air = {k} * v²")
    plt.xlabel("Velocity (m/s)")
    plt.ylabel("Air Resistance (N)")
    plt.grid(True)

    return k

def calculator():
    doPlot = False
    if len(sys.argv) == 3:
        path = sys.argv[1]
        if sys.argv[2] == "plot":
            doPlot = True
    elif len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        print("Please provide path for data sets")
        sys.exit()
    files_in_path = sorted(os.listdir(path))

    data_sets_and_weight = []

    radius = float(input("\nRadius of original circle in cm: "))
    cutout_angle = float(input("\nAngle of cutout: "))
    
    for i, f in enumerate(files_in_path):
        if ".csv" in f:
            print(f"\n{f}")
            weight = float(input("Weight in grams: "))
            data_sets_and_weight.append((f, weight))


    velocity_list = []
    airRes_list = []

    for i, fw in enumerate(data_sets_and_weight):
        velocity_list.append(math.fabs(calcFromPositionAndTime(f"{path}{fw[0]}", i)))
        
        weight = fw[1] / 1000 # Convert grams to kg
        airRes = weight * 9.82

        airRes_list.append(airRes)

    plt.suptitle("Data sets")


    for i, plot in enumerate(plots):
        if i == 0:
            axis[0, 0].plot(plot[1][0], plot[1][1], "bo")
            axis[0, 0].plot(plot[0][0], plot[0][1], "r-")
            axis[0, 0].set_ylabel("Position (m)")
        elif i == 1:
            axis[0, 1].plot(plot[1][0], plot[1][1], "bo")
            axis[0, 1].plot(plot[0][0], plot[0][1], "r-")
        elif i == 2:
            axis[0, 2].plot(plot[1][0], plot[1][1], "bo")
            axis[0, 2].plot(plot[0][0], plot[0][1], "r-")
        elif i == 3:
            axis[1, 0].plot(plot[1][0], plot[1][1], "bo")
            axis[1, 0].plot(plot[0][0], plot[0][1], "r-")
            axis[1, 0].set_xlabel("Time (s)")
            axis[1, 0].set_ylabel("Position (m)")
        elif i == 4:
            axis[1, 1].plot(plot[1][0], plot[1][1], "bo")
            axis[1, 1].plot(plot[0][0], plot[0][1], "r-")
            axis[1, 1].set_xlabel("Time (s)")
        elif i == 5:
            axis[1, 2].plot(plot[1][0], plot[1][1], "bo")
            axis[1, 2].plot(plot[0][0], plot[0][1], "r-")
            axis[1, 2].set_xlabel("Time (s)")

    plt.tight_layout()






    k = calcK(velocity_list, airRes_list)

    open_angle, c_w = calcAngleAndCw(radius, cutout_angle, k)
    print("\n")
    print(100 * "=")
    print(f"\nangle = {open_angle}\nc_w = {c_w}")
    if doPlot:
        plt.show()

if __name__ == "__main__":
    calculator()
