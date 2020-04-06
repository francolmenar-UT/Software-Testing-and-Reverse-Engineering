import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

def read_data():
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    c1 = "Elapsed Time"
    c2 = "Covered Branches"

    data1 = pd.read_csv(filename1, sep=",", header=None, names=[c1, c2])
    data1[c1] = round(data1[c1].astype(float) / 1e6) #round numbers and convert them to ms
    # insert zero in both columns at index 1
    line = pd.DataFrame({c1: 0, c2: 0}, index=[0])
    data1 = pd.concat([data1.iloc[:0], line, data1.iloc[0:]]).reset_index(drop=True)

    data2 = pd.read_csv(filename2, sep=",", header=None, names=[c1, c2])
    data2[c1] = round(data2[c1].astype(float) / 1e6)  # round numbers and convert them to ms
    # insert zero in both columns at index 1
    data2 = pd.concat([data2.iloc[:0], line, data2.iloc[0:]]).reset_index(drop=True)

    # if data1[c1].iloc[data1.shape[0]-1] < data2[c1].iloc[data1.shape[0]-1]:
    #     endMeasure = data1[c1].iloc[data1.shape[0]-1]
    #     end_index1 = data1.loc[data1[c1] == endMeasure].index[0]
    # else:
    #     endMeasure = data2[c1].iloc[data1.shape[0]-1]
    #     end_index1 = data2.loc[data2[c1] == endMeasure].index[0]

    merged_df = pd.merge(data1, data2, how='outer', on=[c1],indicator=True)
    #merged_df[c2 + "_y"] = merged_df[c2 + "_y"].fillna(method='pad')
    #merged_df[c2 + "_x"] = merged_df[c2 + "_x"].fillna(method='pad')

    return merged_df

def print_data(data):
    sample_rate = 1
    data = data.iloc[::sample_rate, :] #reduces the number of datapoints

    fig, ax = plt.subplots()

    #data = data.dropna()
    ax.plot(data["Elapsed Time"], data["Covered Branches_x"], label="Problem11_seq", linewidth=0.7)
    ax.plot(data["Elapsed Time"], data["Covered Branches_y"], label="Problem11_gen", linewidth=0.7)

    #print (data.tail())
    # set plot ticks to be a timestamp and that there are always 7 ticks (7 fits well to the plot size)
    #plt.xticks(np.arange(0, data.shape[0], step=(data.shape[0]/6)-1),data["Elapsed Time"])

    ax.set_title('Convergence Graph')
    ax.legend()
    ax.set_ylabel("Branches")
    ax.set_xlabel("time (ms)")
    plt.show()

print_data(read_data())
