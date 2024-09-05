from typing import List, Dict
import pandas as pd


async def create_excel_file(data: List[Dict], filename: str):
    dataframe = pd.DataFrame(data)
    dataframe.to_excel(filename, index=False)
