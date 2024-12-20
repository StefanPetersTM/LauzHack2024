### Quickstart guide


# Demand Forecasting and Event Simulation Dashboard

## Overview

Our project is an interactive dashboard designed to forecast Bristor's demand volumes and simulate the impact of various marketing events on future demand. By leveraging Facebook's Prophet time series forecasting model and an interactive Dash application, we provide a powerful tool for stakeholders to visualize and understand how different factors influence Bristor's future demand.

## How to Run the Project

### Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/bristor-forecasting.git
   cd bristor-forecasting
   ```

2. **Install Dependencies**:

   ```bash
   pip install pandas numpy prophet dash plotly
   ```

3. **Place the Data File**:

   - Change the file path in `Prophet_Bristor.py` path pointing to `BRISTOR_Zegoland.xlsx`.

4. **Run the Application**:

   ```bash
   python main.py
   ```

5. **Access the Dashboard**:

   - Open your web browser and navigate to `http://127.0.0.1:8050` to view the dashboard.


## Problem Statement

Understanding and predicting demand is crucial for effective decision-making in sales and marketing. Bristor faces challenges in forecasting demand due to multiple influencing factors such as competitor activities, marketing efforts, and market dynamics. Traditional forecasting methods often lack the flexibility to simulate the impact of hypothetical events or adjust forecasts based on real-time inputs.

## Solution

We developed a dynamic forecasting tool that:

- **Utilizes Advanced Time Series Forecasting**: Employs Facebook's Prophet model to generate accurate demand forecasts incorporating multiple external regressors.
- **Simulates Marketing Event Impacts**: Allows users to adjust variables like event start date, impact magnitude, and event type to simulate how marketing events affect demand.
- **Offers an Interactive Dashboard**: Provides an intuitive interface with sliders, dropdowns, and input fields for real-time forecast adjustments and visualization.
- **Displays Correlation Insights**: Computes and visualizes correlation matrices to help users understand relationships between different influencing factors.

## Features

- **Interactive Forecasting**: Adjust forecasts on-the-fly by modifying event parameters and immediately see the impact on demand projections.
- **Multi-Factor Analysis**: Incorporates various factors such as competitor new patients, marketing emails, calls, share of voice, and more into the forecasting model.
- **User-Friendly Interface**: Built with Dash, the dashboard is intuitive and easy to navigate, even for non-technical users.
- **Real-Time Visualizations**: Presents forecasts and correlations through dynamic graphs and heatmaps that update in real-time with user inputs.
- **Correlation Matrix**: Provides a heatmap to visualize the correlations between different variables, aiding in deeper data analysis.

## How It Works

### Data Preparation

- **Data Loading**: Historical data is loaded from `BRISTOR_Zegoland.xlsx`.
- **Signal Processing**: Extracts and processes relevant signals such as new patients, marketing activities, share of voice, and demand volumes.
- **Data Alignment**: Ensures all time series data are correctly aligned despite different lengths by forward and backward filling missing values.

### Forecasting with Prophet

- **Model Configuration**: A Prophet model is configured with relevant regressors that influence demand volumes.
- **Model Training**: The model is trained using the prepared historical data.
- **Future Data Frame Creation**: A future data frame is created to extend forecasts beyond the historical data range.

### Event Simulation

- **Event Parameters**: Users can specify:
  - **Event Start Date**: When the event's impact begins.
  - **Impact Magnitude**: The percentage change in the influencing factor.
  - **Event Type**: The factor that the event affects (e.g., emails, calls, share of voice).
- **Impact Application**: The specified impact is applied to the chosen factor in the forecast from the event start date onwards.

### Interactive Dashboard

- **Controls**:
  - **Sliders**: Adjust the date range for historical and forecasted data, and set the event start date.
  - **Dropdowns**: Select the product and the factor of influence (event type).
  - **Numeric Input**: Define the impact magnitude as a percentage.
- **Graphs**:
  - **Demand Forecast**: Visualizes historical demand and forecasted demand with confidence intervals.
  - **Correlation Matrix**: Displays a heatmap of correlations between different variables.

### Real-Time Updates

- **Callback Functions**: Dash callbacks ensure that any change in the inputs triggers an update in the forecast and visualizations.
- **Data Reprocessing**: The model recalculates forecasts based on new inputs, ensuring that the displayed information is always up-to-date.

## Technical Details

### Dashboard Components

- **Graph**: Displays historical and forecasted demand volumes with confidence intervals and error bands.
- **Sliders**: Allow users to adjust the date range and event start date.
- **Dropdowns**: Enable selection of products and factors of influence.
- **Numeric Input**: Sets the magnitude of the event's impact.
- **Correlation Matrix Heatmap**: Visualizes the correlation between different variables.

## Innovation and Impact

- **Interactive Event Simulation**: Empowers users to explore "what-if" scenarios by simulating the impact of various events on demand forecasts.
- **Comprehensive Analysis**: Combines forecasting with correlation analysis to provide deeper insights into how different factors affect demand.
- **User-Centric Design**: The dashboard's intuitive interface makes complex data analysis accessible to users without a technical background.
- **Scalability**: The framework can be easily extended to include more products, additional influencing factors, or more complex event scenarios.


## Conclusion

Our interactive dashboard provides a valuable tool for Bristor's sales and marketing teams to forecast demand and make informed decisions. By simulating the impact of various events and visualizing the results in real-time, stakeholders can proactively strategize and respond to market changes. This project showcases the power of combining advanced forecasting techniques with interactive data visualization to address real-world business challenges.
