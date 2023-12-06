from rest_framework.pagination import PageNumberPagination

class FeedPaginator(PageNumberPagination):
    page_size = 20

    def get_page(self):
        page = super().get_page()
        if not page.object_list:
            return None  # Return None when there are no objects
        return page