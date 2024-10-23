def get_media_ids(media_attachments):
    media_ids = []

    for media in media_attachments:
        media_ids.append(media['id'])

    if len(media_ids) == 0:
        return None

    return media_ids


def is_bridge_accounts(account_name, target_accounts):
    return account_name in target_accounts
