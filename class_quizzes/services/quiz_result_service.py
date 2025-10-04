"""
Servicio para el manejo de resultados de quizzes.

Esta clase maneja la persistencia y recuperación de resultados de quizzes
de los estudiantes.
"""

from typing import List, Optional
from django.shortcuts import get_object_or_404
from ..models import QuizResult, Quiz
from users.models import Student
from .interfaces import QuizResultServiceInterface


class QuizResultService(QuizResultServiceInterface):
    """Implementación del servicio de resultados de quizzes."""
    
    def save_quiz_result(self, student_id: int, quiz_id: int, score: int, 
                        total_questions: int, correct_answers: int) -> QuizResult:
        """
        Guarda el resultado de un quiz.
        
        Args:
            student_id: ID del estudiante
            quiz_id: ID del quiz
            score: Puntaje obtenido
            total_questions: Número total de preguntas
            correct_answers: Número de respuestas correctas
            
        Returns:
            QuizResult: El resultado guardado
        """
        student = get_object_or_404(Student, id=student_id)
        quiz = get_object_or_404(Quiz, id=quiz_id)
        
        return QuizResult.objects.create(
            student=student,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers
        )
    
    def get_student_quiz_result(self, student_id: int, quiz_id: int) -> Optional[QuizResult]:
        """
        Obtiene el resultado de un estudiante en un quiz específico.
        
        Args:
            student_id: ID del estudiante
            quiz_id: ID del quiz
            
        Returns:
            QuizResult o None: El último resultado del estudiante en el quiz
        """
        student = get_object_or_404(Student, id=student_id)
        quiz = get_object_or_404(Quiz, id=quiz_id)
        
        return QuizResult.objects.filter(student=student, quiz=quiz).last()
    
    def get_student_completed_quizzes(self, student_id: int) -> List[QuizResult]:
        """
        Obtiene todos los quizzes completados por un estudiante.
        
        Args:
            student_id: ID del estudiante
            
        Returns:
            List[QuizResult]: Lista de resultados de quizzes completados
        """
        student = get_object_or_404(Student, id=student_id)
        return list(QuizResult.objects.filter(student=student))
