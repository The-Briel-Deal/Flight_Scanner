import pandas


class DataManager:
    def __init__(self):
        self.df = pandas.read_csv('location.csv')

    def return_df(self):
        return self.df