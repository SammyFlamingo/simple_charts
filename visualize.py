import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# add any keys not wanted in the final dict. remove any that are desired
unused_keys = ["", "bikeid", "end station latitude", "end station longitude", "end station id",
               "start station latitude", "start station longitude", "start station id", "name_localizedValue0"]

# enter the path to the csv
csv_path = "/home/alex/projects/simple_charts/citibike_sample.csv"
current_year = datetime.today().year

dicts_list = []
trips_list = [[], [], []]
age_list = []
trip_averages = []


# builds list of dicts
def buildDictList():
    dict_reader = csv.DictReader(open(csv_path))
    dicts = []

    # add each row to the list as a dict
    for row in dict_reader:
        dicts.append(row)

    return dicts


# cleans the dicts
# adds trip lengths to trips_list, separated by gender
# calls calc_averages()
# calls calc_ages()
def wrangle_data():

    # pops the keys not desired in the dict
    for dict in buildDictList():
        for key in unused_keys:
            dict.pop(key)

        # relabels genders to be easily identified
        # separate the cleaned dicts into 3 lists of trip durations converted to  minutes
        if dict["gender"] == "0":
            dict["gender"] = "undisclosed"
            trips_list[0].append((int(dict["tripduration"]) / 60))
        if dict["gender"] == "1":
            dict["gender"] = "male"
            trips_list[1].append((int(dict["tripduration"]) / 60))
        if dict["gender"] == "2":
            dict["gender"] = "female"
            trips_list[2].append((int(dict["tripduration"]) / 60))

        calc_ages(dict)
    calc_averages()
    age_list.sort()

    return dicts_list, age_list


# calculates ages from birthyear and current year
def calc_ages(dict):
    age = int(current_year) - int(dict["birth year"])
    age_list.append(age)

    return dict


# calculate mean average of each trip list and append to list of averages
def calc_averages():
    for list_of_durations in trips_list:
        trip_averages.append(np.average(list_of_durations))

    return trip_averages


# returns a bar chart
def trips_bar(list_of_avgs):
    genders = ["Undisclosed", "Male", "Female"]

    # set the number of ticks on the x-axis
    x_axis = np.arange(len(genders))
    fig, bar_chart = plt.subplots()

    # plot a bar for each gender, set the color and label for each bar
    undisc, men, women = plt.bar(x_axis, list_of_avgs)
    undisc.set_facecolor("mediumorchid")
    undisc.set_label("Undisclosed")
    men.set_facecolor("blue")
    men.set_label("Men")
    women.set_facecolor("pink")
    women.set_label("Women")

    # sets attributes of the chart
    bar_chart.set_xticks(x_axis)
    bar_chart.set_xticklabels(["Undisclosed", "Men", "Women"])
    bar_chart.set_ylabel("Average Trip Duration")
    bar_chart.set_title("Trip Averages by Gender")
    bar_chart.legend()

    plt.show()

    return bar_chart


# display pie chart of each gender as a percent of the whole sample
def gender_percents(separated_trips):
    labels = "Undisclosed", "Male", "Female"
    trip_count = 0
    gender_percents = []

    # calculate the total number of trips
    for list in separated_trips:
        trip_count = trip_count + len(list)
    # calculate each gender's percent of the total
    for list in separated_trips:
        gender_percents.append(len(list) / trip_count)

    fig, pie_chart = plt.subplots()
    pie_chart.pie(gender_percents, explode=None, labels=labels, autopct="%1.1f%%")
    pie_chart.axis("equal")
    pie_chart.set_title("Genders as a Percent of the Sample")

    plt.show()

    return pie_chart


# display a histogram showing the distribution of ages in data
def age_distribution(list_of_ages):
    x = list_of_ages
    num_bins = max(list_of_ages) - min(list_of_ages)

    # the histogram of the data
    fig, hist_chart = plt.subplots()
    n, bins, patches = hist_chart.hist(x, num_bins)

    # sets attributes of the chart
    hist_chart.set_xlabel("Age of Rider")
    hist_chart.set_xticks(find_ticks())
    hist_chart.set_ylabel("Count of Riders")
    hist_chart.set_title("Number of Riders by Age")

    plt.show()

    return hist_chart


# creates integer list at increments of 5
def find_ticks():
    ticks_list = []

    if np.min(age_list) % 5 != 0:
        tick = age_list[0] - 4
        while tick % 5 != 0:
            tick = tick + 1
    else:
        tick = np.min(age_list)

    ticks_list.append(tick)

    while tick <= np.max(age_list):
        tick = tick + 5
        ticks_list.append(tick)

    return ticks_list


wrangle_data()
avg_trip_bar = trips_bar(trip_averages)
gender_pie = gender_percents(trips_list)
ages_histogram = age_distribution(age_list)
