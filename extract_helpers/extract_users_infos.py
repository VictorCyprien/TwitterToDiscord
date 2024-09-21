from typing import Dict, List
from glom import glom

from datetime import datetime

from .entities import get_entities
from helpers import Logger


logger = Logger()


# This allow to remove empty content before getting user info
def filter_empty_data(data: Dict) -> Dict:
    entities = get_entities(data)
    filtered_entries = [
        one_user for one_user in entities
        if "itemContent" in one_user.get("content", {})
    ]

    for index in [0, 3]:
        try:
            data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"][index]["entries"] = filtered_entries
        except (IndexError, KeyError):
            continue
    return data


def extract_urls(list_urls: Dict) -> str:
    description_urls = glom(list_urls, "description.urls", skip_exc=KeyError, default=[])
    urls_url = glom(list_urls, "url.urls", skip_exc=KeyError, default=[])

    urls = ""
    if description_urls:
        try:
            urls = urls + description_urls[0]["expanded_url"] + "\n"
        except KeyError:
            logger.error("Unable to get url, proceed...")
    if urls_url:
        try:
            urls = urls + urls_url[0]["expanded_url"] + "\n"
        except KeyError:
            logger.error("Unable to get url, proceed...")
    return urls


# Display user info 
def extract_users_data(data: Dict) -> List[Dict]:
    content_path = "content.itemContent.user_results.result"
    entities = get_entities(data)
    final_list_user = []
    for one_entity in entities:
        username = glom(one_entity, f"{content_path}.legacy.screen_name", skip_exc=KeyError, default=None)
        name = glom(one_entity, f"{content_path}.legacy.name", skip_exc=KeyError, default=None)
        description = glom(one_entity, f"{content_path}.legacy.description", skip_exc=KeyError, default=None)
        profile_image = glom(one_entity, f"{content_path}.legacy.profile_image_url_https", skip_exc=KeyError, default=None)
        created_at = glom(one_entity, f"{content_path}.legacy.created_at", skip_exc=KeyError, default=None)
        followers_number = glom(one_entity, f"{content_path}.legacy.followers_count", skip_exc=KeyError, default=None)
        following_number = glom(one_entity, f"{content_path}.legacy.friends_count", skip_exc=KeyError, default=None)
        tweets_count = glom(one_entity, f"{content_path}.legacy.statuses_count", skip_exc=KeyError, default=None)
        
        list_urls = glom(one_entity, f"{content_path}.legacy.entities", skip_exc=KeyError, default=None)
        urls = extract_urls(list_urls)

        current_user = {
            "profile_url": f"https://x.com/{username}",
            "username": username,
            "name": name,
            "description": description,
            "profile_image": profile_image,
            "created_at": datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y').strftime('%d/%m/%Y') if created_at is not None else None,
            "followers_number": followers_number,
            "following_number": following_number,
            "tweets_count": tweets_count
        }

        if urls != "":
            current_user["urls"] = urls

        final_list_user.append(current_user)
    
    return final_list_user
