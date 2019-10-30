import pandas as pd
import time



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
DAYS = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')


def user_input_check(data_type, check_list):
    """
    Function to check user input validity
    :param data_type - str place holder to check user input for city, month or day
    :param check_list: List of items the user input needs to be validated against
    Returns:
        Valid user input to the get_filters function if not reruns the function until
        a valid option is given.

    """
    user_input = input("Please enter the {} to analyze data: ".format(data_type))
    if user_input.lower() in check_list:
        user_input = user_input.lower()
        return user_input
    else:
        print ("Invalid {} name please make sure the {} entered is in "
               "the list {}".format(data_type, data_type, check_list))
        user_input_check(data_type, check_list)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = user_input_check('city', list(CITY_DATA.keys()))

        # get user input for month (all, january, february, ... , june)
        month = user_input_check('month', MONTHS)

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = user_input_check('day', DAYS)
        break

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
    try:
        df = pd.read_csv(CITY_DATA[city])

        # Covert 'Start Time' Column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Extract the month, day  and hour of the week from Start Time to create new columns
        df['Month'] = df['Start Time'].dt.month_name()
        df['Day'] = df['Start Time'].dt.weekday_name
        df['Hour'] = df['Start Time'].dt.hour

        if month == 'all':
            if day != 'all':
                # Filter by day if user wants to analyze data for all months on a particular day
                df = df[df['Day'] == day.title()]
        else:
            df = df[df['Month'] == month.title()]
            if day == 'all':
                # Filter by month if user wants to analyze data for all days for a particular month
                pass
            else:
                # Filter by day  and month user wants to analyze data
                df = df[df['Day'] == day.title()]
    except:
        # Print Error if you are unable to read a file
        print("Error: Unable to open {} file".format(CITY_DATA[city]))
    return df


def df_validation(column, df):
    """

    :param column: column index
    :param df: dataframe filterby city, month and date options
    :return:
        :exception if column does not exist in the dataframe
    """
    if column in df:
        pass
    else:
        raise Exception("{} column does not exist".format(column))



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("\tMost common month of the year: ", df['Month'].mode()[0])

    # display the most common day of week
    print("\tMost common day of week: ", df['Day'].mode()[0])

    # display the most common start hour
    print("\tMost common hour of the day: ", df['Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try :
        df_validation('Start Station',df.columns)
        # display most commonly used start station
        print("\tMost commonly used start station: ", df['Start Station'].mode()[0])
    except Exception as e:
        print("\t",e)

    try:
        df_validation('End Station', df.columns)
        # display most commonly used end station
        print("\tMost commonly used end station: ", df['End Station'].mode()[0])
    except Exception as e:
        print("\t",e)

    # display most frequent combination of start station and end station trip
    # Creating a new combo column with Start and End time
    df['Start-End station combo'] = df['Start Station'] + ' and ' + df['End Station']
    print("\tMost commonly used combination of Start and End station: ", df['Start-End station combo'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    try:
        df_validation('End Station', df.columns)
        # display total travel time
        print("\tTotal travel time: ", df['Trip Duration'].sum())

        # display mean travel time
        print("\tTotal travel time: ", df['Trip Duration'].mean())

    except Exception as e:
        print("\t",e)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stat_out(df, stat_index):
    """

    :param df: dataframe filtered by aggregator
    :param stat_index: list of index s
    :return:
        Formatted output with index and value separated by ':'
    """
    formated_out = ''

    for i in range(0, len(stat_index)):
        formated_out += "{} - {}, ".format(stat_index[i], df[stat_index[i]])

    # Return all but the last 2 characters
    return formated_out[:-2]


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        df_validation('User Type', df.columns)
        # Display counts of user types
        user_type_count = df['User Type'].value_counts()
        print("\tCount of user type: {} in a total of {} users"
                            .format(user_stat_out(user_type_count,
                                    user_type_count.index.values),
                                    df['User Type'].count()))
    except Exception as e:
        print("\t",e)

    try:
        df_validation('Gender', df.columns)
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print("\tCount of Genders: {} in a total of {} customers"
                            .format(user_stat_out(gender_count,
                                    gender_count.index.values),
                                    df['Gender'].count()))
    except Exception as e:
        print("\t",e)

    try:
        df_validation('Gender', df.columns)
        # Display earliest, most recent, and most common year of birth
        print("\n\tEarliest Year of Birth:", int(df['Birth Year'].min()))
        print("\tMost recent Year of Birth:", int(df['Birth Year'].max()))
        print("\tMost common Year of Birth:", int(df['Birth Year'].mode()[0]))

    except Exception as e:
        print("\t",e)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_output(df, start_index):
    """

    :param df: Dataframe for printing 5 lines at time
    :param start_index: dataframe start index for rows to be printed
    print five rows of dataframe as long as the user says yes
    """
    while True:
        raw_output = input("Would you like to see 5 lines raw data for above analysis? Enter yes or no: ")
        if raw_output.lower() == 'no':
            break
        else:
            if start_index < df.shape[0]:
                end_index = start_index + 5
                # show 5 rows of the dataframe starting from the index
                print(df.iloc[start_index: end_index])
                start_index = end_index
            else:
                print("You have reached the end of the data. Output will start from beginning..")
                start_index = 0


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        start_index = 0
        raw_output(df, start_index)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
