#%%

import numpy as np
import pandas as pd
import requests
import json



class FDA_query(object):
    """
    Class to query the FDA API
    """
    def __init__(self, DB_Name, API_key):
        """
        DB names are either Label or NDC for labeling information or NDC for NDC information

        """
        self.DB_Name = DB_Name.upper()
        self.APIkey = r"api_key="+str(API_key)
        
        if self.DB_Name == "LABEL":
            self.url_root = r"https://api.fda.gov/drug/label.json?"
        elif self.DB_Name == "NDC":
            self.url_root = r"https://api.fda.gov/drug/ndc.json?"

    def set_API_Key(self, new_API_key):
        self.APIkey = new_API_key
    
    ###############################################
    # Define qurey parameters from the API
    def build_query(self, **kwargs):
        """
        Query parameter Common options are (API requires exact match):
        brand_name, active_ingredients, package_ndc, route
        
        input must be exact as the API requires above
        
        inclue n_limit and skip parameters to limit the number of results
        
        ##ALL **kwargs must be entered as strings##
        """
        # Define the query parameters
        query_params = {k: v for k,v in kwargs.items()}
        
        #handle limit and skip parameters
        try:
            n_lim = query_params.pop("n_limit")
            lim = "&limit=" + str(n_lim)
        except KeyError:
            lim = ""
        try:    
            n_skip = query_params.pop("skip")
            skip = "&skip=" + str(n_skip)
        except KeyError:
            skip = ""

        active_label = {"LABEL":"openfda.substance_name",
                        "NDC":"active_ingredients.name"}
        
        # handle API name
        if "active_ingredients" in query_params:
            query_params[active_label[self.DB_Name]] = query_params.pop("active_ingredients")

            
        #build search string
        if len(query_params) > 1:
            search_term = "+AND+".join([":".join([k, v]) for k,v in query_params.items()])
        else:
            search_term = ":".join(list(query_params.items())[0])
            
        # return query parameters

        return "{}{}&search={}{}{}".format(self.url_root, self.APIkey, search_term, lim, skip)
    
    
    def get_data(self, n_lim = 1000, n_skip = 0,**query_params):
        """
        Return the data from the API
        Default limit is 1000 and skip is 0
        
        Return a list of dictionaries with the data for a giben query
        """
        query_params_DICT = {k: v for k,v in query_params.items()}

        json_objs = []
        
        while True:
            try:
                query_params_DICT["n_limit"] = str(n_lim)
                query_params_DICT["skip"] = str(n_skip)
                query = self.build_query(**query_params_DICT)
                data = requests.get(query).json()["results"]
                json_objs.extend(data)
                
                n_skip += n_lim
                
            except:
                print("Done")
                break
            
        
        return json_objs
    
    #helper functions to count the number of nested dictionaries
 
        
    def get_keys(self, json_obj):
        """
        Return a list of possible column names for a given json object
        """
        def recursive_items(dictionary):
            for key, value in dictionary.items():
                if type(value) is dict:
                    yield from recursive_items(value)
                else:
                    yield (key, value)
        try:            
            return [key for key, value in recursive_items(json_obj)]
        except:
            print("check Input object has to be in JSON or dictionary format")

    
    def set_col_names(self, col_names):
        """
        Enter interested column names as 1 string, separated by commas or a list or a  string
        
        """
        if type(col_names) == str:
            self.col_names = col_names.split(",")
        elif type(col_names) == list:
            self.col_names = col_names
        else:
            print("Column names must be a string or a list")
            return
        
        
        
    def get_col_names(self):
        """
        Return the chosen column names
        To be worked on in the future if needed
        
        """
        return self.col_names
    
    def build_dt(self, json_obj):
        """
        Build a dataframe from a list of json objects
        To be worked on in the future if needed
        
        """
        
        pass
        
        

        
        
# %%
