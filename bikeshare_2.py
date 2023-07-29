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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('\nHello! My name is Jacek :) \n \nI will assist You while exploring some US bikeshare data!\n \nBut to do that I will need some information from You.\n'')
    
    
    while True:
        city = input('Would You like me to analyze data from Chicago, New York City or Washington? - ').lower()
        if city not in CITY_DATA:
            print('\nI\'m sorry but You entered incorrect city name. Let\'s try again :)\n')
        else:
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = input('\nWhich month from January to June You would like me to analyze for You? \nPlease type "all" if I should analyze all months together! - ').lower()
        if (month not in months) and (month != 'all'):
            print('\nYou entered incorrect month name. Let\'s try again :)')
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input('\nWhich day of the week You would like me to analyze for You? \nPlease type Monday to Sunday, or "all" if I should analyze all days of the week! - ').lower()
        if (day not in days) and (day != 'all'):
            print('\nYou entered incorrect day of the week. Let\'s try again :)')
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

    # load the data into dataframe
    df=pd.read_csv(CITY_DATA[city])

    # convert date columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # creating new columns with month and day of the week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #filter by day if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nNow I am calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_popular_month = df['month'].mode()[0]
    print('Most Popular Month:', most_popular_month)

    # display the most common day of week
    most_popular_day = df['day_of_week'].mode()[0]
    print('Most Popular day:', most_popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print('Most Popular Hour:', most_popular_hour)

    print("\nThis took me %s seconds to prepare it for You." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nNow I am calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most popular start station:', Start_Station)

    # display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost popular end station:', End_Station)

    # display most frequent combination of start station and end station trip
    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print('\nMost popular combination of start station and end station trip:', Start_Station, " & ", End_Station)

    print("\nThis took me %s seconds to prepare it for You." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nNow I am calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', round(Total_Travel_Time/86400, 2), " Days")

    # display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', round(Mean_Travel_Time/60, 2), " Minutes")

    print("\nThis took me %s seconds to prepare it for You." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nNow I am calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    except KeyError:
        print("\nGender Types:\nNo data available for this month.")

    # Display earliest, most recent, and most common year of birth
    try:
        Earliest_Year = int(df['Birth Year'].min())
        print('\nEarliest Year:', Earliest_Year)
    except KeyError:
        print("\nEarliest Year:\nNo data available for this month.")

    try:
        Most_Recent_Year = int(df['Birth Year'].max())
        print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
        print("\nMost Recent Year:\nNo data available for this month.")

    try:
        Most_Common_Year = int(df['Birth Year'].value_counts().idxmax())
        print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
        print("\nMost Common Year:\nNo data available for this month.")

    print("\nThis took me %s seconds to prepare it for You." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df):
    """
    Loads and display data according to user input
    Args:
        df - Dataframe containing data filtered from function load_data()
    """
    view_data = input('\nWould You like me to display 5 first rows of individual trip data? Enter YES or NO\n').lower()
    start_loc = 0
    while True:
        if view_data == 'no':
            break
        print(df[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("\nWould You like to see next 5 rows of data?: - ").lower()
                    

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
            break

            
if __name__ == "__main__":
    main()