from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt


async def create_excel_file(data: List[Dict], filename: str):
    dataframe = pd.DataFrame(data)
    dataframe.rename(columns={'username': 'Utilisateur', 'latest_following': 'Dernier abonnement', 'last_check': 'Date du dernier abonnement'}, inplace=True)
    dataframe.to_excel(filename, index=False)


def create_list_image(data: List[Dict]):
    dataframe = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(len(dataframe.columns) * 2, len(dataframe) * 0.4))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=dataframe.values, colLabels=dataframe.columns, cellLoc='center', loc='center')
    plt.savefig('list.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig=fig)