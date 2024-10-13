from typing import List, Dict
from itertools import chain

# We convert the list of dict to dict of dicts and we remove _id from each dict
# From this : [{'_id': 123, 'username': 'abcd', 'latest_following': 'someone', 'notifying_discord_channel': 123, 'last_check': '01/01/1900 12:00:00'}]
# To this : {'1630347533317701633': {'username': 'abcd', 'latest_following': 'someone', 'notifying_discord_channel': 123, 'last_check': '01/01/1900 12:00:00'}}

def convert_list_dict_to_dicts(data: List[Dict]) -> Dict:
    return {f"{one_data['_id']}": {key: value for key, value in one_data.items() if key != "_id"} for one_data in data}


# This happend when getting all followers/followings of one user
def convert_list_list_dict_to_list_dict(data: List[List[Dict]]) -> List[Dict]:
    return list(chain.from_iterable(data))
