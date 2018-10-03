import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# add any keys not wanted in the final dict. remove any that are desired
unused_keys = ["", "bikeid", "end station latitude", "end station longitude", "end station id",
               "start station latitude", "start station longitude", "start station id", "name_localizedValue0"]

# enter the path to the csv
csv_path = "file path"


# builds list of dicts
def buildDictList(csv_location):
    dict_reader = csv.DictReader(open(csv_location))
    dicts = []

    # add each row to the list as a dict
    for row in dict_reader:
        dicts.append(row)

    return dicts


# cleans the dicts
def cleanData(list_of_dicts, list_keys_removed):
    # pops the keys not desired in the dict
    for dict in list_of_dicts:
        for key in list_keys_removed:
            dict.pop(key)

        # relabels genders to be easily identified
        if dict["gender"] == "0":
            dict["gender"] = "undisclosed"
        if dict["gender"] == "1":
            dict["gender"] = "male"
        if dict["gender"] == "2":
            dict["gender"] = "female"

    return list_of_dicts


# calculates ages from birthyear and current year
def calcAges(dicts_list):
    age_list = []
    current_year = datetime.today().year

    for dict in dicts_list:
        age = int(current_year) - int(dict["birth year"])
        age_list.append(age)

    age_list.sort()

    return age_list


# separate the cleaned list of dicts into 3 lists of trip durations

def separateTrips(cleaned_dicts):
    trips_list = [[], [], []]

    # adding each gender's trips to their trip list and converting seconds to minutes
    for dict in cleaned_dicts:
        if dict["gender"] == "undisclosed":
            trips_list[0].append((int(dict["tripduration"]) / 60))
        if dict["gender"] == "male":
            trips_list[1].append((int(dict["tripduration"]) / 60))
        if dict["gender"] == "female":
            trips_list[2].append((int(dict["tripduration"]) / 60))

    return trips_list


# calculate mean average of each trip list and append to list of averages
def calcAvgs(trips_list):
    trip_avgs = []

    for list in trips_list:
        trip_avgs.append(np.average(list))

    return trip_avgs


# returns a bar chart
def barOfTrips(list_of_avgs):
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

    return bar_chart


# display pie chart of each gender as a percent of the whole sample
def pieOfGenders(separated_trips):
    labels = "Undisclosed", "Male", "Female"
    tripcount = 0
    gender_percents = []

    # calculate the total number of trips
    for list in separated_trips:
        tripcount = tripcount + len(list)
    # calculate each gender's percent of the total
    for list in separated_trips:
        gender_percents.append(len(list) / tripcount)

    fig, pie_chart = plt.subplots()
    pie_chart.pie(gender_percents, explode=None, labels=labels, autopct="%1.1f%%")
    pie_chart.axis("equal")
    pie_chart.set_title("Genders as a Percent of the Sample")

    return pie_chart


def histChart(list_of_ages):
    x = list_of_ages
    num_bins = max(list_of_ages) - min(list_of_ages)

    # the histogram of the data
    fig, hist_chart = plt.subplots()
    n, bins, patches = hist_chart.hist(x, num_bins)

    # sets attributes of the chart
    hist_chart.set_xlabel("Age of Rider")
    hist_chart.set_xticks([20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
    hist_chart.set_ylabel("Count of Riders")
    hist_chart.set_title("Number of Riders by Age")

    return hist_chart


dicts_list = cleanData(buildDictList(csv_path), unused_keys)
age_list = calcAges(dicts_list)
separated_trips = separateTrips(dicts_list)
avgs_list = calcAvgs(separated_trips)
avg_trip_bar = barOfTrips(avgs_list)
pie_chart = pieOfGenders(separated_trips)
histogram_chart = histChart(age_list)