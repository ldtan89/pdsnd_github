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
    print('\nCalculating Trip Duration Stats...')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    avg_duration = df['Trip Duration'].mean()

    print(f'\nTotal travel time: {total_duration:,.2f} seconds')
    print(f'Mean travel time: {avg_duration:.2f} seconds')

    print(f'\nThis took {time.time() - start_time:.4f} seconds.')

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:')
    for user_type, count in user_types.items():
        print(f'{user_type}: {count}')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nGender Counts:')
        for gender, count in gender_counts.items():
            print(f'{gender}: {count}')
    else:
        print('\nGender data not available for this city.')

    # Display birth year stats
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print(f'\nEarliest Birth Year: {earliest}')
        print(f'Most Recent Birth Year: {most_recent}')
        print(f'Most Common Birth Year: {most_common}')
    else:
        print('\nBirth year data not available for this city.')

    print(f"\nThis took {(time.time() - start_time):.4f} seconds.")
    print('-'*40)

def display_raw_data(df):
    """
    Displays raw data upon request by the user.
    Displays 5 rows at a time and continues based on user input.
    """
    row = 0
    while True:
        view_data = input('\nWould you like to view 5 rows of raw data? Enter \'yes\' or \'no\': \n').lower()
        if view_data != 'yes':
            break
            
        # Get current chunk of data
        data_chunk = df.iloc[row:row + 5]
        
        # Display headers only for first chunk
        header = f"{' ':>8} {'Start Time':<24} {'End Time':<24} {'Trip Duration':<14} {'Start Station':<35} {'End Station':<35} {'User Type':<12} {'Gender':<8} {'Birth Year':<8}"
        print(header)
        
        # Display each row
        for _, data in data_chunk.iterrows():
            # Get the ID from first column value
            id_num = str(data.iloc[0])
            
            # Format each field
            start_time = str(data['Start Time'])
            end_time = str(data['End Time'])
            trip_duration = str(data['Trip Duration'])
            start_station = str(data['Start Station'])
            end_station = str(data['End Station'])
            user_type = str(data['User Type'])
            gender = str(data['Gender']) if 'Gender' in data else ''
            birth_year = str(data['Birth Year']) if 'Birth Year' in data else ''
            
            print(f"{id_num:>8} {start_time:<24}{end_time:<24}{trip_duration:<14}{start_station:<35}{end_station:<35}{user_type:<12}{gender:<8}{birth_year:<8}")
        
        row += 5
        if row >= len(df):
            print("\nNo more data to display!")
            break

def main():
    while True:
        # Get all three values from get_filters()
        city, month, day = get_filters()
        
        # Pass all three values to load_data()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter \'yes\' or \'no\'.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
