
from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    """Formulario mejorado para BlogPost con estilos Bootstrap."""
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-info-subtle',
                'placeholder': 'Título del post',
                'maxlength': '200'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-info-subtle',
                'placeholder': 'Contenido del post...',
                'rows': 8
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control bg-info-subtle',
                'placeholder': 'https://ejemplo.com (opcional)'
            }),
        }
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'url': 'URL de referencia (opcional)',
        }
    
    def clean_title(self):
        """Validación personalizada para el título."""
        title = self.cleaned_data.get('title')
        if title and len(title) < 5:
            raise forms.ValidationError('El título debe tener al menos 5 caracteres.')
        return title
    
    def clean_content(self):
        """Validación personalizada para el contenido."""
        content = self.cleaned_data.get('content')
        if content and len(content) < 20:
            raise forms.ValidationError('El contenido debe tener al menos 20 caracteres.')
        return content


class BlogPostSearchForm(forms.Form):
    """Formulario para búsqueda de blog posts (complementa las CBVs)."""
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar en posts...',
            'autocomplete': 'off'
        }),
        label='Buscar'
    )
    
    teacher = forms.ModelChoiceField(
        queryset=None,  # Se define en la vista
        required=False,
        empty_label="Todos los profesores",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Profesor'
    )
    
    def __init__(self, *args, **kwargs):
        teachers_queryset = kwargs.pop('teachers_queryset', None)
        super().__init__(*args, **kwargs)
        if teachers_queryset:
            self.fields['teacher'].queryset = teachers_queryset
