# Standard Imports
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

# Third-party Import
import pandas as pd

def get_daily_positives(df):
    # Get daily positives for cases indicator
    # Getting only daily columns with less than half null values
    df = df.loc[:, df.isnull().mean() < .5]

    # Getting only numeric columns for sum
    columns = df.columns
    daily_columns = columns[4:-2]

    daily_results = df[daily_columns]

    daily_totals = daily_results.sum()

    return daily_totals


def school_type_totals(df_final):
    columns = df_final.columns
    daily_columns = columns[3:-2]

    df_final['type'] = df_final['type'].str.strip()
    df_grouped = df_final.groupby('type')

    df_grouped_cols = df_grouped[daily_columns].sum()
    df_grouped_yesterday = df_grouped_cols.iloc[:, :-1]

    type_grouped = df_grouped_cols.sum(axis=1)

    type_grouped_yesterday = df_grouped_yesterday.sum(axis=1)

    return type_grouped, type_grouped_yesterday


def aggregated_totals(df_final):
    # Getting only daily columns with less than half null values
    df_final = df_final.loc[:, df_final.isnull().mean() < .5]

    # Getting numeric columns for tally
    columns = df_final.columns
    daily_columns = columns[4:-2]

    df_sums = df_final[daily_columns].sum()
    df_aggregated = df_sums.cumsum()

    return df_aggregated


def top_schools(df_final):
    df_final['school_fullname'] = df_final['school'] + ' ' + df_final['type']
    school_groups = df_final.groupby('school_fullname')
    school_sums = school_groups['total_positive'].sum()
    school_sums = school_sums.sort_values(ascending=False)
    top_schools = school_sums[:15].sort_values(ascending=True)

    return top_schools


def geo_data(df_final):

    # Dropping columns with more than half null values
    df_final = df_final.loc[:, df_final.isnull().mean() < .5]

    # Getting cumulative totals for chart
    columns = df_final.columns
    daily_columns = columns[4:-3]
    info_columns = columns[1:4]
    current = daily_columns[-1]

    # Saving current state as first slide, so chart begins with most recent date
    df_info = df_final[info_columns]
    # Cumulative sums for final day
    df_cumulative = df_final[daily_columns].cumsum(axis=1)
    df_info['Current'] = df_cumulative[current]

    # Merging all historical dates behind in chronological order
    df_cumulative = pd.merge(left=df_info,
                             right=df_final[daily_columns].cumsum(axis=1),
                             left_index=True,
                             right_index=True)


    # Melting dataframe for timeseries data
    df_melted = pd.melt(df_cumulative,
                        id_vars=df_cumulative.columns[0:3],
                        value_vars=df_cumulative.columns[3:])
    # Renaming melted columns
    df_melted.rename(columns={'variable': 'date',
                              'value': 'total'},
                     inplace=True)


    # Reading in school geo data
    df_locations = pd.read_csv('data/school_locations.csv')

    # Merging school geo data
    df_locations.drop(columns=df_locations.columns[0], inplace=True)
    # Splitting lat and long
    df_locations['latitude'] = df_locations['geo'].str.split(', ', expand=True)[0]
    df_locations['longitude'] = df_locations['geo'].str.split(', ', expand=True)[1]
    # Converting to float values
    df_locations['latitude'] = pd.to_numeric(df_locations['latitude'])
    df_locations['longitude'] = pd.to_numeric(df_locations['longitude'])
    # Dropping geo column
    df_locations = df_locations.drop(columns='geo')
    # Dropping Total Staff column
    df_locations.drop(columns='Total Staff & Student',
                        inplace=True)


    # Merging geo and sum data
    df_geo = pd.merge(left=df_melted,
                      right=df_locations,
                      on=['school', 'type'])

    # Reformatting school types for index
    df_geo['Category'] = df_geo['type'].str.replace('ES', 'Elementary') \
        .replace('MS', 'Middle') \
        .replace('HS', 'High')

    return df_geo
