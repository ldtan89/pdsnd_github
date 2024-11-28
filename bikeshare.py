import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    # Get user input for city
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington? \n').lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please choose Chicago, New York, or Washington.")

    # Get user input for filter type
    while True:
        time_filter = input('\nWould you like to filter the data by month, day, or not at all? Type "none" for no time filter.\n').lower()
        if time_filter in ['month', 'day', 'none']:
            break
        else:
            print("Invalid input. Please choose 'month', 'day', or 'none'.")

    month = day = 'all'
    
    # Get month and day based on filter choice
    if time_filter == 'month':
        while True:
            month = input('\nWhich month? January, February, March, April, May, or June? \n').lower()
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            if month in months:
                break
            else:
                print("Invalid input. Please choose a valid month.")
    
    elif time_filter == 'day':
        while True:
            day = input('\nWhich day? Please type your response as an integer (e.g., 1=Sunday).\n')
            try:
                day = int(day)
                if 1 <= day <= 7:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 7.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    try:
        # load data file into a dataframe
        df = pd.read_csv(CITY_DATA[city])

        # convert Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])

        # extract month, day of week, and hour from Start Time
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.dayofweek + 1
        df['hour'] = df['Start Time'].dt.hour

        # filter by month if applicable
        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
            df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            df = df[df['day_of_week'] == day]

        return df

    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert Start Time column to datetime if not already
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week and hour from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print(f'Most Common Month: {months[popular_month-1].title()}')

    # Most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print(f'Most Common Day of Week: {popular_day}')

    # Most common hour
    popular_hour = df['hour'].mode()[0]
    print(f'Most Common Start Hour: {popular_hour}')

    print(f"\nThis took {(time.time() - start_time):.4f} seconds.")
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Uses groupby() and nlargest() for finding most common trip.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most common start station
    popular_start = df['Start Station'].mode()[0]
    print(f'Most common start station: {popular_start}')

    # Most common end station
    popular_end = df['End Station'].mode()[0]
    print(f'Most common end station: {popular_end}')

    # Most common trip using groupby and nlargest
    # 1. Group by both stations
    # 2. Count occurrences
    # 3. Reset index to make a DataFrame
    # 4. Use nlargest to get most frequent
    trip_counts = (df.groupby(['Start Station', 'End Station'])
                    .size()
                    .reset_index(name='count')
                    .nlargest(1, 'count'))
    
    # Get the most common trip from the result
    start = trip_counts.iloc[0]['Start Station']
    end = trip_counts.iloc[0]['End Station']
    count = trip_counts.iloc[0]['count']
    
    print(f'Most common trip: {start} -> {end}')

    print(f"\nThis took {(time.time() - start_time):.4f} seconds.")
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time


    # display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types


    # Display counts of gender


    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
