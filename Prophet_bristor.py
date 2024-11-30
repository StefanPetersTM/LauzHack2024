import BRISTOR

from prophet import Prophet
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



### Loading
bristor_df = BRISTOR.load_bristor_into_df("/home/stefan/Downloads/files/BRISTOR_Zegoland.xlsx")


### hardcoding signals
ds = pd.date_range(start="2020-08-01", end="2024-10-01", freq="M"),


bristor_new_patients = bristor_df[3][:44].set_index('Date')['Value'].rename('bristor_new_patients')
competitors_new_patients = bristor_df[3][44:87].set_index('Date')['Value'].rename('competitors_new_patients')
bristor_emails = bristor_df[4][:51].set_index('Date')['Value'].rename('bristor_emails')
bristor_call = bristor_df[4][51:].set_index('Date')['Value'].rename('bristor_call')
bristor_share_of_voice = bristor_df[5][:40].set_index('Date')['Value'].rename('bristor_share_of_voice')
competitors_share_of_voice = bristor_df[5][40:80].set_index('Date')['Value'].rename('competitors_share_of_voice')
bristor_factory_volumes = bristor_df[0].set_index('Date')['Value'].rename('bristor_factory_volumes')
bristor_demand_volumes = bristor_df[2][:46].set_index('Date')['Value'].rename('y') # bristor_demand_volumes
competitors_demand_volumes = bristor_df[2][46:92].set_index('Date')['Value'].rename('competitors_demand_volumes')


df = bristor_demand_volumes.to_frame().join(competitors_new_patients, how='outer').join(bristor_emails, how='outer').join(bristor_call, how='outer').join(bristor_share_of_voice, how='outer').join(competitors_share_of_voice, how='outer').join(bristor_factory_volumes, how='outer').join(bristor_new_patients, how='outer').join(competitors_demand_volumes, how='outer').reset_index().rename(columns={'Date': 'ds'})


### TODO check if this makes sense
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')


#df = df.fillna(0)

model = Prophet() # TODO tweak parameters
model.add_regressor('competitors_new_patients')
model.add_regressor('bristor_emails')
model.add_regressor('bristor_call')
model.add_regressor('competitors_share_of_voice')
model.add_regressor('bristor_share_of_voice')
model.add_regressor('bristor_factory_volumes')
model.add_regressor('bristor_new_patients')
#model.add_regressor('competitor_demand_volumes')
model.add_regressor('competitors_demand_volumes')
#model.add_regressor('bristor_demand_volumes')



# Fit the model
model.fit(df)
# If a competitor releases a

# Create future DataFrame
future = model.make_future_dataframe(periods=12, freq="M")  # Forecast for next 12 months
future['competitors_new_patients'] = df['competitors_new_patients']
future['bristor_emails'] = df['bristor_emails']
future['bristor_call'] = df['bristor_call']
future['competitors_share_of_voice'] = df['competitors_share_of_voice']
future['bristor_share_of_voice'] = df['bristor_share_of_voice']
future['bristor_factory_volumes'] = df['bristor_factory_volumes']
future['bristor_new_patients'] = df['bristor_new_patients']
future['competitors_demand_volumes'] = df['competitors_demand_volumes']


event_start = pd.to_datetime("2025-04-01")
impact = 0.9 # 10% reduction in demand
# Adjust SoV for competitor impact
for i, date in enumerate(future['ds']): # TODO fix the share of voice
    if date >= event_start:
        future.loc[i, 'bristor_share_of_voice'] *= impact  # Reduce SoV by 10%


# Make predictions
forecast = model.predict(future)


### CORRELATION MATRIX


regressor_names_historic_data = ['competitors_new_patients', 'bristor_emails', 'bristor_call', 'competitors_share_of_voice', 'bristor_share_of_voice', 'bristor_factory_volumes', 'bristor_new_patients', 'competitors_demand_volumes']
# Correlation heatmap
correlation_matrix = df[regressor_names_historic_data].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()