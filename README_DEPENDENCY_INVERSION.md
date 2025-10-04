# Inversión de Dependencias en el Módulo class_quizzes

## Introducción

Este documento documenta la implementación del **Principio de Inversión de Dependencias (DIP)** en el módulo `class_quizzes` del proyecto NexClass. La refactorización se realizó como parte de la Actividad 3, transformando un código fuertemente acoplado en una arquitectura más flexible, testeable y mantenible.

## Problemas Identificados

### 1. Acoplamiento Fuerte en las Vistas

**Archivo**: `views.py` (Original)

```python
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)  # Dependencia directa del modelo
    questions = Question.objects.filter(quiz=quiz)  # Acceso directo a ORM
    student = Student.objects.get(user=request.user)  # Dependencia externa

    # Lógica de negocio mezclada con acceso a datos
    if 'correct_answers' not in request.session:
        request.session['correct_answers'] = 0

    # Cálculo de puntaje embebido en la vista
    score = int((correct_answers / total_questions) * 100)

    # Creación directa de objetos
    QuizResult.objects.create(
        student=student,
        quiz=quiz,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_answers
    )
```

### 2. Violaciones Específicas del DIP

- **Dependencias directas**: Las vistas dependen directamente de modelos concretos
- **Lógica de negocio dispersa**: Cálculos y validaciones mezclados con código de vista
- **Bajo cohesión**: Múltiples responsabilidades en una sola función
- **Alta rigidez**: Cambios en modelos requieren cambios en vistas

### 3. Dependencias Problemáticas Identificadas

```python
# Dependencias externas directas
from users.models import Student, Teacher
from classCreation_Schedules.models import Class

# Uso directo de ORM en vistas
Quiz.objects.filter(...)
Question.objects.create(...)
Answer.objects.get(...)
QuizResult.objects.filter(...)
```

## Solución Implementada

### 1. Componentes Creados

#### A. Interfaces/Protocolos (`services/interfaces.py`)

```python
class QuizRepositoryInterface(Protocol):
    """Abstracción para operaciones de datos de Quiz."""
    def get_quiz_by_id(self, quiz_id: int) -> Any: ...
    def get_questions_by_quiz(self, quiz_id: int) -> List[Any]: ...
    def create_question(self, quiz_id: int, question_text: str) -> Any: ...

class QuizEvaluationServiceInterface(Protocol):
    """Abstracción para lógica de evaluación."""
    def evaluate_answer(self, answer_id: int) -> bool: ...
    def calculate_score(self, correct_answers: int, total_questions: int) -> int: ...

class QuizResultServiceInterface(Protocol):
    """Abstracción para manejo de resultados."""
    def save_quiz_result(self, student_id: int, quiz_id: int, ...) -> Any: ...
```

#### B. Implementaciones Concretas

**Repository Pattern** (`services/quiz_repository.py`):
```python
class QuizRepository(QuizRepositoryInterface):
    def get_quiz_by_id(self, quiz_id: int) -> Quiz:
        return get_object_or_404(Quiz, id=quiz_id)
    
    def create_question(self, quiz_id: int, question_text: str) -> Question:
        quiz = self.get_quiz_by_id(quiz_id)
        return Question.objects.create(text=question_text, quiz=quiz)
```

**Service Layer** (`services/quiz_evaluation_service.py`):
```python
class QuizEvaluationService(QuizEvaluationServiceInterface):
    def calculate_score(self, correct_answers: int, total_questions: int) -> int:
        if total_questions == 0:
            return 0
        return int((correct_answers / total_questions) * 100)
```

#### C. Factory para Inyección de Dependencias (`services/service_factory.py`)

```python
class ServiceFactory:
    @classmethod
    def get_quiz_repository(cls) -> QuizRepositoryInterface:
        if cls._quiz_repository is None:
            cls._quiz_repository = QuizRepository()
        return cls._quiz_repository
    
    @classmethod
    def set_quiz_repository(cls, repository: QuizRepositoryInterface) -> None:
        cls._quiz_repository = repository  # Para testing/mocking
```

## Estructura Antes vs Después

### ANTES - Estructura Monolítica
```
class_quizzes/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py          # Modelos con dependencias externas
├── tests.py
├── urls.py
├── views.py           # Vistas con lógica de negocio mezclada
├── __pycache__/
├── migrations/
└── templates/
```

### DESPUÉS - Estructura con Inversión de Dependencias
```
class_quizzes/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py          # Modelos puros
├── tests.py
├── urls.py
├── views.py           # Vistas refactorizadas con DI
├── views_original.py  # Backup del código original
├── services/          # NUEVA CAPA DE SERVICIOS
│   ├── __init__.py
│   ├── interfaces.py              # Abstracciones/Protocolos
│   ├── quiz_repository.py         # Patrón Repository
│   ├── quiz_evaluation_service.py # Lógica de evaluación
│   ├── quiz_result_service.py     # Manejo de resultados
│   ├── session_manager.py         # Gestión de sesiones
│   ├── user_service.py            # Operaciones de usuario
│   └── service_factory.py         # Factory para DI
├── __pycache__/
├── migrations/
└── templates/
```

## Código Antes vs Después

### Función `take_quiz` - ANTES

```python
def take_quiz(request, quiz_id):
    # PROBLEMA: Dependencias directas de módulos de bajo nivel
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    total_questions = questions.count()
    student = Student.objects.get(user=request.user)

    current_question_index = int(request.GET.get('question_index', 0))

    # PROBLEMA: Lógica de negocio en la vista
    if 'correct_answers' not in request.session:
        request.session['correct_answers'] = 0

    if current_question_index >= total_questions:
        # PROBLEMA: Cálculo de negocio embebido
        correct_answers = request.session['correct_answers']
        score = int((correct_answers / total_questions) * 100)

        # PROBLEMA: Creación directa de objetos
        QuizResult.objects.create(
            student=student,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers
        )

        del request.session['correct_answers']
        return redirect('quiz_result', quiz_id=quiz.id)

    current_question = questions[current_question_index]
    answers = current_question.answers.all()

    if request.method == 'POST':
        selected_answer_id = request.POST.get('answer')
        # PROBLEMA: Acceso directo al ORM
        selected_answer = Answer.objects.get(id=selected_answer_id)

        # PROBLEMA: Lógica de evaluación en la vista
        if selected_answer.is_correct:
            request.session['correct_answers'] += 1

        return redirect(f'{request.path}?question_index={current_question_index + 1}')

    # PROBLEMA: Cálculo directo en la vista
    progress = int((current_question_index + 1) / total_questions * 100)

    return render(request, 'take_quiz.html', {
        'quiz': quiz,
        'current_question': current_question,
        'answers': answers,
        'progress': progress,
        'current_question_index': current_question_index + 1,
        'total_questions': total_questions
    })
```

### Función `take_quiz` - DESPUÉS

```python
def take_quiz(request, quiz_id):
    # SOLUCIÓN: Inyección de dependencias - Alto nivel depende de abstracciones
    quiz_repository = ServiceFactory.get_quiz_repository()
    quiz_evaluation_service = ServiceFactory.get_quiz_evaluation_service()
    quiz_result_service = ServiceFactory.get_quiz_result_service()
    session_manager = ServiceFactory.get_session_manager()
    user_service = ServiceFactory.get_user_service()

    # SOLUCIÓN: Uso de abstracciones en lugar de implementaciones concretas
    quiz = quiz_repository.get_quiz_by_id(quiz_id)
    questions = quiz_repository.get_questions_by_quiz(quiz_id)
    total_questions = len(questions)
    student = user_service.get_student_by_user(request.user)

    current_question_index = int(request.GET.get('question_index', 0))

    # SOLUCIÓN: Delegación a servicio especializado
    session_manager.initialize_quiz_session(request)

    if current_question_index >= total_questions:
        # SOLUCIÓN: Lógica de negocio en servicios especializados
        correct_answers = session_manager.get_correct_answers(request)
        score = quiz_evaluation_service.calculate_score(correct_answers, total_questions)

        # SOLUCIÓN: Delegación a servicio de resultados
        quiz_result_service.save_quiz_result(
            student_id=student.id,
            quiz_id=quiz.id,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers
        )

        session_manager.clear_quiz_session(request)
        return redirect('quiz_result', quiz_id=quiz.id)

    current_question = questions[current_question_index]
    answers = quiz_repository.get_answers_by_question(current_question.id)

    if request.method == 'POST':
        selected_answer_id = request.POST.get('answer')

        # SOLUCIÓN: Evaluación a través de servicio especializado
        if quiz_evaluation_service.evaluate_answer(int(selected_answer_id)):
            session_manager.update_correct_answers(request)

        return redirect(f'{request.path}?question_index={current_question_index + 1}')

    # SOLUCIÓN: Cálculo delegado a servicio de evaluación
    progress = quiz_evaluation_service.get_quiz_progress(
        current_question_index + 1, 
        total_questions
    )

    return render(request, 'take_quiz.html', {
        'quiz': quiz,
        'current_question': current_question,
        'answers': answers,
        'progress': progress,
        'current_question_index': current_question_index + 1,
        'total_questions': total_questions
    })
```

## Beneficios Obtenidos

### 1. Flexibilidad y Mantenibilidad

**ANTES**: Cambiar la lógica de evaluación requería modificar las vistas
```python
# Cambio en el cálculo requiere editar la vista
score = int((correct_answers / total_questions) * 100)
```

**DESPUÉS**: Se puede cambiar la implementación sin tocar las vistas
```python
# Implementación alternativa sin cambiar vistas
class GenerousEvaluationService(QuizEvaluationServiceInterface):
    def calculate_score(self, correct_answers: int, total_questions: int) -> int:
        base_score = (correct_answers / total_questions) * 100
        return min(100, int(base_score + 5))  # Bonus de 5 puntos

# Cambiar implementación
ServiceFactory.set_quiz_evaluation_service(GenerousEvaluationService())
```
### 2.  Separación de Responsabilidades

**ANTES**: Una vista manejaba múltiples responsabilidades
- Acceso a datos
- Lógica de evaluación
- Manejo de sesiones
- Cálculo de puntajes
- Persistencia de resultados

**DESPUÉS**: Cada servicio tiene una responsabilidad específica
- `QuizRepository`: Solo acceso a datos
- `QuizEvaluationService`: Solo lógica de evaluación
- `SessionManager`: Solo manejo de sesiones
- `QuizResultService`: Solo manejo de resultados

### 3.  Inversión de Control

**ANTES**: Las vistas controlaban todas las dependencias
```python
# Vista controla la creación de dependencias
quiz = get_object_or_404(Quiz, id=quiz_id)
student = Student.objects.get(user=request.user)
```

**DESPUÉS**: Factory controla la inyección de dependencias
```python
# Factory maneja las dependencias
quiz_repository = ServiceFactory.get_quiz_repository()
user_service = ServiceFactory.get_user_service()
```

##  Conclusiones

###  Objetivos Cumplidos

1. **Inversión de Dependencias Implementada**: Las vistas ya no dependen directamente de modelos concretos, sino de abstracciones.

2. **Arquitectura Mejorada**: Se implementó una arquitectura por capas con separación clara de responsabilidades.

3. **Flexibilidad Aumentada**: Se pueden cambiar implementaciones sin modificar código de alto nivel.

4. **Mantenibilidad Mejorada**: Cada componente tiene una responsabilidad específica y bien definida.