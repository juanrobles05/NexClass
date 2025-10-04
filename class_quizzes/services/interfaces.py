"""
Interfaces y protocolos para la inversión de dependencias en el módulo class_quizzes.

Este módulo define las abstracciones que seguirán las implementaciones concretas,
cumpliendo con el Principio de Inversión de Dependencias (DIP).
"""

from typing import Protocol, List, Optional, Dict, Any
from django.http import HttpRequest


class QuizRepositoryInterface(Protocol):
    """Interfaz para operaciones de datos relacionadas con Quiz."""
    
    def get_quiz_by_id(self, quiz_id: int) -> Any:
        """Obtiene un quiz por su ID."""
        ...
    
    def get_questions_by_quiz(self, quiz_id: int) -> List[Any]:
        """Obtiene todas las preguntas de un quiz."""
        ...
    
    def get_answers_by_question(self, question_id: int) -> List[Any]:
        """Obtiene todas las respuestas de una pregunta."""
        ...
    
    def create_question(self, quiz_id: int, question_text: str) -> Any:
        """Crea una nueva pregunta."""
        ...
    
    def create_answer(self, question_id: int, answer_text: str, is_correct: bool) -> Any:
        """Crea una nueva respuesta."""
        ...


class QuizEvaluationServiceInterface(Protocol):
    """Interfaz para la lógica de evaluación de quizzes."""
    
    def evaluate_answer(self, answer_id: int) -> bool:
        """Evalúa si una respuesta es correcta."""
        ...
    
    def calculate_score(self, correct_answers: int, total_questions: int) -> int:
        """Calcula el puntaje basado en respuestas correctas."""
        ...
    
    def get_quiz_progress(self, current_question: int, total_questions: int) -> int:
        """Calcula el progreso del quiz en porcentaje."""
        ...


class QuizResultServiceInterface(Protocol):
    """Interfaz para el manejo de resultados de quizzes."""
    
    def save_quiz_result(self, student_id: int, quiz_id: int, score: int, 
                        total_questions: int, correct_answers: int) -> Any:
        """Guarda el resultado de un quiz."""
        ...
    
    def get_student_quiz_result(self, student_id: int, quiz_id: int) -> Optional[Any]:
        """Obtiene el resultado de un estudiante en un quiz específico."""
        ...
    
    def get_student_completed_quizzes(self, student_id: int) -> List[Any]:
        """Obtiene todos los quizzes completados por un estudiante."""
        ...


class SessionManagerInterface(Protocol):
    """Interfaz para el manejo de sesiones durante la evaluación."""
    
    def initialize_quiz_session(self, request: HttpRequest) -> None:
        """Inicializa una sesión de quiz."""
        ...
    
    def update_correct_answers(self, request: HttpRequest, increment: int = 1) -> None:
        """Actualiza el conteo de respuestas correctas en la sesión."""
        ...
    
    def get_correct_answers(self, request: HttpRequest) -> int:
        """Obtiene el conteo actual de respuestas correctas."""
        ...
    
    def clear_quiz_session(self, request: HttpRequest) -> None:
        """Limpia la sesión del quiz."""
        ...


class UserServiceInterface(Protocol):
    """Interfaz para operaciones relacionadas con usuarios."""
    
    def get_student_by_user(self, user: Any) -> Any:
        """Obtiene un estudiante por su usuario."""
        ...
    
    def get_teacher_by_user(self, user: Any) -> Any:
        """Obtiene un profesor por su usuario."""
        ...
