"""
IS590 PR - Assignment 2

Instructor: Mr. Weible
Author: Alan Chen
NetID: ycchen4
"""

"""
Program introduction:
the user can pass the two .txt file as a parameter to the "process_storm_data" funciton 
to calculate the raw data then print the result of the question 2.

"""

"====================================================================================================================="
"MARK: Import Library"
"""
The only library used in this assignment is PrettyTable
ref: https://github.com/jazzband/prettytable
"""
from prettytable import PrettyTable

"====================================================================================================================="
"MARK: Function definition"


def process_storm_data(file_name, result_dict):
    """
    The main function to read the raw data line by line.
    Meanwhile, the function will find and calculate the five questions in the assignment - ID, name, start date, end date,
    highest Maximum sustained wind, and the count of landfall

    :param file_name: name of file in .txt format
    :param result_dict: an empty dictionary to gather the storm data for future use, such as print on console or output a file
    :return: None
    """
    with open(file_name, 'r') as input_file:
        # initiate a dictionary for the storm
        storm_dict = reset_storm_dict()

        current_line_count = 0
        for line in input_file:

            # if the first two characters of the string is alphabetic, then it is the header line
            if line[0:2].isalpha():
                # 1. print the id and name
                # print('Storm system ID is ' , line[0:4])
                storm_dict["stormID"] = line[0:4]

                if line.find('UNNAMED', 18, 28) == -1:
                    # print('the name of the storm is ', line[18:28])
                    storm_dict["name"] = line[19:28].replace(" ", "")

                # set how many lines of this storm data
                current_line_count = int(line[33:36])

                continue

            # start count lines for this storm
            current_line_count -= 1

            # if the first two characters of the string is not alphabetic, then it is the data line
            # 2. start date and end date of the storm
            if storm_dict["startDate"] is None:
                storm_dict["startDate"] = line[0:8]

            # if input_file.__next__() is not None:
            #     if input_file.__next__()[0:2].isalpha() and storm_dict["endDate"] is None:
            storm_dict["endDate"] = line[0:8]

            # 3. The highest Maximum sustained wind (in knots) and when it first occurred (date & time)
            current_sustained_wind = int(line[38:41])
            if current_sustained_wind != "-99" and current_sustained_wind > storm_dict["maxSustainedWind"]:
                storm_dict["maxSustainedWind"] = current_sustained_wind
                date_string = line[0:8]
                storm_dict["maxSustainedWind_time"] = \
                    date_string[0:4] + "/" + date_string[4:6] + "/" + date_string[6:] + " " \
                    + line[10:12] + ":" + line[12:14]

            # 4. The total pressure change in millibars. (highest minus lowest)
            calculate_pressure_change(storm_dict, int(line[43:47]))

            # 5. How many times it had a “landfall”
            if line[16:17] == 'L':
                storm_dict["landfallCount"] = storm_dict["landfallCount"] + 1

            # print the result in the end of each storm section
            if 0 == current_line_count:
                print_storm_detail(storm_dict)

                # if result_list has current year then add it; if not, pass it
                current_year = storm_dict["startDate"][0:4]

                # if the yearly data existed, add it
                # if not, create this yearly storm data
                max_sustained_wind = int(storm_dict["maxSustainedWind"])
                if current_year in result_dict:
                    current_year_storm_data_arr = result_dict[current_year]

                    # number of storm within the same year + 1
                    current_year_storm_data_arr[1] += 1
                    catogorize_storm_by_wind_speed(current_year_storm_data_arr, max_sustained_wind)

                else:
                    new_yearly_arr = [current_year, 1, 0, 0, 0, 0, 0]
                    catogorize_storm_by_wind_speed(new_yearly_arr, max_sustained_wind)
                    result_dict[current_year] = new_yearly_arr

                storm_dict = reset_storm_dict()


def print_storm_detail(storm_dict):
    """
    Print each storm detail on the console

    :param storm_dict:  a customized dictionary for memorize the necessary storm data,
    storm_dict details is elaborated in the "reset_storm_dict" function
    :return: None
    """
    print("------------------------------------------------------------------------------------")
    # print(storm_dict) # for debug
    print("The ID of the storm is ", storm_dict["stormID"])

    if storm_dict["name"] != "UNNAMED":
        print("The name of the storm is ", storm_dict["name"])
    else:
        print("The storm does not have a name")

    print_storm_date(storm_dict["startDate"], True)
    print_storm_date(storm_dict["endDate"], False)

    print("The maximum sustained wind is ", storm_dict["maxSustainedWind"], " kt")
    print("The time of maximum sustained wind is ", storm_dict["maxSustainedWind_time"])

    pressure_change = storm_dict["highestPressure"] - storm_dict["lowestPressure"]
    pressure_change = pressure_change if storm_dict["highestPressure"] >= storm_dict["lowestPressure"] else None

    if pressure_change is not None:
        print("Total pressure change is ", pressure_change, " millibars")
    else:
        print("No pressure data")

    print("The landfall happened ", storm_dict["landfallCount"], " times")


def print_storm_date(date_string, is_start_date):
    """
    Print out the date on the console with "YYYY/MM/DD" format

    :param date_string: the date string with "YYYYMMDD" format
    :param is_start_date: a boolean value identify whether the date is start date
    :return: None
    """
    date_type = "end"
    if is_start_date:
        date_type = "start"

    print("The ", date_type, " date of the storm is ", date_string[0:4], "/", date_string[4:6], "/", date_string[6:])


def calculate_pressure_change(storm_dict, current_pressure):
    """
    Assign the highest and lowest pressure to the storm dictionary in certain condition
    :param storm_dict: a customized dictionary for memorize the necessary storm data
    :param current_pressure: the pressure in one line of one storm data
    :return: None
    """
    if current_pressure != -999:
        if 0 == storm_dict["lowestPressure"]:
            storm_dict["lowestPressure"] = current_pressure
        if current_pressure > storm_dict["highestPressure"]:
            storm_dict["highestPressure"] = current_pressure
        if current_pressure < storm_dict["lowestPressure"]:
            storm_dict["lowestPressure"] = current_pressure


def reset_storm_dict():
    """
    Reset the storm dictionary to original state
    :return: a dictionary of storm-related data
    """
    storm_dict = {
        "stormID": None,
        "name": "UNNAMED",
        "startDate": None,
        "endDate": None,
        "maxSustainedWind": 0,
        "maxSustainedWind_time": None,
        "highestPressure": 0,
        "lowestPressure": 0,
        "landfallCount": 0
    }
    return storm_dict


def catogorize_storm_by_wind_speed(current_year_storm_data_arr, max_sustained_wind):
    """
    Update category of storm data based on the sustained wind speed

    :param current_year_storm_data_arr: the yearly storm data array
    :param max_sustained_wind: the maximum of the current storm
    :return: None
    """
    if 64 <= max_sustained_wind:
        current_year_storm_data_arr[2] += 1

    if 83 <= max_sustained_wind:
        current_year_storm_data_arr[3] += 1

    if 96 <= max_sustained_wind:
        current_year_storm_data_arr[4] += 1

    if 113 <= max_sustained_wind:
        current_year_storm_data_arr[5] += 1

    if 137 <= max_sustained_wind:
        current_year_storm_data_arr[6] += 1


def print_yearly_result(result_dict):
    """
    For debugging purpose
    Print the result of the storm statistics on console for the last question with the help of PrettyTable library

    :param result_dict: a dictionary which year are the key, and the value is a array of storm-related data,
    including happened year, number of storms in the year, and numbers of category in the year.

    :return: None
    """
    result_table = PrettyTable()
    result_table.field_names = ["Year", "Storms", "Cat.1", "Cat.2", "Cat.3", "Cat.4", "Cat.5"]

    for year in sorted(result_dict.keys()):
        yearly_data = result_dict[year]
        result_table.add_row(yearly_data)

    print(result_table)


def output_yearly_result(result_dict):
    """
    Output the result of the storm statistics to a .txt file for the last question with the help of PrettyTable library
    :param result_dict:
    :return: None
    """
    result_table = PrettyTable()
    result_table.field_names = ["Year", "Storms", "Cat.1", "Cat.2", "Cat.3", "Cat.4", "Cat.5"]

    for year in sorted(result_dict.keys()):
        yearly_data = result_dict[year]
        result_table.add_row(yearly_data)

    with open('Assignment_2.txt', 'w') as output_file:
        output_file.write(result_table.get_string())


"====================================================================================================================="
"MARK: Program execution"

"""
Initiate the result dictionary for output
Each yearly storm data is a single dictionary, the key is the year, and the value is a array contains the storm details
looks like this:
{
#"1851", [number of storm, number of category 1, number of category 2, number of category 3, number of category 4, number of category 5]
  "1851": ["1851", 6, 3, 1, 1, 0, 0],
}
"""
result_dict = {}

process_storm_data("hurdat2-nepac-1949-2018-122019.txt", result_dict)
process_storm_data("hurdat2-1851-2018-120319.txt", result_dict)

output_yearly_result(result_dict)
