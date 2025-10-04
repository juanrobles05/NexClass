"""
Factory para la inyección de dependencias.

Esta clase centraliza la creación de servicios y maneja la inyección de dependencias,
permitiendo fácil intercambio de implementaciones para testing o diferentes entornos.
"""

from .interfaces import (
    QuizRepositoryInterface,
    QuizEvaluationServiceInterface,
    QuizResultServiceInterface,
    SessionManagerInterface,
    UserServiceInterface
)
from .quiz_repository import QuizRepository
from .quiz_evaluation_service import QuizEvaluationService
from .quiz_result_service import QuizResultService
from .session_manager import SessionManager
from .user_service import UserService


class ServiceFactory:
    """Factory para crear instancias de servicios."""
    
    _quiz_repository: QuizRepositoryInterface = None
    _quiz_evaluation_service: QuizEvaluationServiceInterface = None
    _quiz_result_service: QuizResultServiceInterface = None
    _session_manager: SessionManagerInterface = None
    _user_service: UserServiceInterface = None
    
    @classmethod
    def get_quiz_repository(cls) -> QuizRepositoryInterface:
        """Obtiene una instancia del repositorio de quizzes."""
        if cls._quiz_repository is None:
            cls._quiz_repository = QuizRepository()
        return cls._quiz_repository
    
    @classmethod
    def get_quiz_evaluation_service(cls) -> QuizEvaluationServiceInterface:
        """Obtiene una instancia del servicio de evaluación."""
        if cls._quiz_evaluation_service is None:
            cls._quiz_evaluation_service = QuizEvaluationService()
        return cls._quiz_evaluation_service
    
    @classmethod
    def get_quiz_result_service(cls) -> QuizResultServiceInterface:
        """Obtiene una instancia del servicio de resultados."""
        if cls._quiz_result_service is None:
            cls._quiz_result_service = QuizResultService()
        return cls._quiz_result_service
    
    @classmethod
    def get_session_manager(cls) -> SessionManagerInterface:
        """Obtiene una instancia del manejador de sesiones."""
        if cls._session_manager is None:
            cls._session_manager = SessionManager()
        return cls._session_manager
    
    @classmethod
    def get_user_service(cls) -> UserServiceInterface:
        """Obtiene una instancia del servicio de usuarios."""
        if cls._user_service is None:
            cls._user_service = UserService()
        return cls._user_service
    
    @classmethod
    def set_quiz_repository(cls, repository: QuizRepositoryInterface) -> None:
        """Permite inyectar una implementación personalizada del repositorio."""
        cls._quiz_repository = repository
    
    @classmethod
    def set_quiz_evaluation_service(cls, service: QuizEvaluationServiceInterface) -> None:
        """Permite inyectar una implementación personalizada del servicio de evaluación."""
        cls._quiz_evaluation_service = service
    
    @classmethod
    def set_quiz_result_service(cls, service: QuizResultServiceInterface) -> None:
        """Permite inyectar una implementación personalizada del servicio de resultados."""
        cls._quiz_result_service = service
    
    @classmethod
    def set_session_manager(cls, manager: SessionManagerInterface) -> None:
        """Permite inyectar una implementación personalizada del manejador de sesiones."""
        cls._session_manager = manager
    
    @classmethod
    def set_user_service(cls, service: UserServiceInterface) -> None:
        """Permite inyectar una implementación personalizada del servicio de usuarios."""
        cls._user_service = service
    
    @classmethod
    def reset(cls) -> None:
        """Resetea todas las instancias (útil para testing)."""
        cls._quiz_repository = None
        cls._quiz_evaluation_service = None
        cls._quiz_result_service = None
        cls._session_manager = None
        cls._user_service = None
