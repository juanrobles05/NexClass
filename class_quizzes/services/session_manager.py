"""
Servicio para el manejo de sesiones durante la evaluación de quizzes.

Esta clase maneja el estado de la sesión durante la realización de un quiz.
"""

from django.http import HttpRequest
from .interfaces import SessionManagerInterface


class SessionManager(SessionManagerInterface):
    """Implementación del manejador de sesiones para quizzes."""
    
    CORRECT_ANSWERS_KEY = 'correct_answers'
    
    def initialize_quiz_session(self, request: HttpRequest) -> None:
        """
        Inicializa una sesión de quiz.
        
        Args:
            request: HttpRequest object
        """
        if self.CORRECT_ANSWERS_KEY not in request.session:
            request.session[self.CORRECT_ANSWERS_KEY] = 0
    
    def update_correct_answers(self, request: HttpRequest, increment: int = 1) -> None:
        """
        Actualiza el conteo de respuestas correctas en la sesión.
        
        Args:
            request: HttpRequest object
            increment: Cantidad a incrementar (default: 1)
        """
        self.initialize_quiz_session(request)
        request.session[self.CORRECT_ANSWERS_KEY] += increment
    
    def get_correct_answers(self, request: HttpRequest) -> int:
        """
        Obtiene el conteo actual de respuestas correctas.
        
        Args:
            request: HttpRequest object
            
        Returns:
            int: Número de respuestas correctas
        """
        self.initialize_quiz_session(request)
        return request.session[self.CORRECT_ANSWERS_KEY]
    
    def clear_quiz_session(self, request: HttpRequest) -> None:
        """
        Limpia la sesión del quiz.
        
        Args:
            request: HttpRequest object
        """
        if self.CORRECT_ANSWERS_KEY in request.session:
            del request.session[self.CORRECT_ANSWERS_KEY]
