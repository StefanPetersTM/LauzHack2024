import pandas as pd
import numpy as np
import INNO_EL,INNO_FL,BRISTOR

from prophet import Prophet

def main():
    print("Hello from bmc-lzhk!")

bristor_location:str = ""
inno_el_location:str = ""
inno_fl_location:str = ""


bristor_df = BRISTOR.load_bristor_into_df(bristor_location)
inno_el_df = INNO_EL.load_inno_el_into_df(inno_el_location)
inno_fl_df  = INNO_FL.load_inno_fl_into_df(inno_fl_location)

