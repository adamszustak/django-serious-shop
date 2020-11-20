from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now


def image_directory_path(instance, filename):
    today_as_date = now().date()
    today_as_date_str = today_as_date.strftime("%Y/%m/%d")
    return f"uploads/{today_as_date_str}/{instance.item.title}/main/{filename}"


def get_sentinel_user_deleted():
    return get_user_model().objects.get_or_create(username="deleted")[0]


def get_sentinel_user_anonymous():
    return get_user_model().objects.get_or_create(username="anonymous")[0]


def create_order_id(order_id):
    return f"SeS/{order_id}"


def switch_lang_code(path, language):
    lang_codes = [c for (c, name) in settings.LANGUAGES]
    if path == "":
        raise Exception("URL path for language switch is empty")
    elif path[0] != "/":
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception("%s is not a supported language code" % language)
    parts = path.split("/")
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language
    return "/".join(parts)
