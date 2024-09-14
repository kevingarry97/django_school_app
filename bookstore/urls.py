from django.urls import path
from .views import DashboardView, BookListView, BookCRUDView, CategoryListView, CategoryCRUDView, AuthorListView, AuthorCRUDView, book_chart_data, category_chart_data, author_chart_data

urlpatterns = [  # Now this points to the login page
    path('', DashboardView.as_view(), name='dashboard'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/crud/', BookCRUDView.as_view(), name='book_crud_url'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/crud/', CategoryCRUDView.as_view(), name='category_crud_url'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/crud/', AuthorCRUDView.as_view(), name='author_crud_url'),
    path('book-chart-data/', book_chart_data, name='book_chart_data'),
    path('category_chart_data/', category_chart_data, name='category_chart_data'),
    path('author_chart_data/', author_chart_data, name='author_chart_data')
]