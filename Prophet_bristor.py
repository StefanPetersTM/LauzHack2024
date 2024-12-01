import BRISTOR

from prophet import Prophet
import pandas as pd

def forecast_regressor(future_df, regressor_column,df):
    regressor_model = Prophet()

    regressor_model.fit(df[['ds', regressor_column]].rename(columns={regressor_column:'y'}))

    future_regressor = regressor_model.predict(future_df[['ds']])

    return future_regressor[['ds', 'yhat']]


def get_past_df():
    ### Loading
    bristor_df = BRISTOR.load_bristor_into_df("/home/samsung/Desktop/BMS/BRISTOR_Zegoland.xlsx")

    ### hardcoding signals
    ds = pd.date_range(start="2020-08-01", end="2024-10-01", freq="M"),

    bristor_new_patients = bristor_df[3][:44].set_index('Date')['Value'].rename('bristor_new_patients')
    competitors_new_patients = bristor_df[3][44:87].set_index('Date')['Value'].rename('competitors_new_patients')
    bristor_emails = bristor_df[4][:51].set_index('Date')['Value'].rename('bristor_emails')
    bristor_call = bristor_df[4][51:].set_index('Date')['Value'].rename('bristor_call')
    bristor_share_of_voice = bristor_df[5][:40].set_index('Date')['Value'].rename('bristor_share_of_voice')
    competitors_share_of_voice = bristor_df[5][40:80].set_index('Date')['Value'].rename('competitors_share_of_voice')
    bristor_factory_volumes = bristor_df[0].set_index('Date')['Value'].rename('bristor_factory_volumes')
    bristor_demand_volumes = bristor_df[2][:46].set_index('Date')['Value'].rename('y')  # bristor_demand_volumes
    competitors_demand_volumes = bristor_df[2][46:92].set_index('Date')['Value'].rename('competitors_demand_volumes')

    df = bristor_demand_volumes.to_frame().join(competitors_new_patients, how='outer').join(bristor_emails,
                                                                                            how='outer').join(
        bristor_call, how='outer').join(bristor_share_of_voice, how='outer').join(competitors_share_of_voice,
                                                                                  how='outer').join(
        bristor_factory_volumes, how='outer').join(bristor_new_patients, how='outer').join(competitors_demand_volumes,
                                                                                           how='outer').reset_index().rename(
        columns={'Date': 'ds'})
    return df


def fc(event_start = pd.to_datetime("2025-04-01"), impact = 1.0, event_type = 'share_of_voice'):
    ### Loading
    bristor_df = BRISTOR.load_bristor_into_df("/home/samsung/Desktop/BMS/BRISTOR_Zegoland.xlsx")

    ### hardcoding signals
    ds = pd.date_range(start="2020-08-01", end="2024-10-01", freq="M"),

    bristor_new_patients = bristor_df[3][:44].set_index('Date')['Value'].rename('bristor_new_patients')
    competitors_new_patients = bristor_df[3][44:87].set_index('Date')['Value'].rename('competitors_new_patients')
    bristor_emails = bristor_df[4][:51].set_index('Date')['Value'].rename('bristor_emails')
    bristor_call = bristor_df[4][51:103].set_index('Date')['Value'].rename('bristor_call')
    bristor_mail = bristor_df[4][104:153].set_index('Date')['Value'].rename('bristor_mail')
    bristor_remote_call = bristor_df[4][153:201].set_index('Date')['Value'].rename('bristor_remote_call')
    bristore_telephone = bristor_df[4][201:].set_index('Date')['Value'].rename('bristor_telephone')
    bristor_share_of_voice = bristor_df[5][:40].set_index('Date')['Value'].rename('bristor_share_of_voice')
    competitors_share_of_voice = bristor_df[5][40:80].set_index('Date')['Value'].rename('competitors_share_of_voice')
    bristor_factory_volumes = bristor_df[0].set_index('Date')['Value'].rename('bristor_factory_volumes')
    bristor_demand_volumes = bristor_df[2][:46].set_index('Date')['Value'].rename('y')  # bristor_demand_volumes
    competitors_demand_volumes = bristor_df[2][46:92].set_index('Date')['Value'].rename('competitors_demand_volumes')

    df = (bristor_demand_volumes.to_frame().join(competitors_new_patients, how='outer').join(bristor_emails,
                                                                                            how='outer').join(
        bristor_call, how='outer').join(bristor_share_of_voice, how='outer').join(competitors_share_of_voice,
                                                                                  how='outer').join(
        bristor_factory_volumes, how='outer').join(bristor_new_patients, how='outer').join(competitors_demand_volumes,how='outer').join(bristor_mail, how='outer').join(bristor_remote_call, how='outer').join(bristore_telephone,how='outer')).reset_index().rename(columns={'Date': 'ds'})
    ### TODO check if this makes sense
    df = df.fillna(method='bfill')
    df = df.fillna(method='ffill')
    df = df.drop([54,50, 52])
    # df = df.fillna(0)

    model = Prophet()  # TODO tweak parameters
    model.add_regressor('competitors_new_patients')
    model.add_regressor('bristor_emails')
    model.add_regressor('bristor_call')
    model.add_regressor('bristor_mail')
    model.add_regressor('bristor_remote_call')
    model.add_regressor('bristor_telephone')
    model.add_regressor('competitors_share_of_voice')
    model.add_regressor('bristor_share_of_voice')
    model.add_regressor('bristor_factory_volumes')
    model.add_regressor('bristor_new_patients')
    # model.add_regressor('competitor_demand_volumes')
    model.add_regressor('competitors_demand_volumes')
    # model.add_regressor('bristor_demand_volumes')

    # Fit the model
    model.fit(df)

    # Create future DataFrame
    future = model.make_future_dataframe(periods=12, freq="M")  # Forecast for next 12 months
    future['competitors_new_patients'] = df['competitors_new_patients']
    future['bristor_emails'] = df['bristor_emails']
    future['bristor_call'] = df['bristor_call']
    future['bristor_mail'] = df['bristor_mail']
    future['bristor_remote_call'] = df['bristor_remote_call']
    future['bristor_telephone'] = df['bristor_telephone']
    future['competitors_share_of_voice'] = df['competitors_share_of_voice']
    future['bristor_share_of_voice'] = df['bristor_share_of_voice']
    future['bristor_factory_volumes'] = df['bristor_factory_volumes']
    future['bristor_new_patients'] = df['bristor_new_patients']
    future['competitors_demand_volumes'] = df['competitors_demand_volumes']

    future = future.fillna(method='bfill')
    future = future.fillna(method='ffill')

    evt = 'competitors_new_patients'
    if (event_type == 'emails'):
        evt = 'bristor_emails'
    elif (event_type == 'calls'):
        evt = 'bristor_call'
    elif (event_type == 'competitors_share_of_voice'):
        evt = 'competitors_share_of_voice'
    elif (event_type == 'share_of_voice'):
        evt = 'bristor_share_of_voice'
    elif (event_type == 'factory_volumes'):
        evt = 'bristor_factory_volumes'
    elif (event_type == 'new_patients'):
        evt = 'bristor_new_patients'
    elif (event_type == 'competitors_demand_volumes'):
        evt = 'competitors_demand_volumes'


    print(evt)

    # for regressor in ['competitors_new_patients', 'bristor_emails', 'bristor_call',
    #                   'bristor_mail', 'bristor_remote_call', 'bristor_telephone',
    #                   'competitors_share_of_voice', 'bristor_share_of_voice',
    #                   'bristor_factory_volumes', 'bristor_new_patients', 'competitors_demand_volumes']:
    #     forecasted_values = forecast_regressor(future, regressor, df)
    #     future[regressor] = forecasted_values['yhat']

    # Adjust SoV for competitor impact
    for i, date in enumerate(future['ds']):  # TODO fix the share of voice
        if date >= event_start:
            future.loc[i, evt] *= impact  # Reduce SoV by 10%

    # Make predictions
    return model.predict(future)

def fc_compounded(event_start = pd.to_datetime("2025-04-01"), impact = 1.0, event_type = 'share_of_voice'):
    ### Loading
    bristor_df = BRISTOR.load_bristor_into_df("/home/samsung/Desktop/BMS/BRISTOR_Zegoland.xlsx")

    ### hardcoding signals
    ds = pd.date_range(start="2020-08-01", end="2024-10-01", freq="M"),

    bristor_new_patients = bristor_df[3][:44].set_index('Date')['Value'].rename('bristor_new_patients')
    competitors_new_patients = bristor_df[3][44:87].set_index('Date')['Value'].rename('competitors_new_patients')
    bristor_emails = bristor_df[4][:51].set_index('Date')['Value'].rename('bristor_emails')
    bristor_call = bristor_df[4][51:103].set_index('Date')['Value'].rename('bristor_call')
    bristor_mail = bristor_df[4][104:153].set_index('Date')['Value'].rename('bristor_mail')
    bristor_remote_call = bristor_df[4][153:201].set_index('Date')['Value'].rename('bristor_remote_call')
    bristore_telephone = bristor_df[4][201:].set_index('Date')['Value'].rename('bristor_telephone')
    bristor_share_of_voice = bristor_df[5][:40].set_index('Date')['Value'].rename('bristor_share_of_voice')
    competitors_share_of_voice = bristor_df[5][40:80].set_index('Date')['Value'].rename('competitors_share_of_voice')
    bristor_factory_volumes = bristor_df[0].set_index('Date')['Value'].rename('bristor_factory_volumes')
    bristor_demand_volumes = bristor_df[2][:46].set_index('Date')['Value'].rename('y')  # bristor_demand_volumes
    competitors_demand_volumes = bristor_df[2][46:92].set_index('Date')['Value'].rename('competitors_demand_volumes')

    df = (bristor_demand_volumes.to_frame().join(competitors_new_patients, how='outer').join(bristor_emails,
                                                                                            how='outer').join(
        bristor_call, how='outer').join(bristor_share_of_voice, how='outer').join(competitors_share_of_voice,
                                                                                  how='outer').join(
        bristor_factory_volumes, how='outer').join(bristor_new_patients, how='outer').join(competitors_demand_volumes,how='outer').join(bristor_mail, how='outer').join(bristor_remote_call, how='outer').join(bristore_telephone,how='outer')).reset_index().rename(columns={'Date': 'ds'})
    ### TODO check if this makes sense
    df = df.fillna(method='bfill')
    df = df.fillna(method='ffill')
    df = df.drop([54,50, 52])
    # df = df.fillna(0)

    model = Prophet()  # TODO tweak parameters
    model.add_regressor('competitors_new_patients')
    model.add_regressor('bristor_emails')
    model.add_regressor('bristor_call')
    model.add_regressor('bristor_mail')
    model.add_regressor('bristor_remote_call')
    model.add_regressor('bristor_telephone')
    model.add_regressor('competitors_share_of_voice')
    model.add_regressor('bristor_share_of_voice')
    model.add_regressor('bristor_factory_volumes')
    model.add_regressor('bristor_new_patients')
    # model.add_regressor('competitor_demand_volumes')
    model.add_regressor('competitors_demand_volumes')
    # model.add_regressor('bristor_demand_volumes')

    # Fit the model
    model.fit(df)

    # Create future DataFrame
    future = model.make_future_dataframe(periods=12, freq="M")  # Forecast for next 12 months
    future['competitors_new_patients'] = df['competitors_new_patients']
    future['bristor_emails'] = df['bristor_emails']
    future['bristor_call'] = df['bristor_call']
    future['bristor_mail'] = df['bristor_mail']
    future['bristor_remote_call'] = df['bristor_remote_call']
    future['bristor_telephone'] = df['bristor_telephone']
    future['competitors_share_of_voice'] = df['competitors_share_of_voice']
    future['bristor_share_of_voice'] = df['bristor_share_of_voice']
    future['bristor_factory_volumes'] = df['bristor_factory_volumes']
    future['bristor_new_patients'] = df['bristor_new_patients']
    future['competitors_demand_volumes'] = df['competitors_demand_volumes']

    future = future.fillna(method='bfill')
    future = future.fillna(method='ffill')

    evt = 'competitors_new_patients'
    if (event_type == 'emails'):
        evt = 'bristor_emails'
    elif (event_type == 'calls'):
        evt = 'bristor_call'
    elif (event_type == 'competitors_share_of_voice'):
        evt = 'competitors_share_of_voice'
    elif (event_type == 'share_of_voice'):
        evt = 'bristor_share_of_voice'
    elif (event_type == 'factory_volumes'):
        evt = 'bristor_factory_volumes'
    elif (event_type == 'new_patients'):
        evt = 'bristor_new_patients'
    elif (event_type == 'competitors_demand_volumes'):
        evt = 'competitors_demand_volumes'


    print(evt)
    last_ts = df.index[-1]
    for regressor in ['competitors_new_patients', 'bristor_emails', 'bristor_call',
                      'bristor_mail', 'bristor_remote_call', 'bristor_telephone',
                      'competitors_share_of_voice', 'bristor_share_of_voice',
                      'bristor_factory_volumes', 'bristor_new_patients', 'competitors_demand_volumes']:
        forecasted_values = forecast_regressor(future, regressor, df)
        new_data = forecasted_values[forecasted_values.index >= last_ts].copy()
        future[regressor].update(new_data['yhat'])

    # Adjust SoV for competitor impact
    for i, date in enumerate(future['ds']):  # TODO fix the share of voice
        if date >= event_start:
            future.loc[i, evt] *= impact  # Reduce SoV by 10%

    # Make predictions
    return model.predict(future)

fc()
### CORRELATION MATRIX


#regressor_names_historic_data = ['competitors_new_patients', 'bristor_emails', 'bristor_call', 'competitors_share_of_voice', 'bristor_share_of_voice', 'bristor_factory_volumes', 'bristor_new_patients', 'competitors_demand_volumes']
# Correlation heatmap
#correlation_matrix = df[regressor_names_historic_data].corr()
#sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
#plt.title('Correlation Matrix')
#plt.show()