# Standard libraries
import json
from functools import reduce
import re

# Third-party libraries
from bs4 import BeautifulSoup
import bs4 as bs
import requests
import pandas as pd
import numpy as np
import datetime as dt

url = "https://www.forsyth.k12.ga.us/Page/52982"

today_date = dt.date.today()


def get_urls(url):
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text
    # Parse the html content
    soup = BeautifulSoup(html_content, "html.parser")

    # Getting weekly number lists
    covid_links = []
    for link in soup.find_all("a"):
        if str(link.text).lower().find('week ') != -1:
            # replacing https with http and getting link url
            covid_links.append(str(link['href']).replace('s', '', 1))
        else:
            pass

    return covid_links


def get_weekly_info(url):
    source = requests.get(url).text
    soup = bs.BeautifulSoup(source, 'html.parser')

    # finding hidData element
    token = soup.find_all('input', id=lambda x: x and x.startswith('hidData'))
    # getting 'value' from inside tag
    info = [x.get('value') for x in token][0]

    return info


def remove_html_tags(text):

    # Removing HTML Tag using regex
    pattern = re.compile('<.*?>')
    clean = re.sub(pattern, '', text)

    return clean

def info_dataframe(info):

    # Removing html tags
    info = remove_html_tags(info)

    # Replacing data for Alliance Academy
    info = info.replace('Innovation', 'Innovation HS')

    # Reading info as json string
    info_json = json.loads(info)

    # Removing headers
    headers = info_json.pop(0)

    # Reading into dataframe
    df = pd.DataFrame(info_json, columns=headers)

    return df


def clean_df(df):
    # Removing , fron numbers, replacing o with 0 and converting to numeric values
    columns = df.columns
    for col in columns[1:]:
        df[col] = df[col].str.replace('o', '0')
        df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')

    # Handling change in column naming for week 3
    if "Total Staff & Student" in columns:
        df.drop(columns=['Total Staff & Student'], inplace=True)
    else:
        pass

    # Replacing none values with nulls
    df.replace(to_replace=['None'], value=np.nan, inplace=True)

    # Splitting school name into name and category
    split_names = df['School Name'].str.rsplit(' ', 1, expand=True)
    # Creating columns for name and category
    df['school'] = split_names[0]
    df['type'] = split_names[1]

    # Dropping rows with nulls
    df.dropna(subset=['type'], inplace=True)

    # Final cleaning and ordering of columns
    df.drop(['School Name'], axis=1, inplace=True)
    cols = df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    df = df[cols]

    return df


def get_weekly_dataframes(master_url):
    # Getting weekly links
    url_links = get_urls(master_url)

    # Getting dataframe for each week
    df_list = []
    for url in url_links:
        info = get_weekly_info(url)
        df = info_dataframe(info)
        df = clean_df(df)
        df_list.append(df)

    return df_list

def remove_duplicates(df_list):
    # Keeping F2F column in one df only
    counter = 0
    for df in df_list:
        if 'F2F Students & Staff' not in df.columns:
            pass

        else:
            if counter == 0:
                counter +=1
                pass
            else:
                df.drop(columns=['F2F Students & Staff'], inplace=True)

    return df_list

def add_transportation(df):
    # Adding row for Transporation Staff
    if 'Transportation' in [x for x in df['school']]:
        return df
    else:
        df = df.append({'school': 'Transportation',
                        'type': 'Staff'}, ignore_index=True)
        return df

def merge_dataframes(df_list):

    # Adding transportation rows
    df_list = [add_transportation(x) for x in df_list]

    # Keeping F2F column in one df only
    df_list = remove_duplicates(df_list)

    df_final = reduce(lambda x, y: pd.merge(
        x, y, on=['school', 'type']), df_list)

    return df_final


def get_covid_data(url):
    df_list = get_weekly_dataframes(url)
    df_final = merge_dataframes(df_list)
    for df in df_list:
        print("Dataframe columns: ", df.columns)

    # Organizing columns for statistical analysis
    df_columns = list(df_final.columns)

    # Repositioning 'F2F Students & Staff'
    df_columns.remove('F2F Students & Staff')
    df_columns.insert(2, 'F2F Students & Staff')
    df_final = df_final[df_columns]

    # Slicing only numerical columns
    df_columns = df_columns[3:]

    # Adding sum column
    df_final['total_positive'] = df_final[df_columns].sum(axis=1)
    df_final['percent_positive'] = (df_final['total_positive'] / df_final['F2F Students & Staff']) * 100

    # Cleaning type data
    df_final['type'] = df_final['type'].str.strip()

    # Dropping TOTAL row
    df_final = df_final[df_final['school'] != 'TOTAL']

    return df_final

def data_download():
    df_final = get_covid_data("https://www.forsyth.k12.ga.us/Page/52982")
    df_final.to_csv('forsythk12_covid_data.csv')
    return df_final

# if __name__=="__main__":
#     df_final = get_covid_data("https://www.forsyth.k12.ga.us/Page/52982")
#     df_final.to_csv('forsythk12_covid_data.csv')
#     total_positive = df_final['total_positive'].sum()
#     print(f"Total Positive Cases as of {today_date}: ", total_positive)
#     print(df_final.head())
#     print(df_final.columns)
