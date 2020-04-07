import pandas as pd
import numpy as np
import re
import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_profiling as pp
import folium
import json

# geo_path = 'C:/Users/KIMDOHWAN/PycharmProjects/data/HangJeongDong_ver20200401.geojson'
# geo_str = json.load(open(geo_path, encoding='utf-8'))
# geo_str_seoul = {}
# place_list = []
# for k,v in geo_str.items():
#     geo_str_seoul[k] = v
#     if k=='features':
#         for feature in v:
#             if '서울' in feature['properties']['adm_nm']:
#                 city,gu,dong = feature['properties']['adm_nm'].split(' ')
#                 feature['properties']['gu'] = gu
#                 feature['properties']['dong'] = dong
#                 place_list.append(feature)
#         geo_str_seoul[k] = place_list
# with open('../data/seoul_map.geojson', "w", encoding='utf-8') as json_file:
#     json.dump(geo_str_seoul, json_file, indent=4, ensure_ascii=False)


geo_path = 'C:/Users/KIMDOHWAN/PycharmProjects/data/seoul_map.geojson'
geo_str = json.load(open(geo_path, encoding='utf-8'))
geo_str_ypmp = {}
place_list = []
for k,v in geo_str.items():
    geo_str_ypmp[k] = v
    if k=='features':
        for feature in v:
            if '영등포' in feature['properties']['adm_nm'] or '마포' in feature['properties']['adm_nm']:
                city,gu,dong = feature['properties']['adm_nm'].split(' ')
                feature['properties']['gu'] = gu
                feature['properties']['dong'] = dong
                place_list.append(feature)
        geo_str_ypmp[k] = place_list
with open('../data/seoul_yp_mp_map.geojson', "w", encoding='utf-8') as json_file:
    json.dump(geo_str_ypmp, json_file, indent=4, ensure_ascii=False)