import asyncio
from bs4 import BeautifulSoup

from playwright.async_api import Page


async def get_last_following_from_user(page: Page, user: str):
    await page.goto(f"https://x.com/{user}/following")
    await asyncio.sleep(3)
    html = await page.inner_html("main[role=main]")
    soup = BeautifulSoup(html, "html.parser")
    last_following = soup.find("div", {"style": "transform: translateY(0px); position: absolute; width: 100%;"})
    if "Suivre" in last_following.text:
        print(f"{user} : {last_following.text.split("Suivre")[0]}")
        last_following = last_following.text.split("Suivre")[0]
    else:
        print(f"{user} : {last_following.text.split("Abonné")[0]}")
        last_following = last_following.text.split("Abonné")[0]
    await asyncio.sleep(2)
    return last_following
