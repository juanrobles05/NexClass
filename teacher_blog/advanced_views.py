"""
Class-Based Views avanzadas que demuestran patrones Django más sofisticados.

Este archivo muestra CBVs adicionales que aprovechan características avanzadas
como filtrado, búsqueda, paginación y mixins personalizados.
"""

from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import BlogPost
from .forms import BlogPostSearchForm
from users.models import Teacher


class BlogPostListView(ListView):
    """Vista lista avanzada con filtrado, búsqueda y paginación."""
    
    model = BlogPost
    template_name = 'teacher_blog/blog_post_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 6
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Aplica filtros y búsqueda al queryset."""
        queryset = super().get_queryset()
        
        # Filtro por teacher si se especifica
        teacher_id = self.request.GET.get('teacher')
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        
        # Búsqueda por texto
        search_query = self.request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )
        
        return queryset.select_related('teacher__user')
    
    def get_context_data(self, **kwargs):
        """Añade formulario de búsqueda y estadísticas al contexto."""
        context = super().get_context_data(**kwargs)
        
        # Formulario de búsqueda
        teachers_with_posts = Teacher.objects.filter(
            blog_posts__isnull=False
        ).distinct()
        
        context['search_form'] = BlogPostSearchForm(
            data=self.request.GET or None,
            teachers_queryset=teachers_with_posts
        )
        
        # Estadísticas
        context['total_posts'] = BlogPost.objects.count()
        context['total_teachers'] = teachers_with_posts.count()
        
        return context


class BlogPostStatsView(LoginRequiredMixin, TemplateView):
    """Vista que muestra estadísticas avanzadas de blog posts."""
    
    template_name = 'teacher_blog/blog_stats.html'
    
    def get_context_data(self, **kwargs):
        """Calcula y proporciona estadísticas detalladas."""
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        total_posts = BlogPost.objects.count()
        total_teachers_with_posts = Teacher.objects.filter(
            blog_posts__isnull=False
        ).distinct().count()
        
        # Posts recientes (última semana)
        last_week = timezone.now() - timedelta(days=7)
        recent_posts = BlogPost.objects.filter(created_at__gte=last_week).count()
        
        # Teachers más activos
        top_teachers = Teacher.objects.annotate(
            post_count=Count('blog_posts')
        ).filter(post_count__gt=0).order_by('-post_count')[:5]
        
        # Posts más recientes
        latest_posts = BlogPost.objects.select_related(
            'teacher__user'
        ).order_by('-created_at')[:10]
        
        context.update({
            'total_posts': total_posts,
            'total_teachers_with_posts': total_teachers_with_posts,
            'recent_posts_count': recent_posts,
            'top_teachers': top_teachers,
            'latest_posts': latest_posts,
            'stats_generated_at': timezone.now(),
        })
        
        return context


class MyBlogPostsView(LoginRequiredMixin, ListView):
    """Vista para que los teachers vean sus propios posts."""
    
    model = BlogPost
    template_name = 'teacher_blog/my_blog_posts.html'
    context_object_name = 'my_posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Filtra solo los posts del teacher autenticado."""
        if not hasattr(self.request.user, 'teacher'):
            return BlogPost.objects.none()
        
        return BlogPost.objects.filter(
            teacher=self.request.user.teacher
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Añade estadísticas personales del teacher."""
        context = super().get_context_data(**kwargs)
        
        if hasattr(self.request.user, 'teacher'):
            teacher = self.request.user.teacher
            
            # Estadísticas personales
            total_posts = self.get_queryset().count()
            this_month = timezone.now().replace(day=1)
            posts_this_month = self.get_queryset().filter(
                created_at__gte=this_month
            ).count()
            
            context.update({
                'total_my_posts': total_posts,
                'posts_this_month': posts_this_month,
                'teacher': teacher,
            })
        
        return context


class BlogPostArchiveView(ListView):
    """Vista que muestra posts organizados por fecha."""
    
    model = BlogPost
    template_name = 'teacher_blog/blog_archive.html'
    context_object_name = 'posts_by_month'
    
    def get_queryset(self):
        """Organiza posts por mes y año."""
        return BlogPost.objects.extra(
            select={
                'month': "DATE_FORMAT(created_at, '%%Y-%%m')",
                'year': "DATE_FORMAT(created_at, '%%Y')",
            }
        ).values('month', 'year').annotate(
            post_count=Count('id')
        ).order_by('-year', '-month')
    
    def get_context_data(self, **kwargs):
        """Añade información adicional sobre el archivo."""
        context = super().get_context_data(**kwargs)
        
        # Obtener años únicos para navegación
        years = BlogPost.objects.extra(
            select={'year': "DATE_FORMAT(created_at, '%%Y')"}
        ).values('year').distinct().order_by('-year')
        
        context['years'] = [item['year'] for item in years]
        
        return context


# ================================================================
# MIXINS AVANZADOS PARA REUTILIZACIÓN
# ================================================================

class BlogPostContextMixin:
    """Mixin que añade contexto común a las vistas de blog."""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Añadir información común
        context['total_blog_posts'] = BlogPost.objects.count()
        context['recent_posts'] = BlogPost.objects.select_related(
            'teacher__user'
        ).order_by('-created_at')[:3]
        
        return context


class TeacherPostsFilterMixin:
    """Mixin para filtrar posts por teacher en las URLs."""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        teacher_id = self.kwargs.get('teacher_id')
        
        if teacher_id:
            self.teacher = get_object_or_404(Teacher, id=teacher_id)
            queryset = queryset.filter(teacher=self.teacher)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'teacher'):
            context['teacher'] = self.teacher
        return context
