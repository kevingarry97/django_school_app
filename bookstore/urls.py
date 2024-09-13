from django.urls import path
from .views import DashboardView, BookListView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [  # Now this points to the login page
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/books/', BookListView.as_view(), name='book_list'),
    path('dashboard/books/create/', BookCreateView.as_view(), name='book_create'),
    path('dashboard/books/<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('dashboard/books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
]