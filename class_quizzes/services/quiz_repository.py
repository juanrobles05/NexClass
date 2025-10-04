"""
Implementación concreta del repositorio para operaciones de datos de Quiz.

Esta clase implementa QuizRepositoryInterface y maneja todas las operaciones
de acceso a datos relacionadas con quizzes, preguntas y respuestas.
"""

from typing import List, Any
from django.shortcuts import get_object_or_404
from ..models import Quiz, Question, Answer
from .interfaces import QuizRepositoryInterface


class QuizRepository(QuizRepositoryInterface):
    """Implementación concreta del repositorio de Quiz."""
    
    def get_quiz_by_id(self, quiz_id: int) -> Quiz:
        """Obtiene un quiz por su ID."""
        return get_object_or_404(Quiz, id=quiz_id)
    
    def get_questions_by_quiz(self, quiz_id: int) -> List[Question]:
        """Obtiene todas las preguntas de un quiz."""
        return list(Question.objects.filter(quiz_id=quiz_id))
    
    def get_answers_by_question(self, question_id: int) -> List[Answer]:
        """Obtiene todas las respuestas de una pregunta."""
        question = get_object_or_404(Question, id=question_id)
        return list(question.answers.all())
    
    def create_question(self, quiz_id: int, question_text: str) -> Question:
        """Crea una nueva pregunta."""
        quiz = self.get_quiz_by_id(quiz_id)
        return Question.objects.create(text=question_text, quiz=quiz)
    
    def create_answer(self, question_id: int, answer_text: str, is_correct: bool) -> Answer:
        """Crea una nueva respuesta."""
        question = get_object_or_404(Question, id=question_id)
        return Answer.objects.create(
            question=question, 
            text=answer_text, 
            is_correct=is_correct
        )
