from django.shortcuts import render, redirect, get_object_or_404
from users.models import Teacher
from .models import TeacherRating
from .forms import TeacherRatingForm
from django.contrib.auth.decorators import login_required

@login_required
def rate_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    student = request.user.student  # Asumiendo que el usuario está autenticado como estudiante

    # Intenta recuperar una calificación existente
    try:
        rating = TeacherRating.objects.get(teacher=teacher, student=student)
        form = TeacherRatingForm(instance=rating)  # Prepara el formulario con la calificación existente
    except TeacherRating.DoesNotExist:
        rating = None
        form = TeacherRatingForm()

    if request.method == 'POST':
        form = TeacherRatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.teacher = teacher
            rating.student = student
            
            # Mostrar información del patrón Observer antes de guardar
            observers_count = len(TeacherRating._observers)
            observer_names = [obs.__class__.__name__ for obs in TeacherRating._observers]
            
            print(f"PATRÓN OBSERVER ACTIVADO:")
            print(f"   Se notificará a {observers_count} observadores")
            print(f"   Observadores: {', '.join(observer_names)}")
            print(f"   Nueva calificación: {rating.rating}/5 para {teacher.user.name}")
            
            # Al guardar, automáticamente se ejecuta el patrón Observer
            rating.save()  # Esto dispara notify_observers() automáticamente
            
            return redirect('teachers_detail', teacher_id=teacher.id)

    # Información del patrón Observer para mostrar en el template
    observers_info = []
    for obs in TeacherRating._observers:
        description = 'Sin descripción'
        if obs.__doc__:
            lines = obs.__doc__.split('\n')
            # Buscar la primera línea no vacía después de la primera
            for i in range(1, len(lines)):
                if lines[i].strip():
                    description = lines[i].strip()
                    break
            # Si no hay líneas adicionales, usar la primera línea
            if description == 'Sin descripción' and lines[0].strip():
                description = lines[0].strip()
        
        observers_info.append({
            'name': obs.__class__.__name__,
            'description': description
        })
    
    return render(request, 'rate_teacher.html', {
        'form': form, 
        'teacher': teacher,
        'observers_count': len(TeacherRating._observers),
        'observers_info': observers_info,
        'pattern_demo': True
    })
