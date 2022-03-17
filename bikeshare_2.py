
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'mars', 'april', 'may', 'june']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input(
            "\nChoose a city from chicago, new york, washington: \n").lower()
        if city not in CITY_DATA:
            print("City input not valid, Please try again")
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Enter a month from the first 6 months of the year or Enter \"all\" of them\n").lower()
        if month != 'all' and month not in MONTHS:
            print("Month input not valid, Please try again")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Enter a day of the week or Enter \"all\" of them\n").lower()
        days = ['sunday', 'monday', 'tuesday',
                'wednesday', 'thursday', 'friday', 'saturday']
        if day != 'all' and day not in days:
            print("\nDay input not valid, Please try again\n")
        else:
            break

    print('-'*40)
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
    # load data file
    df = pd.read_csv(CITY_DATA[city])
    # convert Start time colum to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # get month and day of week from Start Time column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding integer
        month = MONTHS.index(month) + 1

    # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    month = df['month'].mode()[0]
    month = MONTHS[month - 1].title()
    print("The most frequent month: ", month)

    # display the most common day of week
    day = df['day_of_week'].mode()[0]
    print("The most common day : ", day)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour = df['hour'].mode()[0]
    t = time.strptime(str(hour), "%H")
    hour = time.strftime("%I %p", t)
    print("The most popular hour of traveling: ", hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common used start station: ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("Most common  end station: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("Most common trip from start to end station: ",
          (df['Start Station'] + ' to ' + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    t = time.gmtime(df['Trip Duration'].sum())
    total = time.strftime("%H : %M", t)
    print("Total travel time\n", total)
    # display mean travel time
    t2 = time.gmtime(df['Trip Duration'].mean())
    mean = time.strftime("%H : %M", t2)
    print("Mean time\n", mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display user type stats
    print("Subscribers: ", df["User Type"].value_counts()[0])
    print("Customers: ", df["User Type"].value_counts()[1])

    # display user gender and birth stats
    try:
        print("Males: ", df["Gender"].value_counts()[0])
        print("Females: ", df["Gender"].value_counts()[1])
        print("Earliest year of birth: ", int(df["Birth Year"].max()))
        print("Most recent year of birth: ", int(df["Birth Year"].min()))
        print("Most common year of birth: ", int(df["Birth Year"].mode()))
    except:
        print("Sorry gender and birth stats are only available for NYC and Chicago")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    rows = 0
    ans = input(
        "\nWould you like to view individual trip data? Enter \"yes\" or \"no\":\n").lower()
    while ans == "yes":
        print(df.iloc[rows: rows+5])
        ans = input(
            "\nWould you like to view individual trip data? Enter \"yes\" or \"no\":\n").lower()
        rows += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
