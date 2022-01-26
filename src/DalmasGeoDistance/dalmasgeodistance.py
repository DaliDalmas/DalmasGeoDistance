import math
import pandas as pd
import logging

class DalmasGeoDistance:
    def __init__(self, origin):
        self.origin = origin
        
    def __repr__(self):
        return repr(f'DalmasGeoDistance with origin at {self.origin }')

    def distance(self, destination):
        lat1, lon1 = self.origin
        lat2, lon2 = destination
        radius = 6371  # km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        return d

    def evaluate(self, df, lat_column=None ,lon_column=None, measure='km'):
        
        if isinstance(df, pd.DataFrame):
            if (lat_column is not None)&(lon_column is not None):
                temp_df = df[[lat_column ,lon_column]]
                points_list = list(temp_df.itertuples(index=False, name=None))
            else:
                raise Exception("""You need to provide column names for 
                                    latitude as lat_column and for longitude 
                                    as lon_column""")
                
        elif isinstance(df, list):
            if df[0][0]&df[0][1]:
                points_list = df
            else:
                raise Exception("""Your list need to have tuples of geopoints 
                                    like (latitude, longitude)""")
                
        distances = [self.distance(i) for i in points_list]
        
        if measure=='km':
            logging.warning("""Returning distances in kilometers you can 
                                change to miles by passing measure='miles' in evaluate""")
            return distances
        elif measure=='miles':
            logging.warning("""Returning distances in miles you can change to kilometres 
                                by passing measure='km' in evaluate""")
            return [i*0.621371 for i in distances]
        else:
            raise Exception("The measure can either be km or miles")