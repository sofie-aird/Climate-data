"""
TODO: add a top-level comment

climate2.py
"""

from cs21_country import *

# you can import some of our lab8 solution functions to use like this:
# from cs21S24_lab08lib import binary_search

def main():

    # NOTE: you can test your code on a smaller file (small.csv) by
    #       uncommenting this line, and commenting out the one that
    #       sets filename to climatewatchdata.csv
    #filename = "small.csv"
    filename = "/usr/local/doc/climatewatchdata.csv"
    data = get_data(filename)
    print("There are %d countries in the database" % (len(data)))
    choice = menu(data)

    #print("Debug: using file %s" %(filename))
    

###########################################
# TODO: Add your functions, including copying over some from your 
#       lab 8 solution, here:

def get_data(filename):
    f = open(filename, "r")
    if (f == None):
        print("Error opening file %s" % (filename))
        return None
    file_data = f.readlines()
    f.close()
    for i in range(len(file_data)):
        file_data[i] = file_data[i].strip()
    data = create_objects(file_data)
    return data

def create_objects(lst):
    countries = []
    for i in range(len(lst)):
        country = lst[i].split(',')
        co2_vals = []
        for j in range(len(country)):
            if (j == 0):
                name = country[j]
            elif (j > 0 and j < 6):
                val = float(country[j])
                co2_vals.append(val)
            elif (j == 6):
                pop_1960 = float(country[j])
            elif (j == 7):
                pop_2020 = float(country[j])
            elif (j == 8):
                gdp_1960 = float(country[j])
            elif (j == 9):
                gdp_2020 = float(country[j])
        data = Country(name, co2_vals, pop_1960, pop_2020,\
        gdp_1960, gdp_2020)
        
        countries.append(data)
    return countries

def menu_options():
    print("""
    ================== Menu ======================
1. The n largest C02 producing countries in given year
2. The CO2 values for n countries with largest GDP in given year
3. The n largest CO2/population producing countries in a given year
4. Print a country's info
5. Quit""")

def menu(data):
    menu_options()
    choice = get_value_between("Select a menu option", 1, 5)
    while choice != 5:
        if choice == 1:
            prompt = "Pick a value for n"
            n = get_value_between(prompt, 1, 193)
            year = get_value_in_set([1960, 1980, 2000, 2020, 2022],\
            "Enter a year (one of 1960, 1980, 2000, 2020, 2022): ")
            selection_sort(data, year, choice)
            display_emissions(data, n, year)
        elif choice == 2:
            prompt = "Pick a value for n"
            n = get_value_between(prompt, 1, 193)
            year = get_value_in_set([1960, 2020],\
            "Enter a year (one of 1960 or 2020): ")
            selection_sort(data, year, choice)
            display_gdp(data, n, year)
        elif choice == 3:
            prompt = "Pick a value for n"
            n = get_value_between(prompt, 1, 193)
            year = get_value_in_set([1960, 2020],\
            "Enter a year (one of 1960 or 2020): ")
            selection_sort(data, year, choice)
            display_per(data, n, year)
        elif choice == 4:
            target = input("Enter the name of the country: ")
            index = find_country(data, target)
            if (index == -1):
                print("Sorry, %s is not in the database" % (target))
            else:
                print(data[index])
        menu_options()
        choice = get_value_between("Select a menu option", 1, 5)


def get_value_between(message, low, high):
    print(message)
    choice = int(input("Enter a value between %d and %d: " % (low, high)))
    while (choice >= high or choice < low):
        if choice == 5:
            print("bye bye")
            return choice
        print("%d is not a valid choice, please try again" % (choice))
        choice = int(input("Enter a value between %d and %d: " % (low, high)))

    return choice

def get_value_in_set(values, prompt):
    year = int(input(prompt))
    while (year not in values):
        print("%d is not a valid value, please try again" % (year))
        year = int(input(prompt))

    return year

def selection_sort(ls, year, choice):
  """
  Sorts the list ls in accending order
    ls: a list of int values
    return: no return value (modifies the list in place)
  """

  #print("DEBUG: inside selection_sort")
  for i in range(len(ls) - 1):
    idx = find_largest(ls, i, len(ls), year, choice)
    swap(ls, i, idx)

def find_largest(ls, start, stop, year, choice):
  """
  returns the index of the smallest value between
  ls[start] and ls[stop-1], inclusive
  """
  if choice == 1:
    max = ls[start].getCO2(year) # assume first element is smallest
    idx = start     # keep track of index of smallest element
    for i in range(start+1, stop):
        if ls[i].getCO2(year) > max: # if element is smaller than min...
            max = ls[i].getCO2(year)   # update the min value seen so far
            idx = i       # also update the index of the smallest value
    return idx
  elif choice == 2:
    max = ls[start].getGDP(year) # assume first element is smallest
    idx = start     # keep track of index of smallest element
    for i in range(start+1, stop):
        if ls[i].getGDP(year) > max: # if element is smaller than min...
            max = ls[i].getGDP(year)   # update the min value seen so far
            idx = i       # also update the index of the smallest value
    return idx
  elif choice == 3:
    max = ls[start].getCO2(year)/ls[start].getPopulation(year) # assume first element is smallest
    idx = start     # keep track of index of smallest element
    for i in range(start+1, stop):
        if ls[i].getCO2(year)/ls[i].getPopulation(year) > max: # if element is smaller than min...
            max = ls[i].getCO2(year)/ls[i].getPopulation(year)   # update the min value seen so far
            idx = i       # also update the index of the smallest value
    return idx

def swap(ls, i, j):
   """
   Swaps elements at index i and j in a list 
     ls : list of elements
     i, j: indicies of two values to swap in ls (int)
     return: no return value (modifies the list in place)
   """

   #print("DEBUG: inside swap %d and %d" %(i, j))

   # need a temporary variable to hold the value so we don't lose it
   tmp = ls[i]
   ls[i] = ls[j]
   ls[j] = tmp

def display_emissions(data, n, year):
    print(" %d      Emissions in Mt          Country" % (year))
    print("-------------------------------------------------------")
    for i in range(n):
        print("%-5d %-20.6f %-30s" % (i+1, data[i].getCO2(year), data[i].getName()))
    print()

def display_gdp(data, n, year):
    print("%d      CO2(Mt)           GDP(B)        Country" % (year))
    print("------------------------------------------------------------")
    for i in range(n):
        print("%-5d %-20.6f %-20.6f %-30s" % (i+1, data[i].getCO2(year), \
        data[i].getGDP(year), data[i].getName()))

def display_per(data, n, year):
    print("%d   C02(Mt)/M people     CO2(Mt)       Population(M)    Country"\
    % (year))
    print("--------------------------------------------------------------\
    --------")
    for i in range(n):
        print("%-5d %-20.6f %-20.6f %-20.6f %-30s" % (i+1, \
        data[i].getCO2(year)/data[i].getPopulation(year), data[i].getCO2(year),\
        data[i].getPopulation(year), data[i].getName()))

def find_country(countries, target):
    low = 0
    high = len(countries) - 1
    while high >= low:
        mid = (low + high) // 2
        if (countries[mid].getName() == target):
            return mid
        elif (countries[mid].getName() > target):
            high = mid - 1
        else: # lst[mid] < x
            low = mid + 1

    # made it here, didn't find it
    return -1





############
main()
