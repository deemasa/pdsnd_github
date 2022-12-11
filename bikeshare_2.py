import time
import pandas as pd
import numpy as np
import json

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        str means String
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'August': 8,
              'September': 9, 'october': 10, 'november': 11, 'december': 12}

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    c = input("Would you like to see data from CHICAGO, NEW YORK CITY, OR WASHINGTON? ").lower()
    if c not in CITY_DATA.keys():
        print("Please enter a valid city name!")
        main()
    else:
        city = CITY_DATA[c]

    # get user input for month (all, january, february, ... , june)
    m = input("Enter month, january, february ... june?: (enter all for no filters): ").lower()
    if not m == 'all':
        if m == 'january' or m == 'february' or m == 'march' or m == 'april' or m == 'may' or m == 'june':
            month = months[m]
        else:
            print("Please enter valid month!")
            main()
    else:
        month = m

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter day of the week as an integer. (e.g 0 = Sunday, 1 = Monday) enter all for no filters: ")

    if day == 'all':
        pass
    else:

        if not day.isdigit():
            print("Please enter valid week day!")
            main()
        elif int(day) > 6:
            print("Please enter a valid week day! (0-6)")
            main()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city)

    # Specific Day and month
    if not month == 'all' and not day == 'all':
        df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H')
        df = df.loc[(df['Start Time'].dt.weekday == int(day)) & (df['Start Time'].dt.month == int(month))]

    # Specific Day and all months data
    elif month == 'all' and not day == 'all':
        df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H')
        df = df.loc[df['Start Time'].dt.weekday == int(day)]

    # Specific Month and all days
    elif not month == 'all' and day == 'all':
        df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H')
        df = df.loc[df['Start Time'].dt.month == int(month)]

    else:
        df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'August': 8,
              'September': 9, 'october': 10, 'november': 11, 'december': 12}
    # displays the calculating most frequent times of travel message
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    month = df['Start Time'].dt.month.value_counts().idxmax()
    month_count = df['Start Time'].dt.month.value_counts().max()
    value = [i for i in months if months[i] == month]
    print(f"Most Common Month is: {value[0]} count: {month_count}")

    # display the most common day of week
    day = df['Start Time'].dt.dayofweek.value_counts().idxmax()
    day_count = df['Start Time'].dt.dayofweek.value_counts().max()
    print(f"Most Common Day of the week is: {day}, count: {day_count}")

    # display the most common start hour
    hour = df['Start Time'].dt.hour.value_counts().idxmax()
    hour_count = df['Start Time'].dt.hour.value_counts().max()
    print(f"Most Common hour is: {hour}, Count: {hour_count} ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    station = df['Start Station'].value_counts().idxmax()
    station_count = df['Start Station'].value_counts().max()
    print(f"Most common Start Station: {station}, count: {station_count}")

    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    end_station_count = df['End Station'].value_counts().max()
    print(f"Most common End Station: {end_station}, count: {end_station_count}")

    # display most frequent combination of start station and end station trip
    start_end = df.groupby(['Start Station', 'End Station']).size().idxmax()
    start_end_count = df.groupby(['Start Station', 'End Station']).size().max()
    print(f"Most common Start Station and End Station Combination is: {start_end}, count: {start_end_count}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    # displaying the message of calculating trip duration
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    avg = df['Trip Duration'].mean()
    print(f"Total Travel time: {total}")

    # display mean travel time
    print(f"Average Travel Time {avg}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of User Types: \n")
    try:
        print(df.groupby(['User Type'])['User Type'].count())
    except:
        print("No User types data")

    # Display counts of gender
    print("Counts of gender: \n")
    try:
        print(df.groupby(['Gender'])['Gender'].count())
    except:
        print("No gender data")

    # Display earliest, most recent, and most common year of birth
    try:
        df['Birth Year'] = pd.to_datetime(df['Birth Year'], format='%Y')
        birth = df['Birth Year'].dt.year.value_counts().idxmax()
        birth_count = df['Birth Year'].dt.year.value_counts().max()
        print(f"Most Common Year of birth is: {birth}, Count: {birth_count}")
        print(f"Earliest year by birth: {df['Birth Year'].dt.year.min()}")
        print(f"Most Recent year by birth is: {df['Birth Year'].dt.year.max()}")
    except:
        print("No Birth data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """Displays raw bikeshare data."""
    # Would you like to view individual trip data (five entries)? Type 'yes' or 'no'\n"
    i = 0
    while True:
        view_data = input("Would you like to view individual trip data (five entries)? Type 'yes' or 'no'\n").lower()
        if view_data == 'yes':
            if i+5 > df.shape[0]:
                print(df.iloc[i:df.shape[0]])
                break
            print(df.iloc[i:i+5,:])
            i += 5
        elif view_data == 'no':
            break
        else:
            print("Please enter a valid input")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            exit()


if __name__ == "__main__":
    main()
