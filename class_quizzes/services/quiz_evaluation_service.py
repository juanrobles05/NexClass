"""
Servicio de evaluación de quizzes.

Esta clase maneja toda la lógica de negocio relacionada con la evaluación
de quizzes, cálculo de puntajes y progreso.
"""

from django.shortcuts import get_object_or_404
from ..models import Answer
from .interfaces import QuizEvaluationServiceInterface


class QuizEvaluationService(QuizEvaluationServiceInterface):
    """Implementación del servicio de evaluación de quizzes."""
    
    def evaluate_answer(self, answer_id: int) -> bool:
        """
        Evalúa si una respuesta es correcta.
        
        Args:
            answer_id: ID de la respuesta seleccionada
            
        Returns:
            bool: True si la respuesta es correcta, False en caso contrario
        """
        answer = get_object_or_404(Answer, id=answer_id)
        return answer.is_correct
    
    def calculate_score(self, correct_answers: int, total_questions: int) -> int:
        """
        Calcula el puntaje basado en respuestas correctas.
        
        Args:
            correct_answers: Número de respuestas correctas
            total_questions: Número total de preguntas
            
        Returns:
            int: Puntaje calculado (0-100)
        """
        if total_questions == 0:
            return 0
        return int((correct_answers / total_questions) * 100)
    
    def get_quiz_progress(self, current_question: int, total_questions: int) -> int:
        """
        Calcula el progreso del quiz en porcentaje.
        
        Args:
            current_question: Número de pregunta actual (1-indexed)
            total_questions: Número total de preguntas
            
        Returns:
            int: Progreso en porcentaje (0-100)
        """
        if total_questions == 0:
            return 0
        return int((current_question / total_questions) * 100)
