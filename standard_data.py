
import pandas as pd

# read excel data
df = pd.read_excel("covid-19_vaccinated.xlsx", engine="openpyxl")

# get min and max value
percent_min = df.describe()['Percent'].min()
percent_max = df.describe()['Percent'].max()

fully_vaccinated_min = df.describe()['Fully vaccinated'].min()
fully_vaccinated_max = df.describe()['Fully vaccinated'].max()

# standard data
covid_19_data = list()
country_name_map = dict()
for index, data in df.iterrows():
    country = data['country']
    en_country = data['en_country']
    percent = data['Percent']
    fully_vaccinated = data['Fully vaccinated']
    # print(country, en_country, percent, fully_vaccinated)
    covid_19_data.append({'name': en_country, 'value': [percent, fully_vaccinated, en_country]})
    country_name_map[en_country] = country
# print(covid_19_data)
# print(country_name_map)
