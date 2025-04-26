import pandas as pd

data = pd.read_csv('transits_all.csv')

conv_data = []

columns = ['planet', 'transit_epoch', 'period']

print(data)
print(data.values)
# print(data[data['ID'] == 'OGLE-TR-1001'])

for i in range(len(data)):
    conv_data.append([data.iloc[i]['ID'], float(data.iloc[i]['tc_0'])-2450000, float(data.iloc[i]['Period_0'])])
    
df = pd.DataFrame(columns=columns, data=conv_data)
    
df.to_csv('star_period_and_transit_time.csv', index=False)