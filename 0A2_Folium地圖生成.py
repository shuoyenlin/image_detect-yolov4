# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 13:29:55 2022

@author: 06006637
"""

import folium



local = [24.115, 120.42436] ##輸入經緯度座標

m = folium.Map(location=local, width=600, height=600, zoom_start=15)  ##繪製地圖

folium.Circle(radius=50, location=local,color='crimson',fill=True,).add_to(m)   ##加入座標標記標記

m.save('testMap.html')   ###地圖僅能儲存html檔

