from django.utils.timezone import now


def image_directory_path(instance, filename):
    today_as_date = now().date()
    today_as_date_str = today_as_date.strftime("%Y/%m/%d")
    return f"uploads/{today_as_date_str}/{instance.item.title}/main/{filename}"
