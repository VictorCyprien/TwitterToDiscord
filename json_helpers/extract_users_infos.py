from typing import Dict, List
from glom import glom

from datetime import datetime


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


def extract_urls(list_urls: Dict) -> str:
    description_urls = glom(list_urls, "description.urls", skip_exc=KeyError, default=[])
    urls_url = glom(list_urls, "url.urls", skip_exc=KeyError, default=[])

    urls = ""
    if description_urls:
        urls = urls + description_urls[0]["expanded_url"] + "\n"
    if urls_url:
        urls = urls + urls_url[0]["expanded_url"] + "\n"
    return urls


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
        profile_image = glom(one_user, f"{content_path}.legacy.profile_image_url_https")
        created_at = glom(one_user, f"{content_path}.legacy.created_at")
        followers_number = glom(one_user, f"{content_path}.legacy.followers_count")
        tweets_count = glom(one_user, f"{content_path}.legacy.statuses_count")
        
        list_urls = glom(one_user, f"{content_path}.legacy.entities")
        urls = extract_urls(list_urls)

        current_user = {
            "user_id": user_id,
            "username": username,
            "name": name,
            "description": description,
            "profile_image": profile_image,
            "created_at": datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y').strftime('%d/%m/%Y'),
            "followers_number": followers_number,
            "tweets_count": tweets_count
        }

        if urls != "":
            current_user["urls"] = urls

        final_list_user.append(current_user)
    
    return final_list_user
