# -*- coding: utf-8 -*-
import requests
import pandas as pd
import datetime
import dataiku
import dataikuapi

client = dataiku.api_client()
project = client.get_project(dataiku.default_project_key())

for i in range(len(list(((project.get_variables()['standard'])['Normal']).keys()))):
    url=list(((project.get_variables()['standard'])['Normal']).values())[i]
    req=requests.get(url)
    resp=req.content
    data = resp.decode('utf-8').splitlines()

    df = pd.DataFrame(data, columns =['ALL'])
    new_header = df.iloc[0]
    df = df[1:] 
    df.columns = new_header

    string=list(df.columns)[0]
    string=string.split(',')

    for j in range(len(string)):
        df[string] = df[str(list(df.columns)[0])].str.split(',', expand=True)
        
    del df[list(df.columns)[0]]

    temp = dataiku.Dataset(list(((project.get_variables()['standard'])['Normal']).keys())[i])
    temp.write_with_schema(df)

