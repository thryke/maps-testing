import pandas as pd
import json
from rymscraper import rymscraper, RymUrl

def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)

network = rymscraper.RymNetwork()

artist_infos = network.get_artists_infos(names=["Thinking Fellers Union Local 282", "Duster", "Korea Girl", "Bladee", "Drain Gang", "Drake"])

df = pd.DataFrame(artist_infos)

formed_first_series = df['Formed'].str.split(', ', n=1)
formed_first_series = formed_first_series.to_string()
if (has_numbers(formed_first_series)):
    df[['Formed Date', 'Formed']] = df['Formed'].str.split(', ', n=1, expand=True)

df[['Formed City', 'Formed State/Province', 'Formed Country']] = df['Formed'].str.split(', ', expand=True)

born_first_series = df['Born'].str.split(', ', n=1)
born_first_series = born_first_series.to_string()
if (has_numbers(born_first_series)):
    df[['Birth Date', 'Born']] = df['Born'].str.split(', ', n=1, expand=True)

df[['Birth City', 'Birth State/Province', 'Birth Country']] = df['Born'].str.split(', ', expand=True)

df['City'] = df['Formed City'].combine_first(df['Birth City'])
df.drop(['Formed City', 'Birth City'], axis=1, inplace=True)

df['State/Province'] = df['Formed State/Province'].combine_first(df['Birth State/Province'])
df.drop(['Formed State/Province', 'Birth State/Province'], axis=1, inplace=True)

df['Country'] = df['Formed Country'].combine_first(df['Birth Country'])
df.drop(['Formed Country', 'Birth Country'], axis=1, inplace=True)

df2 = df['Genres'].str.split(', ', expand=True)
df2.columns = ['Genre 1', 'Genre 2', 'Genre 3', 'Genre 4', 'Genre 5', 'Genre 6']

df = df.join(df2)

csv = df.to_csv('test.csv')
