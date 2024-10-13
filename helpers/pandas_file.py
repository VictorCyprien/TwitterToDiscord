from typing import List, Dict
import pandas as pd
from openpyxl.utils.exceptions import IllegalCharacterError
import matplotlib.pyplot as plt
import re


async def create_excel_file(data: List[Dict], filename: str):
    dataframe = pd.DataFrame(data)
    try:
        dataframe.to_excel(filename, index=False)
    except IllegalCharacterError:
        dataframe = dataframe.map(replace_illegal_characters)
        dataframe.to_excel(filename, index=False)


async def rename_column(filename: str, columns: Dict):
    dataframe = pd.read_excel(filename)
    dataframe.rename(columns=columns, inplace=True)


# This happen when some title have some illegal caracters
# To prevent this, we add a space
def replace_illegal_characters(value):
    if isinstance(value, str):
        return re.sub(r'[\x00-\x1F\x7F]', ' ', value)
    return value


def create_list_image(data: List[Dict]):
    dataframe = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(len(dataframe.columns) * 2, len(dataframe) * 0.4))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=dataframe.values, colLabels=dataframe.columns, cellLoc='center', loc='center')
    plt.savefig('list.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig=fig)