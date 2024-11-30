import pandas as pd
import locale


month_map = {
	"janv": "Jan", "févr": "Feb", "mars": "Mar", "avr": "Apr", "mai": "May",
	"juin": "Jun", "juil": "Jul", "août": "Aug", "sept": "Sep", "oct": "Oct",
	"nov": "Nov", "déc": "Dec"
}

two_digit_to_four_map = {'17' : '2017', '18' : '2018', '19' : '2019'
	,'20': '2020', '21': '2021', '22': '2022', '23': '2023', '24': '2024', '25': '2025',
						 '26': '2026', '27': '2027', '28': '2028', '29': '2029', '30': '2030'}



def parse_french_dates(series):


	for french, english in month_map.items():
		series = series.str.replace(french, english, regex=False)
	for two,four in two_digit_to_four_map.items():
		series = series.str.replace(rf'(?<=\b)-{two}\b', f'-{four}', regex=True)
	result = pd.to_datetime(series, errors='raise')
	return result


def parse_ohio_dates(series: pd.Series):
	try:
		locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
		str_series = series.astype(str)
		return pd.to_datetime(series, format="mixed",errors='raise')
	except ValueError:
		pass

	try:
		new_datetime = parse_french_dates(series)
		return new_datetime
	except ValueError:
		pass

	# if all else fails

	return pd.NaT

def load_inno_el_into_df(filename: str):
	df = pd.read_excel(filename,sheet_name=None, header=0)
	df.pop("Main")
	new_dfs = []
	for sheet in df:
		particular_df = df[sheet]
		particular_df["Country"] = particular_df["Country"].astype(str)
		particular_df["Data type"] = particular_df["Data type"].astype(str)
		try:
			particular_df["Product"] = particular_df["Product"].astype(str)
		except KeyError:
			pass
		try:
			particular_df["Products"] = particular_df["Products"].astype(str)
		except KeyError:
			pass
		try:
			particular_df["Forecast Algorithm"] = particular_df["Forecast Algorithm"].astype(str)
		except KeyError:
			pass
		try:
			particular_df["Data period"] = particular_df["Data period"].astype(str)
		except KeyError:
			pass
		try:
			particular_df["Channel"] = particular_df["Channel"].astype(str)
		except KeyError:
			pass
		try:
			particular_df["Indication"] = particular_df["Indication"].astype(str)
		except KeyError:
			pass

		particular_df["Date"] = particular_df["Date"].astype(str)
		particular_df["Date"] = parse_ohio_dates(particular_df["Date"])

		new_dfs.append(particular_df)
	#ex-factory

	return new_dfs