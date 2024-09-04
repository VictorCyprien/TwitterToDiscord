from typing import Dict
from glom import glom

# This allow to remove empty content before getting user info
def filter_empty_data(data: Dict):
    entries_path = "data.user.result.timeline.timeline.instructions.3.entries"
    list_user = glom(data, entries_path)
    filtered_entries = [
        one_user for one_user in list_user
        if "itemContent" in one_user.get("content", {})
    ]
    data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"][3]["entries"] = filtered_entries
    return data

# Display user info 
def extract_users_data(data: Dict):
    entries_path = "data.user.result.timeline.timeline.instructions.3.entries"
    content_path = "content.itemContent.user_results.result"
    list_user = glom(data, entries_path)
    for one_user in list_user:
        user_id = glom(one_user, f"{content_path}.rest_id")
        username = glom(one_user, f"{content_path}.legacy.name")
        description = glom(one_user, f"{content_path}.legacy.description")

        print(f"USER ID : {user_id}")
        print(f"USERNAME : {username}")
        print(f"DESCRIPTION : {description}")
