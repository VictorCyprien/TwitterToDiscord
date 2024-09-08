from typing import Dict, List
import requests
from glom import glom

from helpers import open_json, get_env_config, save_json, Logger
from json_helpers import extract_users_data, filter_empty_data

logger = Logger()


async def get_x_csrf_token(cookies: List[Dict]) -> str:
    x_csrf_token = None
    for one_cookie in cookies:
        if "ct0" in one_cookie["name"]:
            x_csrf_token = one_cookie['value']
    
    return x_csrf_token

async def make_request(url: str, cookies: List[Dict]) -> Dict:
    env = get_env_config()
    token = env('TWITTER_BEARER_AUTH')

    x_csrf_token = await get_x_csrf_token(cookies)

    if x_csrf_token is None:
        logger.error("Something wrong with Twitter login, please delete cookies file, log into browser and check what happen")
        exit(0)

    headers = {
        "Authorization": f"Bearer {token}",
        "x-csrf-token": x_csrf_token
    }

    res = requests.get(
        url=url, 
        cookies={one_cookie["name"]: one_cookie["value"] for one_cookie in cookies}, 
        headers=headers
    )

    if res.status_code == 403:
        return {}
    return res.json()


async def get_last_followers_from_user(user_id: int, cookies: List[Dict]) -> List[Dict]:
    url = f"https://x.com/i/api/graphql/3_7xfjmh897x8h_n6QBqTA/Followers?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A50%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    data = await make_request(url, cookies)
    if not data:
        return []

    filtred_data = filter_empty_data(data)
    return extract_users_data(filtred_data)


async def get_last_followings_from_user(user_id: int, cookies: List[Dict]) -> List[Dict]:
    url = f"https://x.com/i/api/graphql/0yD6Eiv23DKXRDU9VxlG2A/Following?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A50%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
    data = await make_request(url, cookies)
    if not data:
        return []

    filtred_data = filter_empty_data(data)
    return extract_users_data(filtred_data)


async def get_user_id_with_username(username: str, cookies: List[Dict]) -> int:
    url = f"https://x.com/i/api/graphql/NimuplG1OB7Fd2btCLdBOw/UserByScreenName?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D&features=%7B%22hidden_profile_likes_enabled%22%3Atrue%2C%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&field_toggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D"
    data = await make_request(url, cookies)
    if not data:
        logger.error("User not found because of cookies, please refresh them")
        return None
    
    user_id = glom(data, "data.user.result.rest_id", skip_exc=KeyError, default=None)
    return user_id
