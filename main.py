# Mastodon.py
import datetime

import mastodon
from bs4 import BeautifulSoup

from DataUtil import *
from PostMentions import *

CLIENT_KEY = "NdneB9Zkoj_fEuEUZNfwxd-b_dqx4auT6zvqtVGY1Nc"
CLIENT_SECRET = "6DCqyFTKX1JNlrInYQ6aR95uGF-MosFz9yPmIKD576o"
ACCESS_TOKEN = "VsJDxryTZ5YB2j_6y77iCPHuOBruJQJbzHbw_xaS-rA"
BASE = "https://mastodon.social"

target_accounts = [
    "dan--dan.bsky.social",
    "ppuppa.bsky.social",
    "fluffywuffy-egg.bsky.social"
]

APP_NAME = 'DanDanPublish'

id_matcher = IdMatcher()
since_id_manager = SinceIdManager()


def check_notifications(notifications):
    for notification in notifications.__reversed__():
        check_notification(notification)


def check_notification(notification):
    id = notification['id']
    type = notification['type']
    account = notification['account']

    if type == 'follow':
        return

    status = notification['status']

    if type == 'status' or type == 'mention':
        check_toot(id, account, status)

    if type == 'favorite':
        # 내 account일 경우: 상대 toot에 favorite
        # 상대 account일 경우: 내 acocunt에 favorite
        check_favorite()

    since_id_manager.since_id = id


def check_toot(id, account, status):
    username = account['username']

    content = BeautifulSoup(status['content'], 'html.parser').text
    content = content.replace('@dandan_devloper@mastodon.social', '')

    # get display_name
    display_name = account['display_name']

    # parse media attachments
    media_attachments = status['media_attachments']
    media_ids = None
    if len(media_attachments) > 0:
        media_ids = get_media_ids(media_attachments)

    # get reply id
    mentions = status['mentions']

    reply_to_id = status['in_reply_to_id']
    in_reply_to_id = None
    if reply_to_id is not None:
        reply_to_id = str(reply_to_id)

        if is_bridge_accounts(username, target_accounts):
            in_reply_to_id = id_matcher.get_bot_id(reply_to_id)

        else:
            in_reply_to_id = id_matcher.get_bridge_id(reply_to_id)

        mention_id = id_matcher.get_user_id_for_mention(in_reply_to_id)

        if mention_id is not None:
            content = f"{mention_id} {content}"

        if in_reply_to_id is None:
            print(f"id: {id}")
            print(f"reply_to_id = {reply_to_id}")
            print('current state')
            print(status)
            return

    print(status)

    new_status = publish_toot(
        display_name=display_name,
        content=content,
        media_ids=media_ids,
        in_reply_to_id=in_reply_to_id,
        sensitive=status['sensitive'],
        visibility=status['visibility'],
        spoiler_text=status['spoiler_text']
    )

    # add id data
    if is_bridge_accounts(username, target_accounts):
        bridge_id = str(status['id'])
        bot_id = str(new_status['id'])
    else:
        bridge_id = str(new_status['id'])
        bot_id = str(status['id'])

    id_matcher.add(bridge_id, bot_id)

    if len(mentions) > 0:
        id_matcher.add_user_id_for_mention(bot_id, f"@account['acct']")


def publish_toot(display_name, content, media_ids=None, in_reply_to_id=None, sensitive=None,
                 visibility=None,
                 spoiler_text=''):
    new_content = f"{display_name}\n\n{content}"
    print(f"post: {new_content}")

    return api.status_post(
        new_content,
        in_reply_to_id=in_reply_to_id,
        media_ids=media_ids,
        sensitive=sensitive,
        visibility=visibility,
        spoiler_text=spoiler_text,
        language='ko'
    )


def check_favorite():
    pass


if __name__ == '__main__':
    api = mastodon.Mastodon(
        client_id=CLIENT_KEY,
        client_secret=CLIENT_SECRET,
        access_token=ACCESS_TOKEN,
        api_base_url=BASE
    )

    # notifications = api.notifications()
    notifications = api.notifications(since_id=since_id_manager.since_id)

    print(len(notifications))
    check_notifications(notifications)
