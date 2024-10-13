from typing import Dict, List
import json
import asyncio
import aiohttp

from glom import glom

from helpers import get_env_config, Logger, ErrorHandler, RequestStatus
from extract_helpers import extract_users_data, filter_empty_data, get_entities

logger = Logger()


async def get_x_csrf_token(cookies: List[Dict]) -> str:
    x_csrf_token = None
    for one_cookie in cookies:
        if "ct0" in one_cookie["name"]:
            x_csrf_token = one_cookie['value']
    
    return x_csrf_token


async def make_request(url: str, cookies: List[Dict], params: Dict = None) -> Dict:
    env = get_env_config()
    token = env('TWITTER_BEARER_AUTH')

    x_csrf_token = await get_x_csrf_token(cookies)

    if x_csrf_token is None:
        logger.error(ErrorHandler.REQUESTS_ERROR)
        exit(0)

    headers = {
        "Authorization": f"Bearer {token}",
        "x-csrf-token": x_csrf_token
    }

    async with aiohttp.ClientSession(
        headers=headers, 
        cookies={one_cookie["name"]: one_cookie["value"] for one_cookie in cookies}
    ) as session:
        async with session.get(url=url, params=params) as res:
            if res.status == 403:
                RequestStatus.status = "AUTH_PROBLEM"
                return {}
            if res.text == "Rate limit exceeded":
                logger.error("Rate limit exceeded")
                RequestStatus.status = "AUTH_PROBLEM"
                return {}
            
            data: Dict = await res.json()
            if data.get("errors", None) is not None:
                logger.error("Could not authenticate you")
                RequestStatus.status = "AUTH_PROBLEM"
                return {}
            
            users = glom(data, "data.user", skip_exc=KeyError, default={})
            if not users:
                RequestStatus.status = "USER_PROBLEM"
                return {}

    RequestStatus.status = "OK"
    return data


async def get_last_followers_from_user(user_id: int, cookies: List[Dict]) -> List[Dict]:
    url = f"https://x.com/i/api/graphql/3_7xfjmh897x8h_n6QBqTA/Followers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A50%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    data = await make_request(url, cookies)
    await asyncio.sleep(5)
    if not data:
        return []

    filtred_data = filter_empty_data(data)
    return extract_users_data(filtred_data)


async def get_last_followings_from_user(user_id: int, cookies: List[Dict]) -> List[Dict]:
    url = f"https://x.com/i/api/graphql/0yD6Eiv23DKXRDU9VxlG2A/Following?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A50%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    data = await make_request(url, cookies)
    await asyncio.sleep(5)
    if not data:
        return []

    filtred_data = filter_empty_data(data)
    return extract_users_data(filtred_data)


async def get_user_id_with_username(username: str, cookies: List[Dict]) -> int:
    url = f"https://x.com/i/api/graphql/NimuplG1OB7Fd2btCLdBOw/UserByScreenName?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D&features=%7B%22hidden_profile_likes_enabled%22%3Atrue%2C%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&field_toggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D"
    data = await make_request(url, cookies)
    if not data:
        logger.error(ErrorHandler.USER_ERROR)
        return None
    
    user_id = glom(data, "data.user.result.rest_id", skip_exc=KeyError, default=None)
    if user_id is not None:
        user_id = int(user_id)
    return user_id


def get_cursor_from_data(data: Dict) -> str:
    current_cursor = None
    entities = get_entities(data)
    for one_entity in entities:
        if "cursor-bottom" in one_entity.get("entryId", None):
            cursor_from_data: str = one_entity["content"]["value"]
            if not cursor_from_data.startswith("0"):
                current_cursor = one_entity["content"]["value"]
                break
    
    return current_cursor


async def get_all_followings_from_user(user_id: int, cookies: List[Dict]) -> List[List[Dict]]:
    current_cursor = None
    cursor_in_data = True
    number_of_retry = 0
    number_of_requests = 0
    final_data = []

    features = {
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "tweetypie_unmention_optimization_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": False,
        "tweet_awards_web_tipping_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_media_download_video_enabled": False,
        "responsive_web_enhance_cards_enabled": False
    }

    while(cursor_in_data):
        variables = {
            "userId": user_id,
            "count": 50,
            "includePromotedContent": False
        }

        if current_cursor is not None:
            variables["cursor"] = current_cursor

        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(features)
        }

        url = "https://x.com/i/api/graphql/0yD6Eiv23DKXRDU9VxlG2A/Following"
        logger.info(f"Request with cursor : {variables.get("cursor", None)}")
        data = await make_request(url, cookies, params)
        if not data:
            if number_of_retry == 3:
                logger.error("Too many failed attempts, exiting with what we have")
                break
            logger.warning("Request failed, retrying in 10 minutes...")
            number_of_retry += 1
            number_of_requests = 0
            await asyncio.sleep(600)
            continue

        if number_of_requests == 10:
            logger.info("Waiting 5 minutes to continue requests...")
            number_of_requests = 0
            await asyncio.sleep(300)
        else:
            await asyncio.sleep(10)
            number_of_requests += 1
        current_cursor = get_cursor_from_data(data)
        if current_cursor is None:
            cursor_in_data = False

        filtred_data = filter_empty_data(data)
        final_data.append(extract_users_data(filtred_data))
    
    return final_data


async def get_all_followers_from_user(user_id: int, cookies: List[Dict]) -> List[List[Dict]]:
    current_cursor = None
    cursor_in_data = True
    number_of_retry = 0
    number_of_requests = 0
    final_data = []

    features = {
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "tweetypie_unmention_optimization_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": False,
        "tweet_awards_web_tipping_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_media_download_video_enabled": False,
        "responsive_web_enhance_cards_enabled": False
    }

    while(cursor_in_data):
        variables = {
            "userId": user_id,
            "count": 50,
            "includePromotedContent": False
        }

        if current_cursor is not None:
            variables["cursor"] = current_cursor

        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(features)
        }

        url = "https://x.com/i/api/graphql/3_7xfjmh897x8h_n6QBqTA/Followers"
        logger.info(f"Request with cursor : {variables.get("cursor", None)}")
        data = await make_request(url, cookies, params)
        if not data:
            if number_of_retry == 3:
                logger.error("Too many failed attempts, exiting with what we have")
                break
            logger.warning("Request failed, retrying in 10 minutes...")
            number_of_retry += 1
            number_of_requests = 0
            await asyncio.sleep(600)
            continue

        if number_of_requests == 10:
            logger.info("Waiting 5 minutes to continue requests...")
            number_of_requests = 0
            await asyncio.sleep(300)
        else:
            await asyncio.sleep(10)
            number_of_requests += 1
        current_cursor = get_cursor_from_data(data)
        if current_cursor is None:
            cursor_in_data = False
        
        filtred_data = filter_empty_data(data)
        final_data.append(extract_users_data(filtred_data))
    
    return final_data
