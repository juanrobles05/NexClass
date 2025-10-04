# teacher_blog/views.py - REFACTORIZADO CON CLASS-BASED VIEWS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView, ListView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import BlogPost
from .forms import BlogPostForm
from users.models import Teacher


# ================================================================
# MIXINS PERSONALIZADOS PARA REUTILIZACIÓN
# ================================================================

class TeacherRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere que el usuario sea un teacher."""
    
    def test_func(self):
        return (hasattr(self.request.user, 'user_type') and 
                self.request.user.user_type == 'Teacher')
    
    def handle_no_permission(self):
        return redirect('home')


class BlogPostOwnerMixin(UserPassesTestMixin):
    """Mixin que verifica que el usuario sea el propietario del blog post."""
    
    def test_func(self):
        if not hasattr(self.request.user, 'teacher'):
            return False
        blog_post = self.get_object()
        return blog_post.teacher == self.request.user.teacher


# ================================================================
# CLASS-BASED VIEWS PARA CRUD DE BLOG POSTS
# ================================================================

class BlogPostCreateView(LoginRequiredMixin, TeacherRequiredMixin, 
                        SuccessMessageMixin, CreateView):
    """Vista para crear nuevos blog posts."""
    
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'teacher_blog/create_blog_post.html'
    success_url = reverse_lazy('my_profile_teacher')
    success_message = "¡Blog post creado exitosamente!"
    
    def form_valid(self, form):
        """Asigna automáticamente el teacher al blog post."""
        teacher = get_object_or_404(Teacher, user=self.request.user)
        form.instance.teacher = teacher
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Añade contexto adicional a la vista."""
        context = super().get_context_data(**kwargs)
        context['action'] = 'Crear'
        return context


class BlogPostUpdateView(LoginRequiredMixin, TeacherRequiredMixin, 
                        BlogPostOwnerMixin, SuccessMessageMixin, UpdateView):
    """Vista para editar blog posts existentes."""
    
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'teacher_blog/edit_blog_post.html'
    success_url = reverse_lazy('my_profile_teacher')
    success_message = "Blog post actualizado exitosamente."
    
    def get_context_data(self, **kwargs):
        """Añade contexto adicional a la vista."""
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        context['blog_post'] = self.get_object()
        return context


class BlogPostDeleteView(LoginRequiredMixin, TeacherRequiredMixin, 
                        BlogPostOwnerMixin, DeleteView):
    """Vista para eliminar blog posts."""
    
    model = BlogPost
    template_name = 'teacher_blog/delete_blog_post.html'
    success_url = reverse_lazy('my_profile_teacher')
    
    def delete(self, request, *args, **kwargs):
        """Override para añadir mensaje de éxito."""
        messages.success(request, "El post del blog ha sido eliminado con éxito.")
        return super().delete(request, *args, **kwargs)


class BlogPostDetailView(DetailView):
    """Vista para mostrar un blog post individual."""
    
    model = BlogPost
    template_name = 'teacher_blog/view_blog_post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class TeacherBlogPostListView(ListView):
    """Vista para mostrar todos los blog posts de un teacher específico."""
    
    model = BlogPost
    template_name = 'teacher_blog/teacher_blog_posts.html'
    context_object_name = 'blog_posts'
    paginate_by = 10  # Paginación automática
    
    def get_queryset(self):
        """Filtra los blog posts por teacher."""
        self.teacher = get_object_or_404(Teacher, id=self.kwargs['teacher_id'])
        return BlogPost.objects.filter(teacher=self.teacher).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Añade el teacher al contexto."""
        context = super().get_context_data(**kwargs)
        context['teacher'] = self.teacher
        return context


# ================================================================
# VISTAS BASADAS EN FUNCIONES (MANTENIDAS PARA COMPATIBILIDAD)
# ================================================================

@login_required
def create_blog_post(request):
    """Vista legacy - redirige a la nueva CBV."""
    return BlogPostCreateView.as_view()(request)


@login_required
def edit_blog_post(request, pk):
    """Vista legacy - redirige a la nueva CBV."""
    return BlogPostUpdateView.as_view()(request, pk=pk)


@login_required
def delete_blog_post(request, pk):
    """Vista legacy - redirige a la nueva CBV."""
    return BlogPostDeleteView.as_view()(request, pk=pk)


def teacher_blog_posts(request, teacher_id):
    """Vista legacy - redirige a la nueva CBV."""
    return TeacherBlogPostListView.as_view()(request, teacher_id=teacher_id)


def view_blog_post(request, post_id):
    """Vista legacy - redirige a la nueva CBV."""
    return BlogPostDetailView.as_view()(request, post_id=post_id)