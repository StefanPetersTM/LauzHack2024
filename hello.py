import pandas as pd
import numpy as np
import INNO_EL,INNO_FL,BRISTOR

from prophet import Prophet

def main():
    print("Hello from bmc-lzhk!")

bristor_df = BRISTOR.load_bristor_into_df("/home/stefan/Downloads/files/BRISTOR_Zegoland.xlsx")
inno_el_df = INNO_EL.load_inno_el_into_df("/home/stefan/Downloads/files/INNOVIX_Elbonie.xlsx")
inno_fl_df  = INNO_FL.load_inno_fl_into_df("/home/stefan/Downloads/files/INNOVIX_Floresland.xlsx")







df = pd.read_csv('https://raw.githubusercontent.com/facebook/prophet/main/examples/example_wp_log_peyton_manning.csv')
df.head()

m = Prophet()
m.fit(df)

# Python
future = m.make_future_dataframe(periods=365)
future.tail()

# Python
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

# Python
fig1 = m.plot(forecast)
#fig1.show()
# Python
fig2 = m.plot_components(forecast)
#fig2.show()
# Python
from prophet.plot import plot_plotly, plot_components_plotly

forecast_plot = plot_plotly(m, forecast)
forecast_plot.show()

# Python
components = plot_components_plotly(m, forecast)
components.show()

if __name__ == "__main__":
    main()
