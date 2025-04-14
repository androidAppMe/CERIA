# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:21:24 2024

@author: marys
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:39:15 2024

@author: marys
After this we run the jupyter code (that would be number 6)
"""

import pandas as pd
from NextLevel import NextLevelGraph
from graph_source_target import myGraphPng
from networkX_from_source_target import NetworkXHtml

event="supplier bankruptcy"
data = pd.read_csv("YOUR PATH"+ event +"/"+ event +"/graph-"+event+".csv", encoding = "ISO-8859-1")

NetworkXHtml(data, event)
# 1
# 1, 2, 3, 4, 13, 14, 19, 20, 25, 32, 46, 49
# 3 khali    1, 2, 8, 13
# 2, 3, 5
# 1
# khali
# 1
# 11
# 1, 3, 5, 6
# 1, 2, 3, 4
# 2
# khali
#decrease in supply (low supply)
#4
#2, 7
#1, 2, 4, 5, 6, 8, 10, 11, 14, 15, 17, 19
#1, 2, 3, 4, 5, 6, 8, 9, 12
#1, 2, 3, 4, 5, 6, 7, 8, 9
