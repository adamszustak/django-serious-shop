from django.utils.timezone import now
from django.contrib.auth import get_user_model


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
