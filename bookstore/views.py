from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Book, Author, Category
from .forms import BookForm

# Create your views here.
class DashboardView(View):
    def get(self, request):
        return render(request, 'admin/layout/base.html')
    
class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'admin/layout/book_list.html', {'books': books})
    
@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class BookCreateView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'admin/layout/book_form.html', {'form': form})
    
    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'id': book.id, 'title': book.title})
            return redirect('book_list')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        return render(request, 'admin/layout/book_form.html', {'form': form})
    
@method_decorator(require_http_methods(["GET", "POST", "PUT"]), name='dispatch')
class BookUpdateView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=book)
        return render(request, 'admin/layout/book_form.html', {'form': form, 'book': book})
    
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'id': book.id, 'title': book.title})
            return redirect('book_list')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        return render(request, 'admin/layout/book_form.html', {'form': form, 'book': book})

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        data = json.loads(request.body)
        form = BookForm(data, instance=book)
        if form.is_valid():
            book = form.save()
            return JsonResponse({'success': True, 'id': book.id, 'title': book.title})
        return JsonResponse({'success': False, 'errors': form.errors})
    
@method_decorator(require_http_methods(["GET", "POST", "DELETE"]), name='dispatch')
class BookDeleteView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'admin/layout/book_confirm_delete.html', {'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('book_list')

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return JsonResponse({'success': True})