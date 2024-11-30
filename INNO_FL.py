import pandas as pd


def load_inno_fl_into_df(filename: str):
	df = pd.read_excel(filename,sheet_name=None, header=0)
	return df