"""Constant values of the dashboard"""

#first selecteable year
START_YEAR:int = 1990

#url to the data
DATA_URL:str="https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"

#data source
DATA_SOURCE:str="Data source: Our world in data: "
#data source url
DATA_SOURCE_URL:str="https://github.com/owid/co2-data"

#this variable change its value allong the programm
country_names=set([])

#default values
ALL_CONTINENTS:list[str] = ['world','africa', 'asia', 'europe', 'north america', 'south america']
ALL_DEFAULT_ISO:list[str] = ["DEU","ZAF","CHN","DEU","USA","BRA"]
DEFAULT_NATION:dict[str:str] = dict(zip(ALL_CONTINENTS,ALL_DEFAULT_ISO))

#title of the subplots
SUBPLOT_TITLE:list[str] = ["title1","title2","title3"]