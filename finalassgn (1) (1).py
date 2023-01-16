"""This program analyzes data
"""
import csv
from enum import Enum

filename = './purple_air.csv'

class Stats(Enum):
    MIN = 0
    AVG = 1
    MAX = 2


class EmptyDatasetErrorException(Exception):
    pass


class NoMatchingItemsException(Exception):
    pass


class DataSet:
    def __init__(self, header=""):
        self.header = header
        self._data = None
        self._zips = {}
        self._times = []

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header: str):
        if len(header) <= 30:
            self._header = header
        else:
            raise ValueError
            
    def load_file(self):
        """ Load date from file and assign to self._data """
        file = open(filename, 'r', newline='')
        csvreader = csv.reader(file)
        next(csvreader)
        self._data = [(row[1], row[4], float(row[5])) for row in csvreader]
        #print(self._data)
        file.close()
        print(len(self._data), " lines loaded")
        self._initialize_labels()
        return len(self._data)

    def get_zips(self):
        zips_copy = self._zips.copy()
        return zips_copy

    def toggle_zip(self, target_zip: str):
        """ Toggles passed zipcode status """
        if target_zip in self._zips:
            self._zips[target_zip] = "True" if self._zips[target_zip] == \
                                               "False" else "False"
        else:
            raise LookupError

    def display_cross_table(self, stat: Stats):
        """ Given a stat from DataSet.Stats, produce a table that
        shows the value of that stat for every pair of labels from the
        two categories.
        """
        filtered_dict = []
        for item in self._zips:
            if self._zips[item] == "True":
                filtered_dict.append(item)

        if not self._data:
            print("Please load a dataset first")
            return
        print()
        print(f"{' ':7}", end="")
        for item in self._times:
            print(f"{item:>8}", end="")
        print()
        for item_one in filtered_dict:
            print(f"{item_one:<7}", end="")
            for item_two in self._times:
                try:
                    value = self._cross_table_statistics(item_one,
                                                         item_two)[stat.value]
                    print(f"{value:>8.2f}", end="")
                except NoMatchingItemsException:
                    print(f"{'N/A':>8}", end="")
            print()

    def _initialize_labels(self):
        """Initialize the _zips and _times lists"""
        times_of_day_set = set()
        self._zips = {}
        for item in self._data:
            times_of_day_set.add(item[1])
            self._zips[item[0]] = "True"
        self._times = list(times_of_day_set)

    def _cross_table_statistics(self, descriptor_one: str,
                                descriptor_two: str):
        """Check if ZipCode and Time of Day are correct to store
            Concentration
             """
        if self._data is None:
            raise EmptyDatasetErrorException
        concentration_list = [item[2] for item
                              in self._data if
                              descriptor_one == item[0] and descriptor_two ==
                              item[1]]
        if len(concentration_list) == 0:
            raise NoMatchingItemsException
        return min(concentration_list), (
                sum(concentration_list) / len(concentration_list)), max(
            concentration_list)

    def load_default_data(self):
        """Store table data in self._data"""
        self._data = [("12345", "Morning", 1.1),
                      ("94022", "Morning", 2.2),
                      ("94040", "Morning", 3.0),
                      ("94022", "Midday", 1.0),
                      ("94040", "Morning", 1.0),
                      ("94022", "Evening", 3.2)]
        self._initialize_labels()


def manage_filters(my_dataset: DataSet):
    """ Prints and allows the user to change zipcode status """
    if len(my_dataset.get_zips()) == 0:
        print("Please load a dataset first")
        return

    print("The following labels are in the dataset: ")
    zips_code_list = []
    for i, (zip_code, status) in enumerate(my_dataset.get_zips().items()):
        zips_code_list.append(zip_code)
        conditional = "INACTIVE" if status == "False" else "ACTIVE"
        print(f"{i + 1}: {zip_code:7} {conditional}")

    while True:
        user_choice = input("Please select an item to toggle or press"
                            " enter/return when you are finished.")
        if user_choice == "":
            return
        try:
            user_choice = int(user_choice)
        except ValueError:
            print("Please enter a number or enter/return to exit")
            continue
        if (user_choice < 1) or (user_choice > len(zips_code_list)):
            print("Please enter a number from the list")
            continue

        my_dataset.toggle_zip(zips_code_list[user_choice - 1])
        for i, (zip_code, status) in enumerate(my_dataset.get_zips().items()):
            conditional = "INACTIVE" if status == "False" else "ACTIVE"
            print(f"{i + 1}: {zip_code:7} {conditional}")


def print_menu():
    """Offer options to the user"""
    print("Main Menu")
    print("1 - Print Average Particulate Concentration by Zip Code and Time")
    print("2 - Print Minimum Particulate Concentration by Zip Code and Time")
    print("3 - Print Maximum Particulate Concentration by Zip Code and Time")
    print("4 - Adjust Zip Code Filters")
    print("5 - Load Data")
    print("9 - Quit")


def menu(my_dataset: DataSet):
    """Take valid input from the user and give appropriate response"""
    while True:
        print("")
        print(my_dataset.header)
        print_menu()
        user_choice = input("What is your choice? ")
        try:
            user_choice = int(user_choice)
        except ValueError:
            print("Please enter a number only")
            continue
        if user_choice == 9:
            print("Goodbye! Thank you for using the database")
            break
        elif 0 < user_choice < 6:
            if user_choice == 1:
                my_dataset.display_cross_table(Stats.AVG)
            if user_choice == 2:
                my_dataset.display_cross_table(Stats.MIN)
            if user_choice == 3:
                my_dataset.display_cross_table(Stats.MAX)
            if user_choice == 4:
                manage_filters(my_dataset)
            if user_choice == 5:
                #my_dataset.load_default_data()
                my_dataset.load_file()
        else:
            print("That's not a valid selection")


def main():
    """Obtain the user's name and print the message."""
    user_name = input("Please enter your name: ")
    print("Hi " + user_name + ", welcome to the Air Quality database.")
    purple_air = DataSet()
    while True:
        try:
            user_header = input("Enter a header for the menu: ")
            purple_air.header = user_header
            break
        except ValueError:
            print("Header must be a string less or equal to than thirty "
                  "characters long")

    menu(purple_air)


if __name__ == "__main__":
    main()
#  unit_test()


r"""
Please enter your name: Eric
Hi Eric, welcome to the Air Quality database.
Enter a header for the menu: Data for a cleaner world

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 1
Please load a dataset first

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 5
6147  lines loaded

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 1

        Morning Evening  Midday   Night
94028      1.54    2.26    2.92    1.58
94304      1.36    1.17    2.89    1.23
94022      1.50    1.22    2.92    1.32
94024      1.71    3.42    3.27    1.69
94040      1.86    4.57    3.28    2.47
94087      2.24    4.77    3.92    2.31
94041      2.41    4.53    3.52    3.43
95014      1.06    2.38    3.29    2.19

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 2

        Morning Evening  Midday   Night
94028      0.00    0.00    0.00    0.00
94304      0.00    0.00    0.00    0.00
94022      0.00    0.00    0.00    0.00
94024      0.00    0.00    0.00    0.00
94040      0.00    0.00    0.00    0.00
94087      0.00    0.00    0.00    0.00
94041      0.00    0.00    0.00    0.00
95014      0.00    0.00    0.00    0.00

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 3

        Morning Evening  Midday   Night
94028     25.72   79.88   24.21   25.00
94304      9.66    9.73   20.93    9.92
94022     12.90   11.53   26.59   14.38
94024     15.12   37.57   29.17    9.67
94040     10.49   44.05   25.95   20.34
94087      9.39   38.11   26.48   13.14
94041      8.02   31.82   25.89   19.67
95014      9.95   69.05   25.00   37.82

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 4
The following labels are in the dataset: 
1: 94028   ACTIVE
2: 94304   ACTIVE
3: 94022   ACTIVE
4: 94024   ACTIVE
5: 94040   ACTIVE
6: 94087   ACTIVE
7: 94041   ACTIVE
8: 95014   ACTIVE
Please select an item to toggle or press enter/return when you are finished.8
1: 94028   ACTIVE
2: 94304   ACTIVE
3: 94022   ACTIVE
4: 94024   ACTIVE
5: 94040   ACTIVE
6: 94087   ACTIVE
7: 94041   ACTIVE
8: 95014   INACTIVE
Please select an item to toggle or press enter/return when you are finished.

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 3

        Morning Evening  Midday   Night
94028     25.72   79.88   24.21   25.00
94304      9.66    9.73   20.93    9.92
94022     12.90   11.53   26.59   14.38
94024     15.12   37.57   29.17    9.67
94040     10.49   44.05   25.95   20.34
94087      9.39   38.11   26.48   13.14
94041      8.02   31.82   25.89   19.67

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 9
Goodbye! Thank you for using the database
"""
