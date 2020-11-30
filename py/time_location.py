import pandas as pd
import pickle
import numpy as np
from obspy.core import UTCDateTime

info = pd.read_table('../data/Combined_catalog_hawaii_12MAD_witht.txt',header=None)
time = pickle.load(open('../output/pkl/only_time.pkl', 'rb'))
fi = pickle.load(open('../output/pkl/fi_container.pkl', 'rb'))
labels = pickle.load(open('../output/pkl/labels_stfre.pkl', 'rb'))
Time_events = []
events_location = []
print(len(time))
for i in range(len(info)):
    One_time = ['-'.join(info.values[i][0].split(' ')[0:2]), 
                info.values[i][0].split(' ')[2],  info.values[i][0].split(' ')[3],
                info.values[i][0].split(' ')[4], info.values[i][0].split(' ')[5]]
    Time_events.append(One_time)

for i in range(len(time)):
    for j in range(len(info)):
     
        if time[i] == Time_events[j][0]:
            #计算到2018.4.30的天数
            days = (UTCDateTime(time[i]).timestamp-UTCDateTime('2018-04-30').timestamp)/86400
            location = [Time_events[j][1],Time_events[j][2],Time_events[j][3],str(fi[i]),str(days),Time_events[j][4],labels[i]]
            events_location.append(location)
            break


print(len(events_location))
pickle.dump(events_location, open('../output/pkl/events_location.pkl', 'wb'))

