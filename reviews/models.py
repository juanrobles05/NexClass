from django.db import models
from users.models import Teacher, Student
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


class RatingObserver:
    """
    Patrón Observer - Interfaz base para observadores de calificaciones.
    
    El patrón Observer permite definir una dependencia uno-a-muchos entre objetos,
    de manera que cuando un objeto cambia de estado, todos sus dependientes son
    notificados y actualizados automáticamente.
    
    En este caso, cuando se crea una calificación (Subject), múltiples observadores
    son notificados para realizar acciones específicas.
    """
    def update(self, rating):
        """Método que debe implementar cada observador concreto"""
        raise NotImplementedError("Los observadores deben implementar el método update()")


class EmailNotificationObserver(RatingObserver):
    """Observer concreto que envía notificaciones por email al profesor"""
    
    def update(self, rating):
        """Envía email al profesor notificando la nueva calificación"""
        print(f"🔔 Observer EMAIL activado para rating ID {rating.id}")
        print(f"📧 Intentando enviar email a: {rating.teacher.user.email}")
        
        try:
            subject = f"Nueva calificación recibida - {rating.rating}/5 estrellas"
            message = f"""
            Hola {rating.teacher.user.name},
            
            Has recibido una nueva calificación:
            
            Estudiante: {rating.student.user.name}
            Calificación: {rating.rating}/5 estrellas
            Comentario: {rating.comment or 'Sin comentario'}
            Fecha: {rating.created_at.strftime('%d/%m/%Y %H:%M')}
            
            ¡Sigue brindando excelente educación!
            
            Saludos,
            El equipo de NexClass
            """
            
            print(f"📝 Preparando email:")
            print(f"   Asunto: {subject}")
            print(f"   Para: {rating.teacher.user.email}")
            print(f"   Desde: {settings.DEFAULT_FROM_EMAIL}")
            
            result = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[rating.teacher.user.email],
                fail_silently=False
            )
            
            if result == 1:
                print(f"✅ Email enviado exitosamente a {rating.teacher.user.email}")
            else:
                print(f"⚠️ Email no pudo ser enviado. Resultado: {result}")
                
        except Exception as e:
            print(f"❌ Error enviando email: {e}")
            print(f"❌ Tipo de error: {type(e).__name__}")
            import traceback
            print(f"❌ Traceback: {traceback.format_exc()}")


class StatisticsUpdateObserver(RatingObserver):
    """Observer concreto que actualiza estadísticas del profesor"""
    
    def update(self, rating):
        """Actualiza el promedio de calificaciones del profesor"""
        print(f"📊 Observer ESTADÍSTICAS activado para rating ID {rating.id}")
        try:
            teacher = rating.teacher
            all_ratings = teacher.ratings.all()
            if all_ratings:
                average = sum(r.rating for r in all_ratings) / all_ratings.count()
                teacher.average_rating = round(average, 2)
                teacher.save()
                print(f"✅ Estadísticas actualizadas para {teacher.user.name}: {average:.2f}")
        except Exception as e:
            print(f"❌ Error actualizando estadísticas: {e}")


class ActivityLogObserver(RatingObserver):
    """Observer concreto que registra la actividad en logs"""
    
    def update(self, rating):
        """Registra la nueva calificación en el log de actividad"""
        print(f"📝 Observer LOG activado para rating ID {rating.id}")
        try:
            log_message = (
                f"[{timezone.now()}] Nueva calificación: "
                f"{rating.student.user.username} calificó a "
                f"{rating.teacher.user.username} con {rating.rating}/5"
            )
            print(f"📝 LOG: {log_message}")
            
            # Aquí podrías escribir a un archivo de log o base de datos
            # Por ahora solo imprimimos en consola para demostración
        except Exception as e:
            print(f"❌ Error en log: {e}")


class TeacherRating(models.Model):
    """
    Modelo Subject del patrón Observer.
    
    Mantiene una lista de observadores y los notifica cuando se crea una nueva calificación.
    """
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ratings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Lista de observadores (patrón Observer)
    _observers = []
    
    class Meta:
        unique_together = ('teacher', 'student')  # Un estudiante solo puede calificar a un profesor una vez
    
    @classmethod
    def add_observer(cls, observer):
        """Agrega un observador a la lista de notificación"""
        if observer not in cls._observers:
            cls._observers.append(observer)
            print(f"👁️ Observer agregado: {observer.__class__.__name__}")
    
    @classmethod
    def remove_observer(cls, observer):
        """Remueve un observador de la lista"""
        if observer in cls._observers:
            cls._observers.remove(observer)
            print(f"🚫 Observer removido: {observer.__class__.__name__}")
    
    def notify_observers(self):
        """Notifica a todos los observadores sobre la nueva calificación"""
        print(f"📢 Notificando a {len(self._observers)} observadores...")
        for observer in self._observers:
            try:
                observer.update(self)
            except Exception as e:
                print(f"❌ Error en observer {observer.__class__.__name__}: {e}")
    
    def save(self, *args, **kwargs):
        """Override del método save para implementar el patrón Observer"""
        # Verificar si es una nueva calificación
        is_new = self.pk is None
        print(f"💾 TeacherRating.save() llamado - is_new: {is_new}, PK: {self.pk}")
        
        # Llamar al método save original
        super().save(*args, **kwargs)
        print(f"💾 Después de super().save() - PK: {self.pk}")
        
        # Ejecutar observers tanto para nuevas calificaciones como para actualizaciones
        if is_new:
            print(f"🚀 Ejecutando notify_observers() porque es una NUEVA calificación")
            self.notify_observers()
        else:
            print(f"🔄 Ejecutando notify_observers() porque es una ACTUALIZACIÓN de calificación")
            self.notify_observers()
    
    def __str__(self):
        return f"{self.student.user.username} -> {self.teacher.user.username}: {self.rating}/5"


# Auto-registro de observadores cuando se importa el módulo
# Esto demuestra el patrón Observer en acción
TeacherRating.add_observer(EmailNotificationObserver())
TeacherRating.add_observer(StatisticsUpdateObserver())
TeacherRating.add_observer(ActivityLogObserver())
