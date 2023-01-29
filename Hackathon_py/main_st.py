# This Program allows any user to gather their information off the dexcom
# website and easily view your information on any application and at home
# I AM NOT A MEDICAL PROFESSIONAL THIS IS A CONCEPT DO NOT TAKE THIS ADVICE

import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import streamlit as st


def main():
    st.write("DO NOT TAKE ANY ADVICE GIVEN BY THIS PROGRAM")
    print("Older Data:")
    fname_A = st.text_input("Older Data:", ".csv")
    print("Newer Data:")
    fname_B = st.text_input("Newer Data:", ".csv")
    print("Target BG:")
    target = st.text_input("Target BG:");
    clicked = st.button("Done")
    if clicked == 1:
        bg_data_A = get_bg_data(fname_A)
        bg_data_B = get_bg_data(fname_B)
        compare_data_draw(bg_data_A, bg_data_B)
        compare_data(bg_data_A, bg_data_B, target)


# Takes the information from Dexcoms auto generated csv and export it to a format in Pandas
def get_bg_data(fname):
    results = []
    with fname as csvfile:
        reader = csv.reader(csvfile)
        counter = 0
        for row in reader:
            if counter > 18:
                if row[7] != 'High' and row[7] != 'Low':
                    str_test = row[1]
                    length = len(str_test)
                    str_test = str_test[length - 8:length - 3]
                    hours = int(str_test[0] + str_test[1])
                    minutes = int(str_test[3] + str_test[4])
                    minutes = (hours * 60) + minutes
                    amount = (minutes, int(row[7]))
                    results.append(amount)
            else:
                counter = counter + 1
    data = sorted(results, key=lambda l: l[0])
    holding = [100, 1]
    done = []
    r = -1
    for i in data:
        if int(i[0] / 10) * 10 == r:
            holding[1] = holding[1] + i[1]
            holding[0] = holding[0] + 1
        else:
            avg = holding[1] / holding[0]
            done.append([r, avg])
            holding = [1, i[1]]
            r = int(i[0] / 10) * 10
    done.pop(0)
    df = pd.DataFrame(done, columns=['Minutes', 'Blood Sugar'], dtype=float)
    df = df.sort_values('Minutes')
    df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
    return df


# Drawing the plot of one graph for easily looking at data
def draw_data(df):
    df.plot(x='Minutes', y='Blood Sugar', kind='line')
    plt.show()


# Drawing the plots side by side for easy comparison
def compare_data_draw(df_1, df_2):
    df_1 = df_1.rename(columns={'Blood Sugar': 'Older'})
    df_2 = df_2.rename(columns={'Blood Sugar': 'Newer'})
    st.line_chart(df_1, x='Minutes', y='Older')
    st.line_chart(df_2, x='Minutes', y='Newer')
    #plt.show()


# This function takes the information and computes the average difference at all  points and compares
# the averages and compares them
def compare_data(df_1, df_2, target):
    dp_1 = []
    dp_2 = []
    for i in df_1.itertuples():
        dp_1.append(i)
    for i in df_2.itertuples():
        dp_2.append(i)
    counter = 0
    difference = 0
    diff = []
    avg = 0
    if len(dp_1) == len(dp_2):
        for i in range(len(dp_1)):
            counter = counter + 1
            diff.append([dp_1[i][2] - dp_2[i][2], i])
            difference = difference + diff[i][0]
            avg = dp_1[i][2] + avg
        avg_diff = difference / counter
        avg = avg / counter
        diff = sorted(diff, key=lambda l: l[0])
        st.write("The smallest difference was {} at minute {}".format(diff[0][0], diff[0][1]))
        st.write("The biggest difference was {} at minute {}".format(diff[-1][0], diff[-1][1]))
        st.write("Your BG has changed on average by {}".format(avg_diff))
        target_diff = avg - target*1.3
        if target_diff > 7:
            st.write("I recommend increasing your insulin ratio")
        elif target_diff < -5:
            st.write("I recommend lowering your insulin ratio")
        else:
            st.write("I do not recommend changing your insulin ratio")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
