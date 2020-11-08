from django.db import models


class OrderQuerySet(models.query.QuerySet):
    def search_by_user(self, user):
        return self.filter(user=user.id, status="paid").order_by("-created_date")
