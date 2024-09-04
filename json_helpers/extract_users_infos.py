from typing import Dict, List
from glom import glom

# This allow to remove empty content before getting user info
def filter_empty_data(data: Dict) -> Dict:
    entries_path = "data.user.result.timeline.timeline.instructions.3.entries"
    list_user = glom(data, entries_path)
    filtered_entries = [
        one_user for one_user in list_user
        if "itemContent" in one_user.get("content", {})
    ]
    data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"][3]["entries"] = filtered_entries
    return data

# Display user info 
def extract_users_data(data: Dict) -> List[Dict]:
    entries_path = "data.user.result.timeline.timeline.instructions.3.entries"
    content_path = "content.itemContent.user_results.result"
    list_user = glom(data, entries_path)
    final_list_user = []
    for one_user in list_user:
        user_id = glom(one_user, f"{content_path}.rest_id")
        username = glom(one_user, f"{content_path}.legacy.screen_name")
        name = glom(one_user, f"{content_path}.legacy.name")
        description = glom(one_user, f"{content_path}.legacy.description")

        current_user = {
            "user_id": user_id,
            "username": username,
            "name": name,
            "description": description
        }

        final_list_user.append(current_user)
    
    return final_list_user
