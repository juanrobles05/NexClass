# NexClass

**NexClass** es una aplicación web innovadora y completa cuyo objetivo es transformar los métodos de aprendizaje mediante el uso de tecnologías que conectan a estudiantes con una amplia red de educadores calificados.

La misión del proyecto es ofrecer una plataforma versátil que responda a las necesidades cambiantes de los aprendices de todas las edades y contextos, brindando acceso a instrucción experta en materias académicas, música, deporte, desarrollo profesional y mucho más.

---

## Alcance del Proyecto

El alcance de **NexClass** está definido como el desarrollo de un software web que actúe como un **mercado integral de servicios educativos**.

* Permite a los usuarios crear y administrar perfiles.
* Búsqueda de profesores con distintos filtros.
* Reserva de clases y sesiones.
* Comparación de instructores y calificación de servicios.
* Integración con herramientas de comunicación (Meet).
* Sistema de recursos y quizzes para los estudiantes.
* Blogs personales para docentes.
* Notificaciones y rankings.

El sistema busca ser **seguro, escalable y fácil de usar**, priorizando la protección de datos y ofreciendo una experiencia de usuario confiable.

---

# Actividad 2 Revisión autocritica

Usabilidad

El sistema presenta una interfaz minimalista y clara, con navegación sencilla mediante un menú superior. La personalización con el nombre del usuario y la implementación del modo claro/oscuro son fortalezas que enriquecen la experiencia.

Fortalezas: diseño limpio, navegación intuitiva, personalización de tema.
Aspectos a mejorar: contraste en algunos elementos del modo oscuro.
Observación: el chat inicial no especifica claramente su propósito, lo que puede generar confusión en nuevos usuarios (si es de soporte, de IA o de interacción con docentes).
Otro aspecto a mejorar: el botón de traducción no traduce correctamente todo el contenido de la página, lo que afecta la consistencia en la usabilidad para usuarios que no manejan el idioma original.
Compatibilidad

La aplicación funciona en navegadores modernos y es responsive en distintos tamaños de pantalla.

Fortalezas: diseño adaptable (responsive).
Aspectos a mejorar: se requieren pruebas adicionales en dispositivos móviles y navegadores menos comunes como Safari, donde pueden presentarse inconsistencias visuales.
Rendimiento

Un análisis con Lighthouse arrojó un puntaje de 68/100 en rendimiento, lo cual es aceptable pero con espacio para mejorar.

Resultados clave:

First Contentful Paint (FCP): 1.1s
Largest Contentful Paint (LCP): 1.1s
Speed Index: 1.2s
Cumulative Layout Shift (CLS): 0
Total Blocking Time (TBT): 860ms (alto, afecta interactividad).

Aunque los tiempos iniciales de carga son buenos, el bloqueo del hilo principal reduce la fluidez. Se recomienda:

Optimizar el JavaScript.
Implementar lazy loading de recursos.
Dividir bundles pesados en partes más pequeñas.
Seguridad

El sistema implementa un manejo adecuado de contraseñas, utilizando hash seguro para su almacenamiento.

Fortalezas: autenticación con hash y manejo básico de accesos.
Aspectos a mejorar:
Reforzar validaciones en formularios para prevenir inyecciones SQL/XSS.
Evitar mostrar mensajes de error técnicos al usuario final.