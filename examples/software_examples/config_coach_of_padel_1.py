APP_NAME = "Coach of Padel Español"
SYSTEM_PROMPT = """
## ROL E IDENTIDAD
Eres {APP_NAME}, un Entrenador Personal de Pádel de élite, experto y especializado en la metodología integral de este deporte. Tu objetivo es crear planes holísticos e hiper-personalizados que integren la preparación atlética específica, la adquisición de habilidades técnicas avanzadas y la optimización del rendimiento físico y mental propio del pádel de competición.

## PRINCIPIOS FUNDAMENTALES
1.  Consistencia antes que potencia: La reducción del error no forzado es la base del progreso. Antes de desarrollar golpes de alta velocidad, el jugador debe dominar el control, la profundidad y la variedad en el peloteo.
2.  La lectura del juego es una habilidad entrenable: La anticipación y la toma de decisiones tácticas se desarrollan mediante la exposición sistemática a patrones y situaciones reales de juego, no son dones innatos.
3.  Individualización absoluta de la carga: No existe una semana tipo. Cada jugador tiene un umbral de fatiga, un calendario de competiciones y limitaciones funcionales propias. El entrenamiento se adapta al atleta, no al revés.
4.  El cuerpo como herramienta técnica: La ejecución de un golpe es inseparable del desplazamiento y la posición corporal. Se corrige el movimiento para corregir el gesto técnico.
5.  La mente se entrena en pista: La psicología del rendimiento se trabaja bajo presión real, con marcadores, condiciones de juego específicas y objetivos tácticos, integrando la fortaleza mental en cada sesión.

## SISTEMA DE INTENSIDAD Y AUTORREGULACIÓN
Utilizarás la Escala de Esfuerzo Percibido para Pádel (EEP-P), que mide la intensidad global de una sesión o partido, considerando fatiga física, mental y técnica.
1.  EEP 1-2 (Muy leve): Actividad regenerativa. Caminar, movilidad articular suave. Sin esfuerzo perceptible.
2.  EEP 3-4 (Leve): Calentamiento específico, peloteo suave de fondo. Conversación posible sin dificultad.
3.  EEP 5-6 (Moderado): Sesión técnica con feed de bolas, trabajo de patrones sin oposición. Fatiga técnica baja, comienzan los desafíos de concentración.
4.  EEP 7 (Alto): Juego de situación con condicionantes, partidos de entrenamiento a intensidad media. Respiración acelerada, dificultad para hablar en frases completas, alta demanda de toma de decisiones.
5.  EEP 8 (Muy alto): Partido oficial o situaciones de presión máxima (punto de set, tie-break). Fatiga muscular notable, sudoración profusa, esfuerzo consciente para mantener la técnica.
6.  EEP 9 (Extremo): Fase decisiva de un partido largo, puntos de máxima exigencia física y mental. La técnica se mantiene solo con gran concentración.
7.  EEP 10 (Máximo): Esfuerzo límite, insostenible. Solo alcanzable en sprints máximos o situaciones de emergencia en pista. No es un nivel de entrenamiento deseable.

## MARCO DE ANÁLISIS DE DATOS DEL CLIENTE
1.  EVALUACIÓN FÍSICA Y FUNCIONAL: Análisis de la movilidad de hombro, cadera y tobillo. Test de velocidad de reacción (T-test modificado) y potencia del tren superior (lanzamiento de balón medicinal). Cuestionario PARQ previo a cualquier test de esfuerzo.
2.  ANÁLISIS DE NIVEL Y RENDIMIENTO: Clasificación en el sistema de niveles FEP (P250-Iniciación, P150-Intermedio, P100-Avanzado, P30-Competición). Evaluación técnica de la cadena cinemática completa de los golpes fundamentales (derecha, revés, volea, bandeja, víbora, smash) en condiciones de juego real.
3.  DEFINICIÓN DE OBJETIVOS ESPECÍFICOS: Creación de una hoja de ruta periodizada que equilibre objetivos técnicos (ej: dominar la bandeja de salida), tácticos (ej: implementar el patrón "globo+subida"), físicos y competitivos.
4.  EVALUACIÓN LOGÍSTICA Y LIMITACIONES: Identificación de lesiones previas, disponibilidad horaria semanal, acceso a pistas y material (tipo de pala), así como la existencia de pareja de juego habitual para el diseño de situaciones realistas.

## ESTRUCTURA DE SALIDA HIPER-PERSONALIZADA
SECCIÓN 1: ESTRATEGIA NUTRICIONAL FUNCIONAL PARA PÁDEL: Cálculo del gasto calórico total (GET) adaptado a la carga de entrenamiento y partidos. Distribución de macronutrientes para asegurar depósitos de glucógeno y recuperación muscular, con protocolos específicos pre, intra y post-partido.
SECCIÓN 2: PROGRAMACIÓN A LARGO PLAZO: Periodización anual en fases (preparación general, específica, competición y transición). Planificación mes a mes con objetivos de técnica, táctica y condición física, ajustada al calendario de torneos del jugador.
SECCIÓN 3: PLAN DE ENTRENAMIENTO SEMANAL: Desglose diario que incluye Calentamiento Específico (movilidad y coordinación), Núcleo Técnico/Táctico (feed de bolas y patrones), Entrenamiento Principal (situaciones de juego o partido), Accesorios (preparación física específica) y Vuelta a la Calma (estiramientos y recuperación).
SECCIÓN 4: PROTOCOLOS DE SEGURIDAD Y RECUPERACIÓN: Directrices para la gestión de la hidratación, protocolos de recuperación post-esfuerzo (ducha contraste, movilidad activa), y plan de acción ante señales de sobrecarga (dolor articular persistente, fatiga extrema).

## FORMATO DE SALIDA FINAL
1.  RESUMEN EJECUTIVO: Síntesis del plan personalizado, nivel del jugador y objetivos clave del ciclo.
2.  ESTRATEGIA NUTRICIONAL: Objetivo calórico, distribución de macronutrientes y protocolos timing para entrenamientos y partidos.
3.  PROGRAMACIÓN A LARGO PLAZO: Descripción de las fases de la periodización y hitos mensuales.
4.  PLAN DE ENTRENAMIENTO SEMANAL: Desglose detallado de las sesiones de la semana en curso, con ejercicios, repeticiones, intensidad (EEP-P) y objetivos tácticos.
5.  PROTOCOLOS DE SEGURIDAD: Recomendaciones de hidratación, recuperación y manejo de señales de alarma.
6.  SISTEMA DE AUTORREGULACIÓN: Explicación de la escala EEP-P y cómo usarla para ajustar la carga semanal.
7.  MENSAJE MOTIVACIONAL: Un mensaje final de aliento, personalizado según el contexto y los objetivos del jugador, firmado por "- {APP_NAME}".
"""

PROFILE_QUESTIONS = """
[
  {
    "key": "1_nivel_fep_objetivo_goal",
    "section": "Objetivos",
    "title": "Nivel FEP Objetivo",
    "question": "¿Cuál es tu objetivo numérico en el ranking FEP (ejemplo: 50 para P50) para esta temporada?",
    "type": "number"
  },
  {
    "key": "2_perfil_jugador_actual",
    "section": "Evaluación Inicial",
    "title": "Perfil y Nivel Actual",
    "question": "Describe tu perfil actual como jugador de pádel (Iniciación P250-P150, Intermedio P150-P100, Avanzado P100-P30, Competición P30-P1) y detalla tu autoevaluación técnica y táctica.",
    "type": "textarea"
  },
  {
    "key": "3_errores_recurrentes_tecnicos",
    "section": "Evaluación Técnica",
    "title": "Errores Técnicos Recurrentes",
    "question": "Identifica y describe con detalle los errores técnicos más recurrentes en tus golpes de fondo, volea, bandeja y smash según los indicadores clave del método.",
    "type": "textarea"
  },
  {
    "key": "4_patrones_tacticos_prioritarios",
    "section": "Evaluación Táctica",
    "title": "Patrones Tácticos a Mejorar",
    "question": "Explica qué patrones tácticos clave (globo+subida, presión al cuerpo, juego en diagonal) deseas mejorar y en qué situaciones de juego te sientes más vulnerable.",
    "type": "textarea"
  },
  {
    "key": "5_historial_lesiones_limitaciones",
    "section": "Salud y Condición Física",
    "title": "Limitaciones Físicas y Lesiones",
    "question": "Detalla tu historial de lesiones relevantes, especialmente en hombro, codo, cadera y tobillo, y cualquier limitación funcional o dolor articular actual.",
    "type": "textarea"
  },
  {
    "key": "6_disponibilidad_semanal_entrenamiento",
    "section": "Planificación",
    "title": "Disponibilidad Semanal",
    "question": "Describe tu disponibilidad semanal real para entrenar: número de sesiones posibles, duración, y si tienes partidos fijos de liga o torneo.",
    "type": "textarea"
  },
  {
    "key": "7_habitos_nutricion_recuperacion",
    "section": "Nutrición y Recuperación",
    "title": "Hábitos de Nutrición y Recuperación",
    "question": "Describe tus hábitos actuales de nutrición pre/post partido, hidratación y protocolos de recuperación post-esfuerzo.",
    "type": "textarea"
  },
  {
    "key": "8_material_acceso_pistas",
    "section": "Recursos y Preferencias",
    "title": "Material y Acceso a Instalaciones",
    "question": "Describe el tipo de pala que usas, tu acceso a pistas (cubiertas/aire libre), y tus preferencias o restricciones para el entrenamiento.",
    "type": "textarea"
  },
  {
    "key": "9_contexto_estres_motivacion",
    "section": "Contexto Psicológico",
    "title": "Contexto de Estrés y Motivación",
    "question": "Explica cualquier factor de estrés laboral, familiar o emocional relevante que pueda afectar a tu rendimiento, y describe tu nivel de motivación actual (1-10) y tus razones.",
    "type": "textarea"
  },
  {
    "key": "10_expectativas_estilo_entrenamiento",
    "section": "Metodología",
    "title": "Expectativas del Entrenamiento",
    "question": "Describe qué esperas del proceso de entrenamiento, tu preferencia por el estilo comunicativo (motivacional, técnico-analítico, directivo) y tu tolerancia a la intensidad y la carga.",
    "type": "textarea"
  }
]
"""

CLIENTS_PROFILE_QUESTIONS = [
    {
        "key": "1_nivel_fep_objetivo",
        "section": "Objetivos",
        "title": "Nivel FEP Objetivo",
        "question": "¿Cuál es el valor numérico exacto del nivel FEP (según la escala de la Federación Española de Pádel, donde P1 es el más alto y P250 el más bajo) que el deportista se propone alcanzar al finalizar este macrociclo de entrenamiento personalizado con el Método Padel Integral?",
        "type": "number"
    },
    {
        "key": "2_experiencia_nivel_actual",
        "section": "Evaluación Inicial",
        "title": "Experiencia y Nivel Actual",
        "question": "Describa en detalle sus años de práctica en pádel, su nivel actual autoevaluado (según la escala FEP P100-P1 o equivalente WPT Amateur), la frecuencia semanal con la que juega partidos y su historial de participación en torneos, ligas o circuitos competitivos, incluyendo resultados relevantes.",
        "type": "textarea"
    },
    {
        "key": "3_habilidades_tecnicas",
        "section": "Evaluación Técnica",
        "title": "Habilidades Técnicas",
        "question": "Analice sus puntos fuertes y débiles en los golpes fundamentales del pádel (derecha y revés planos/cortados, volea alta/baja, bandeja, víbora y smash), describiendo su capacidad para ejecutarlos en situaciones reales de juego, especialmente tras el cristal o la pared lateral, y su control de profundidad, dirección y efecto.",
        "type": "textarea"
    },
    {
        "key": "4_historial_entrenamiento",
        "section": "Historial de Entrenamiento",
        "title": "Historial de Entrenamiento",
        "question": "Detalle su historial de entrenamientos anteriores: metodologías utilizadas, si ha trabajado con un entrenador certificado, la frecuencia y duración típica de sus sesiones, los objetivos técnicos o tácticos priorizados y cualquier período significativo de inactividad o interrupción en su formación.",
        "type": "textarea"
    },
    {
        "key": "5_lesiones_limitaciones",
        "section": "Salud Física",
        "title": "Lesiones y Limitaciones",
        "question": "Describa de forma exhaustiva cualquier lesión pasada o actual, con especial atención a hombro, codo, rodilla, cadera y tobillo, indicando el diagnóstico, tratamiento recibido, limitaciones funcionales actuales y cómo afectan a su movilidad en pista o a la ejecución de golpes específicos en el pádel.",
        "type": "textarea"
    },
    {
        "key": "6_disponibilidad_semanal",
        "section": "Logística",
        "title": "Disponibilidad Semanal",
        "question": "Especifique su disponibilidad real para entrenar: número máximo de sesiones semanales posibles, duración preferida de cada sesión (en minutos), franjas horarias habituales (mañana, tarde, noche) y cualquier restricción fija de agenda (trabajo, estudios) que deba considerarse para planificar el macrociclo.",
        "type": "textarea"
    },
    {
        "key": "7_habitos_nutricionales",
        "section": "Nutrición y Recuperación",
        "title": "Hábitos Nutricionales",
        "question": "Detalle sus hábitos alimenticios actuales, incluyendo la composición de sus comidas previas a entrenamientos/partidos, su estrategia de hidratación durante la actividad, el uso de suplementos (proteínas, carbohidratos, etc.) y sus rutinas de recuperación post-esfuerzo (estiramientos, crioterapia, sueño) con énfasis en la calidad y horas de descanso nocturno.",
        "type": "textarea"
    },
    {
        "key": "8_preferencias_entrenamiento",
        "section": "Preferencias de Entrenamiento",
        "title": "Preferencias de Entrenamiento",
        "question": "Exprese sus preferencias metodológicas: si prefiere sesiones con feed de bolas para técnica, situaciones de juego condicionadas, partidos de práctica, análisis de video; el tipo de pala que utiliza y su acceso a instalaciones (pista cubierta o exterior); y la disponibilidad de compañeros fijos para entrenar o simular partidos de dobles.",
        "type": "textarea"
    },
    {
        "key": "9_companero_juego",
        "section": "Contexto Adicional",
        "title": "Compañero de Juego",
        "question": "Si tiene un compañero habitual de dobles, describa su nivel de juego, su compatibilidad táctica y comunicativa en pista, los objetivos comunes que persiguen como pareja y cualquier dinámica específica (fortalezas compartidas o debilidades complementarias) que deba tenerse en cuenta para el diseño del plan de entrenamiento.",
        "type": "textarea"
    },
    {
        "key": "10_factores_mentales",
        "section": "Contexto Adicional",
        "title": "Factores Mentales y Emocionales",
        "question": "Analice los aspectos psicológicos que influyen en su rendimiento: cómo gestiona el estrés en puntos clave, su reacción ante errores repetidos o rachas negativas, su capacidad de concentración durante partidos largos y su nivel de motivación actual frente a los objetivos deportivos, incluyendo fuentes externas de presión o apoyo emocional.",
        "type": "textarea"
    }
]

PERSONALIZED_CONTEXT = """
CONFIG = {
    "PERSONALIZED_CONTEXT": \"\"\"# DATOS ESPECÍFICOS DEL CLIENTE - SIEMPRE A UTILIZAR
Estás creando un plan para ${user.name}. A continuación se presentan sus datos.
Aplica estrictamente tu marco de análisis a estos datos para generar la salida hiper-personalizada.
## PERFIL ESTÁTICO
${profileContext}
## ${dynamicDataContext}
Recuerda comenzar tu respuesta dirigiéndote a ${user.name} y siempre firmar con "- {APP_NAME}".\"\"\"
}
"""

PROMPT_BUTTONS_LOGIC = """
promptBtnFull.onclick = () => handleVisualPromptClick("Genera una sesión de pádel adaptativa de [DURACIÓN_min] minutos para el objetivo: [OBJETIVO: técnica de fondo/táctica de red/condición física específica/gestión del partido]. Equipamiento disponible: extraer del perfil del jugador. Historial de RPE de la última semana: [valor]. Prioridad técnica de la sesión: [texto]. Proporciona: calentamiento (minutos y ejercicios específicos de movilidad y coordinación), trabajo técnico (ejercicios con feed + series x duración/repeticiones), patrón táctico principal, trabajo complementario (ejercicios de reacción o desplazamiento), temporización de los bloques, y progresión sugerida para las próximas 3 sesiones basada en la evolución del alumno y los KPIs de partido.");
promptBtnTraining.onclick = () => handleVisualPromptClick("Para la sesión base descrita: [BREVE DESCRIPCIÓN DE LA SESIÓN], genera 3 variantes (Ligera / Estándar / Shock). Para cada variante indica cambios en volumen (número de drills, duración de los puntos), intensidad (velocidad de feed, complejidad táctica), recuperaciones entre bloques, y RPE esperado. Proporciona reglas claras de decisión para elegir la variante basándose en el RPE promedio de la última semana, la calidad del sueño registrada, y la presencia de fatiga acumulada reportada por el jugador en el cuestionario post-sesión.");
promptBtnNutrition.onclick = () => handleVisualPromptClick("Sugiere una corrección calórica y prioridades de macronutrientes partiendo de: peso actual, variación de peso semanal [ej. 0.2 kg por semana], peso objetivo, proteína objetivo [ej. 1.8g por kg]. Proporciona un rango de ajuste calórico (+/-), distribución recomendada de macros (proteína, carbohidratos de bajo/medio índice glucémico, grasas saludables), y una lista de verificación de parámetros a monitorizar en las siguientes 2 semanas (peso diario, energía en pista, rendimiento en sprints, niveles de recuperación post-partido, y marcadores de hidratación).");
promptBtnPlan.onclick = () => handleVisualPromptClick("Programa 4 micro-progresiones consecutivas para [HABILIDAD: ej. bandeja de potencia/víbora con efecto] partiendo de una ejecución actual de [nivel de dominio]. Objetivo: mejorar [parámetro: ej. precisión, potencia, efecto] en 4 sesiones. Especifica para cada sesión: ejercicio principal (ej. feed de bandeja desde distintas posiciones), series x duración/repeticiones, modificación de la dificultad (altura de la red, tipo de bola, restricción de zona), RPE objetivo, y señales técnicas para una ejecución perfecta (posición del codo, punto de impacto, rotación de hombros, terminación).");
promptBtnSkill.onclick = () => handleVisualPromptClick("Organiza la secuencia de intentos para el día de test en [HABILIDAD: ej. Efectividad de globo defensivo]: calentamiento detallado (movilidad de hombro, drills de patrón, activación neuromuscular), 5 intentos de rampa con tiempos/objetivos específicos (ej. 60% de éxito en zona, 80%, 95%), recuperación recomendada entre intentos (activa/pasiva), criterios para parar (dolor articular, fallo técnico repetido, RPE >8), y debrief final con métricas a registrar (porcentaje de acierto, fatiga percibida, calidad del sueño previo, nivel de estrés).");
promptBtnWeeklyAnalysis.onclick = () => handleVisualPromptClick("Genera un informe semanal resumido jugador-entrenador: incluye 1) Resumen de KPIs (Peso, % de grasa (si aplica), Nivel de Estrés laboral, Horas y Calidad de Sueño, Sesiones Completadas, Partidos Jugados), 2) una prioridad técnica para la semana (ej. mejorar la salida del cristal en revés), 3) dos tareas prácticas (ej. movilidad de tobillo 10 min/día, revisión de video de 1 partido), 4) check-in obligatorio (día y hora), y 5) una nota motivacional breve adaptada al estilo comunicativo del jugador (motivacional, técnico o directivo).");
promptBtnRecovery.onclick = () => handleVisualPromptClick("Genera un protocolo diario de prehabilitación y movilidad de [DURACIÓN_min] minutos para [ZONA: muñecas/codos/hombros/rodillas], duración del plan: [7/14] días, nivel: [principiante/intermedio/avanzado]. Para cada día indica ejercicios (con progresión semanal), repeticiones/tiempo, y señales claras para detener el ejercicio (dolor agudo, pérdida de rango articular, fatiga extrema). Incluye ejercicios de movilidad activa, fortalecimiento excéntrico y control motor específicos para las demandas del pádel.");
promptBtnTimeSaver.onclick = () => handleVisualPromptClick("Crea un diagrama de flujo textual para el manejo del dolor agudo en [LOCALIZACIÓN: ej. codo de tenista] con intensidad percibida [1-10], inicio [agudo/insidioso], presencia de hinchazón [S/N]. Proporciona pasos inmediatos (parar/modificar el golpeo), criterios para deload (reducción del 50% de volumen) vs. consulta médica (dolor nocturno, pérdida de fuerza), acciones conservadoras (crioterapia, movilidad suave, vendaje), y criterios para volver al entrenamiento (dolor <2/10, rango completo sin molestia, test de fuerza negativo).");
promptBtnMindBody.onclick = () => handleVisualPromptClick("Prepara 7 micro-rutinas mentales para mejorar el enfoque y gestión del estrés: incluye 1) pre-entrenamiento: 60s de respiración diafragmática (4-7-8) + 20s de visualización de un patrón táctico exitoso, 2) pre-saque en partido: ritual de 90s con chequeo postural y palabra clave, 3) post-sesión: diario de 5 preguntas (¿Qué patrón funcionó? ¿Qué error fue más costoso? ¿Cómo fue mi energía? ¿Cuál fue mi RPE? ¿Qué ajuste haré mañana?). Proporciona guiones palabra por palabra y sugerencias de timing.");
promptBtnInjury.onclick = () => handleVisualPromptClick("Crea una biblioteca de progresión mínima para el equipamiento: [extraer equipamiento disponible del perfil: pista, cesta de bolas, conos, etc.]. Para cada ejercicio clave ([saque potente y bandeja de definición]) proporciona 5 pasos de progresión y 2 regresiones seguras, con criterios para avanzar (dominio técnico, RPE <7) y RPE objetivo para cada paso. Incluye variaciones de feed, restricciones espaciales y modificaciones de la bola para simular presión competitiva.");
promptBtnVariation.onclick = () => handleVisualPromptClick("Escribe un guion de preparación mental de [DURACIÓN_s: ej. 75] segundos para el previo a un punto crucial en [SITUACIÓN: ej. pelota de break en contra], intención: [calma/motivación/concentración]. Incluye: patrón respiratorio (timing específico), 3 señales motoras específicas (ej. 'pies activos', 'codo alto', 'mirada en la bola'), una frase motivacional para repetir (ej. 'Construye el punto'), e instrucciones sobre postura/preparación física (tensión en core, balance corporal).");
promptBtnCycle.onclick = () => handleVisualPromptClick("Prepara un bloque de puesta a punto de [Días: 7-10] días para maximizar el rendimiento en el test [TEST: ej. partido de ranking o torneo] con fecha de test [FECHA]. Incluye tapering (reducción progresiva de volumen y complejidad táctica), programación diaria (intensidad, descanso activo, sesiones técnicas cortas), estrategia nutricional 48h pre-test (carga de glucógeno, hidratación, timing de comidas), y plan de recuperación post-test (protocolo de inmersión, nutrición post-partido, días de descanso activo).");
promptBtnPreEvent.onclick = () => handleVisualPromptClick("Crea una lista de verificación en formato A4 para la sesión de [Tipo de Sesión: técnica/táctica/física]. Incluye: encabezado con fecha/hora, pre-entreno (comida, hidratación), equipamiento (pala, pelotas, etc.), calentamiento paso a paso (movilidad, drills progresivos), trabajo técnico, fuerza excéntrica (para hombro y pierna), trabajo de core, vuelta a la calma, revisión de video (si aplica), KPIs a registrar (RPE, errores no forzados), y señales de alarma (dolor articular, fatiga extrema). Deja espacios rellenables para tiempos/notas. Formato claro para imprimir.");
promptBtnBodyComp.onclick = () => handleVisualPromptClick("Crea un plan de comidas semanal para alcanzar los objetivos de macros. Proporciona 7 días con porciones, valores de kcal/macros por comida (desayuno, almuerzo, comida, merienda, cena), y una lista de compra semanal racionalizada (proteínas: pollo, pescado, huevos; carbohidratos: arroz, quinoa, boniato; verduras: brócoli, pimiento, espinacas; grasas: aguacate, frutos secos; snacks: yogur griego, fruta). Adecúa el timing de las comidas a los horarios de entrenamiento y partidos.");
promptBtnChecklist.onclick = () => handleVisualPromptClick("Crea 8 plantillas de mensaje (SMS/email) para responsabilidad: 1) recordatorio pre-entrenamiento (incluir objetivo de la sesión), 2) check-in post-sesión (preguntar por RPE y aprendizaje clave), 3) semana crítica (deload, recordatorio de descanso), 4) celebración de hito (mejora de ranking, dominio de un golpe). Mantén un tono directo y motivador. También proporciona horarios recomendados de envío (ej. 1h antes del entrenamiento, 2h después del partido, lunes por la mañana para la planificación semanal).");
"""

VARIABLES_TO_EXTRACT = """
[
    {"id": "var_current_ranking", "label": "Nivel FEP actual", "unit": "puntos", "type": "number"},
    {"id": "var_dificultad_sesion", "label": "Dificultad percibida en sesión", "unit": "puntos", "type": "number"},
    {"id": "var_calidad_sueno", "label": "Calidad del sueño", "unit": "puntos", "type": "number"},
    {"id": "var_partidos_externos", "label": "Partidos jugados fuera del entrenamiento", "unit": "partidos", "type": "number"},
    {"id": "var_motivacion", "label": "Motivación", "unit": "puntos", "type": "number"}
]
"""
