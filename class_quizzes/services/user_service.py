"""
Servicio para operaciones relacionadas con usuarios.

Esta clase maneja la obtención de información de estudiantes y profesores.
"""

from django.shortcuts import get_object_or_404
from users.models import Student, Teacher
from .interfaces import UserServiceInterface


class UserService(UserServiceInterface):
    """Implementación del servicio de usuarios."""
    
    def get_student_by_user(self, user) -> Student:
        """
        Obtiene un estudiante por su usuario.
        
        Args:
            user: Usuario de Django
            
        Returns:
            Student: El estudiante asociado al usuario
        """
        return get_object_or_404(Student, user=user)
    
    def get_teacher_by_user(self, user) -> Teacher:
        """
        Obtiene un profesor por su usuario.
        
        Args:
            user: Usuario de Django
            
        Returns:
            Teacher: El profesor asociado al usuario
        """
        return get_object_or_404(Teacher, user=user)
