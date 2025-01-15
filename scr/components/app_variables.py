"""Constant and variable values of the dashboard as a Dataclass."""
import dataclasses
import pandas as pd

@dataclasses.dataclass
class Values:
    year:int
    YEAR_MAX:int
    """Constant and variable values of the dashboard as a Dataclass."""
    YEAR_START:int = 1950
    #url to the data
    DATA_URL:str="https://nyc3.digitaloceanspaces.com/owid-public/data/co2/owid-co2-data.csv"
    df:pd.DataFrame = dataclasses.field(default_factory=pd.DataFrame)
    #data source
    DATA_SOURCE:str="Data source: Our world in data: "
    #data source url
    DATA_SOURCE_URL:str="https://github.com/owid/co2-data"
    #this variable change its value allong the programm
    country_iso_codes:list[str]=dataclasses.field(default_factory=list)
    #default values
    ALL_CONTINENTS:tuple[str] = ('world','africa', 'asia', 'europe', 'north america', 'south america')
    ALL_DEFAULT_ISO:tuple[str] = ("DEU","ZAF","CHN","DEU","USA","BRA")
    DEFAULT_NATION:dict[str:str] = dataclasses.field(default_factory=dict)
    #title of the subplots
    SUBPLOT_TITLE:tuple[str] = ("title1","title2","title3")
    region:str = "world"
    subplot_color_offset:int = 0

    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.df = pd.read_csv(self.DATA_URL)
        self.DEFAULT_NATION = dict(zip(self.ALL_CONTINENTS,self.ALL_DEFAULT_ISO))
        self.country_iso_codes = ["DEU"]
        self.YEAR_MAX = self.df["year"].max()
        self.year = self.YEAR_MAX

    def clear(self):
        self.country_iso_codes = []

    def add_country(self,iso_code:str)->None:
        self.country_iso_codes.append(iso_code)

    def remove_country(self,iso_code:str)->None:
        self.country_iso_codes.remove(iso_code)

    def select_country(self,iso_code:str)-> None:
        if iso_code in self.country_iso_codes:
            self.remove_country(iso_code)
        else:
            self.add_country(iso_code)

    def select_one_country(self, iso_code:str)->None:
        self.country_iso_codes = [iso_code]