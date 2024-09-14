from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Book, Author, Category
from .forms import BookForm, CategoryForm, AuthorForm
from django.db.models import Count
from django.db.models.functions import ExtractYear

# Create your views here.
def book_chart_data(request):
    # Extract the year from the publication_date and count the number of books per year
    books_per_year = (
        Book.objects
        .annotate(year=ExtractYear('publication_date'))  # Extract the year from the date
        .values('year')  # Group by the extracted year
        .annotate(book_count=Count('id'))  # Count the number of books per year
        .order_by('year')  # Order by year
    )

    # Prepare the data for Chart.js
    labels = [entry['year'] for entry in books_per_year]  # X-axis: years
    data = [entry['book_count'] for entry in books_per_year]  # Y-axis: number of books

    # Return the data as JSON
    return JsonResponse({
        'labels': labels,  # Years
        'data': data  # Number of books per year
    })
    
class DashboardView(View):
    def get(self, request):
        return render(request, 'admin/layout/dashboard.html')

# Book CRUD Views
class BookListView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        authors = Author.objects.all()
        categories = Category.objects.all()
        return render(request, 'admin/layout/book_list.html', {'books': books, 'authors': authors, 'categories': categories})

class BookCRUDView(View):
    def post(self, request, *args, **kwargs):
        # Handle book creation and updating
        book_id = request.POST.get('bookId')
        
        # If there's a book_id, this is an update
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            form = BookForm(request.POST, instance=book)
        else:
            # Otherwise, we're creating a new book
            form = BookForm(request.POST)
        
        if form.is_valid():
            book = form.save()
            return JsonResponse({'success': True, 'id': book.id, 'title': book.title})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        try:
            # Get the book ID from the request body and delete the book
            book_id = request.POST.get('bookId')
            book = get_object_or_404(Book, id=book_id)
            book.delete()
            return JsonResponse({'success': True})
        
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

    def get(self, request, *args, **kwargs):
        # Optional: To handle GET requests for fetching book data (if needed)
        return HttpResponseBadRequest("Invalid method for this endpoint")

# Category CRUD
class CategoryListView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'admin/layout/category_list.html', {'categories': categories})

class CategoryCRUDView(View):
    def post(self, request, *args, **kwargs):
        # Handle category creation and updating
        category_id = request.POST.get('categoryId')

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            form = CategoryForm(request.POST, instance=category)
        else:
            form = CategoryForm(request.POST)
        
        if form.is_valid():
            category = form.save()
            return JsonResponse({'success': True, 'id': category.id, 'name': category.name})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    def delete(self, request, *args, **kwargs):
        try:
            # Get the category ID from the request body
            category_id = request.POST.get('categoryId')

            if not category_id:
                return JsonResponse({'success': False, 'error': 'No category ID provided'}, status=400)

            category = get_object_or_404(Category, id=category_id)
            category.delete()

            # Return a success response
            return JsonResponse({'success': True})
        
        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

# Author CRUD
class AuthorListView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Attempt to fetch authors
            authors = Author.objects.all()
            return render(request, 'admin/layout/author_list.html', {'authors': authors})
        except Exception as e:
            # Handle the exception
            print(f"Error occurred: {e}")
        finally:
            # This block runs regardless of whether an exception occurred or not
            print("Cleaning up")
        

class AuthorCRUDView(View):
    def post(self, request, *args, **kwargs):
        author_id = request.POST.get('authorId')
        if author_id:
            author = get_object_or_404(Author, id=author_id)
            form = AuthorForm(request.POST, instance=author)
        else:
            form = AuthorForm(request.POST)
        
        if form.is_valid():
            author = form.save()
            return JsonResponse({'success': True, 'id': author.id, 'name': author.name})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        
    def delete(self, request, *args, **kwargs):
        try:
            # Get the ID of the author to delete from the request body
            author_id = request.POST.get('authorId')
            
            # Ensure the author exists
            author = get_object_or_404(Author, id=author_id)
            
            # Delete the author
            author.delete()

            # Return a success response
            return JsonResponse({'success': True})
        except Exception as e:
            # Handle the exception
            print(f"Error occurred: {e}")
        finally:
            # This block runs regardless of whether an exception occurred or not
            print("Cleaning up")
        
