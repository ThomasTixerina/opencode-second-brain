En este video como referencia de youtube: https://www.youtube.com/watch?v=_0alyykYhCY
Este es un resumen de los prompts: Para construir tu sistema automático en *NotebookLM*, Joaquín Barberá utiliza tres motores específicos. A continuación, detallo los prompts de configuración (sistema) y los prompts de acción (solicitud) para cada uno:

### 1. Motor de Tendencias
Este motor se enfoca en recomendar las mejores herramientas de IA actuales basándose en fuentes del sector.
* **Prompt de configuración (personalizado):** "Actúa como un director de innovación en IA en una agencia de creación de contenidos. Accede a los contenidos de las fuentes como boletines más recientes de la industria y a bases de datos. Tu objetivo es sintetizar toda esta información para uno, recomendar herramientas específicas que se ajusten a la descripción del proyecto del usuario. Dos, resumir los cambios clave en la industria. Y al recomendar herramientas explica por qué se ajustan al proyecto del usuario e indica la fuente de dónde proviene la información." (2:50)
* **Prompt de solicitud:** "Estoy trabajando en un vídeo cinematográfico sobre unos seres humanos futuristas, mitad biológicos, mitad electrónicos, que habitan el planeta Marte siglos después de que la Tierra se convirtiera en un planeta inhabitable. Recomiéndame las mejores herramientas y recursos para lograr este proyecto desglosado en guion, generación, imagen y vídeo y voz y audio y que luego me des una explicación de por qué cada herramienta." (3:30)

### 2. Motor de Escritura
Utiliza la clonación de estilos a partir de transcripciones de vídeos de referencia para replicar estructuras ganadoras.
* **Prompt de configuración (personalizado):** "Actúa como un escritor de guiones profesional para vídeos de YouTube. Tu objetivo es clonar el estilo y lenguaje de las fuentes transcritas proporcionadas. Analiza detenidamente longitud de frase, vocabulario, uso del humor y sarcasmo, uso de expresiones no formales, estilo de transiciones. Cuando te pida escribir un guion, no utilices un lenguaje genérico de inteligencia artificial, como 'en este vídeo veremos' o parecidos. En su lugar, escribe exactamente como lo haría el guionista de los vídeos de referencia. Prioriza la retención de la audiencia y la creación de hooks fuertes desde el inicio, así como roturas de patrón para generar picos de retención." (6:25)
* **Prompt de solicitud:** "Revisa las transcripciones de los vídeos de referencia para identificar la audiencia objetivo y estilo. Escribe un guion completo basado en este esquema de duración aproximadamente 5 minutos. Estructura: emita la estructura hook y estrategias de retención utilizadas en los vídeos de referencia. Formato: solo texto hablado (voice over), no incluya descripciones, etcétera. Tema del guion: seres humanos futuristas, mitad biológicos, mitad electrónicos, que habitan el planeta Marte siglos después de que la Tierra se convierta en un planeta inhabitable." (7:13)

### 3. Motor de Generación
Se encarga de crear prompts técnicos precisos basados en la documentación oficial de las herramientas de IA.
* **Prompt de configuración (personalizado):** "Actúa como un ingeniero de prompts. Tu objetivo es generar prompts para generación de contenido. Siempre consulta las fuentes antes de responder. Ten en cuenta cuando te pidan un prompt todo esto, utilizar la síntesis de parámetros exacta que aparecen las fuentes. No inventes comandos que no existan en la documentación. Aparte de generar el prompt, dame una explicación detallada de los elementos más importantes y ajustes técnicos que has incluido, así como el por qué para que me sirva de aprendizaje para aprender a crear prompts." (9:59)
* **Prompts de solicitud:**
    * *Para imágenes:* "Crear un prompt para generar una imagen con [nombre de herramienta] sobre [tema de la historia] y luego al final del prompt explícame qué ajustes técnicos estás aplicando y por qué." (10:56)
    * *Para vídeo:* "Genera un prompt para una toma FPV de dron a alta velocidad con [nombre de herramienta]. Basándote en la guía técnica disponible incluye parámetros de movimiento de cámara y efectos de distorsión propios de este tipo de toma, dejando espacio para propuestas creativas. Genera el prompt con la estructura y los tecnicismos correctos y al final del prompt explícame qué ajustes técnicos estás aplicando y por qué." (12:14)

Joaquín Barberá propone este sistema de tres motores (0:26) con el objetivo de dejar de depender de trucos temporales y construir una estructura sólida y automatizable para la creación de contenido con IA. La lógica detrás de dividir el flujo de trabajo es la especialización de tareas para evitar la obsolescencia y mejorar la calidad:

Motor de Tendencias (0:44): Su función es resolver el problema de la sobreinformación. En lugar de buscar herramientas manualmente cada día, este motor sintetiza noticias y bases de datos para recomendar solo las IA más adecuadas para cada proyecto específico, garantizando que siempre utilices tecnología actualizada.
Motor de Escritura (5:02): Este motor se encarga de clonar el estilo, el tono y las estrategias de retención de creadores exitosos. Al configurarlo con transcripciones de referencia, evitas el lenguaje genérico de las IAs y logras guiones con personalidad propia y estructuras probadas para maximizar la retención de la audiencia.
Motor de Generación (8:43): Es el pilar técnico. Su objetivo es leer la documentación oficial de cada modelo de IA (como Leonardo AI, Kling, Luma Dream Machine, etc.) para generar prompts con la sintaxis y los parámetros técnicos exactos requeridos por cada herramienta, eliminando el proceso de ensayo y error.
Al usar este sistema modular, no solo ahorras tiempo, sino que garantizas que cada fase de la producción (elección de herramienta, redacción y ejecución técnica) esté optimizada al máximo nivel profesional.

La **configuración personalizada** (el "prompt de sistema") es el elemento clave que le da a cada cuaderno en *NotebookLM* un rol y un objetivo específicos. Joaquín Barberá utiliza esta función para transformar la herramienta en motores especializados (2:43, 6:18, 9:52). Cada configuración incluye:

* **Asignación de un Rol:** Se define una identidad profesional para la IA (ej. "Director de innovación en IA", "Escritor de guiones profesional" o "Ingeniero de prompts").
* **Definición del Objetivo:** Se establece la misión clara de lo que la IA debe hacer con la información, como sintetizar tendencias, clonar estilos de escritura o generar parámetros técnicos.
* **Reglas de Comportamiento:** Se incluyen instrucciones sobre cómo debe procesar la información, qué evitar (como lenguaje genérico de IA) y cómo estructurar sus respuestas (ej. "siempre consulta las fuentes", "no inventes comandos").
* **Formato de Salida:** Se especifica cómo debe entregar la información (ej. "dame una explicación detallada de los ajustes técnicos para que me sirva de aprendizaje").

Al configurar el cuaderno de esta manera, garantizas que la IA actúe como un **experto especializado** en lugar de como un asistente genérico.

La **configuración personalizada** (el "prompt de sistema") es el elemento clave que le da a cada cuaderno en *NotebookLM* un rol y un objetivo específicos. Joaquín Barberá utiliza esta función para transformar la herramienta en motores especializados (2:43, 6:18, 9:52). Cada configuración incluye:

* **Asignación de un Rol:** Se define una identidad profesional para la IA (ej. "Director de innovación en IA", "Escritor de guiones profesional" o "Ingeniero de prompts").
* **Definición del Objetivo:** Se establece la misión clara de lo que la IA debe hacer con la información, como sintetizar tendencias, clonar estilos de escritura o generar parámetros técnicos.
* **Reglas de Comportamiento:** Se incluyen instrucciones sobre cómo debe procesar la información, qué evitar (como lenguaje genérico de IA) y cómo estructurar sus respuestas (ej. "siempre consulta las fuentes", "no inventes comandos").
* **Formato de Salida:** Se especifica cómo debe entregar la información (ej. "dame una explicación detallada de los ajustes técnicos para que me sirva de aprendizaje").

Al configurar el cuaderno de esta manera, garantizas que la IA actúe como un **experto especializado** en lugar de como un asistente genérico.


----------------------------------------------

Aquí esta toda la transcripción del video, para que puedas entender todo el concepto desde cualquier IA que vaya usar este motor de tendencias, que vamos a usar para la generación de contenido y el cual tu vas a controlar directamente y vas a hacer todo el trabajo por mi:


0:00
¿Estás viendo este vídeo? Es posible que
0:02
te hagas estas dos preguntas. ¿Qué
0:04
herramientas has utilizado? ¿Qué prom
0:07
has empleado? Pero no te voy a responder
0:09
a eso. La herramienta o pron que te dé
0:11
hoy mañana puede estar obsoleto. Lo que
0:14
necesitas es un sistema. No te voy a dar
0:17
un pez, te voy a enseñar a pescar. Vamos
0:19
a crear una máquina que seleccione tus
0:22
herramientas y genere tus promps
0:24
automáticamente. Y no te pierdas el
0:26
último paso que convierte este flujo en
0:29
una auténtica máquina de ingeniería de
0:31
promps. Así que vamos a verlo.
0:35
Accedemos a Notebook LM. Vamos a crear
0:37
un nuevo cuaderno haciendo clic en crear
0:40
nuevo y le vamos a poner este nombre.
0:44
Motor de tendencias. Cada día se lanzan
0:47
cientos de nuevas herramientas de
0:49
inteligencia artificial. ¿Cómo elegir
0:51
cuáles utilizar para nuestro caso
0:54
concreto sin perder horas de búsqueda de
0:57
información y pruebas? Pues lo que
1:00
haremos será crear un motor de
1:02
tendencias de inteligencia artificial en
1:03
nuestro notebook LM. Para eso, haremos
1:06
clic en añadir fuentes, luego en sitios
1:08
web y aquí vamos a añadir cinco sitios
1:11
web, cinco fuentes de herramientas de
1:14
inteligencia artificial. En primer lugar
1:17
vamos a subir esta se llama de Ramown
1:20
AI, donde tenemos noticias recientes,
1:24
diarias sobre lo más importante de la
1:26
industria de la inteligencia artificial.
1:28
Vamos a copiar la URL.
1:30
Pegamos. También añadiremos esta página
1:33
que se llama de Neuron, que tiene un
1:35
enfoque más práctico. Copiamos la URL y
1:39
la pegamos. También vamos a usar como
1:41
fuente Futureepedia donde iremos a I
1:44
tools y aquí tenemos todas las
1:46
herramientas clasificadas por categorías
1:49
y lo que vamos a hacer es copiar cada
1:52
una de estas categorías. ¿Veis? De estos
1:55
enlaces. Ya las tengo aquí todas
1:58
pegadas. También usaremos product con
2:02
tendencias diarias de herramientas de
2:04
inteligencia artificial.
2:07
Por supuesto, también vamos a utilizar
2:09
LM Arena y haremos clic aquí en
2:12
overview,
2:13
donde tenemos un importante comparativo
2:16
de herramientas de inteligencia
2:17
artificial clasificadas por categorías.
2:20
Copiamos URL
2:23
y la añadimos. Una vez tenemos todas las
2:27
URLs de las fuentes, hacemos clic en
2:29
insertar.
2:32
Nuestro cuaderno ya tiene el
2:33
conocimiento, pero le falta algo
2:35
crucial. Debemos darle su rol y objetivo
2:39
para que nuestra máquina pueda cumplir
2:40
su misión correctamente. Y para ello
2:43
iremos a la configuración del cuaderno a
2:45
personalizado y vamos a utilizar este
2:47
prom.
2:50
Actúa como un director de innovación en
2:52
IA en una agencia de creación de
2:54
contenidos. Acede a los contenidos de
2:56
las fuentes como boletines más recientes
2:58
de la industria y a bases de datos. Tu
3:01
objetivo es sintetizar toda esta
3:03
información para uno, recomendar
3:06
herramientas específicas que se ajusten
3:08
a la descripción del proyecto del
3:10
usuario.
3:12
Dos, resumir los cambios clave en la
3:15
industria. Y al recomendar herramientas
3:17
explica por qué se ajustan al proyecto
3:19
del usuario e indica la fuente de dónde
3:22
proviene la información. Y le damos a
3:25
guardar. Y es hora de preguntar a
3:27
nuestro motor de tendencias. Lo
3:30
siguiente, estoy trabajando en un vídeo
3:32
cinematográfico sobre unos seres humanos
3:34
futuristas, mitad biológicos, mitad
3:36
electrónicos, que habitan el planeta
3:38
Marte siglos después de que la Tierra se
3:40
convirtiera en un planeta inhabitable.
3:43
le decimos que nos recomiende las las
3:45
mejores herramientas y recursos para
3:47
lograr este proyecto desglosado en
3:50
guion, generación, imagen y vídeo y voz
3:54
y audio y que luego nos dé una
3:57
explicación de por qué cada herramienta.
4:00
Y le damos a enviar.
4:03
Y aquí tenemos ya la respuesta de
4:05
nuestro motor para el script, para el
4:08
guion. nos recomienda por aquí Cloud
4:10
Opus 46 Thinking y Cloud 3.5 Sonet. Nos
4:14
dice por qué, la razones, el impacto
4:17
cinematográfico,
4:19
generación de imagen y vídeo, Leonardo
4:21
AI y Clean 3.0. Y aquí nos explica el
4:25
porqué de cada caso, voz y audio, eleven
4:29
laps, música, va, ¿vale? Y aquí nos
4:33
explica todo perfectamente. A diferencia
4:35
de lo que nos podría haber respondido TR
4:37
GPT con una respuesta supergeneralista y
4:41
probablemente desactualizada, nuestra
4:43
máquina de tendencias nos da una
4:45
respuesta totalmente actualizada,
4:48
teniendo en cuenta la relevancia e
4:50
idoneidad de cada herramienta. Ya
4:53
tenemos las herramientas. Ahora toca
4:55
otra parte fundamental, la creación del
4:57
guion.
5:00
Ahora necesitamos un motor de escritura
5:02
especializado en nuestra temática que
5:04
tenga una estrategia ganadora y para eso
5:07
usaremos la clonación. Vamos a crear un
5:09
nuevo cuaderno y a este lo vamos a
5:12
llamar
5:15
motor de escritura. Para mi caso
5:17
concreto, voy a utilizar este canal de
5:20
YouTube de historias de ciencia ficción.
5:23
No vamos a hacer una clonación literal
5:25
de los vídeos, lo que vamos a hacer es
5:27
utilizar su estrategia y su lenguaje. Y
5:29
para hacer esto más rápido, vamos a
5:31
utilizar esta extensión de Chrome
5:33
YouTube to Notebook LM. Le damos añadir
5:36
a Chrome y luego añadir extensión. A
5:39
continuación, en vídeos vamos a
5:41
populares para que los ordene de más a
5:43
menos popularidad. Y fijaos, hacemos
5:46
clic aquí en notebook LM, le damos a
5:49
elegir un cuaderno y aquí lo tenemos.
5:51
Motor de escritura.
5:56
y automáticamente se están añadiendo
5:58
todos los vídeos de la página. Ahora nos
6:01
queda un punto fundamental porque si en
6:04
este momento le pedimos que nos haga un
6:06
guion, lo que va a hacer es un resumen
6:08
de los vídeos que ya tiene. Y eso no es
6:10
lo que queremos. Tenemos que configurar
6:12
el motor de escritura para que replique
6:15
el estilo y el lenguaje. Y para eso nos
6:18
vamos a la configuración del cuaderno
6:20
personalizado y vamos a pegar este prom.
6:25
Actúa como un escritor de guiones
6:27
profesional para vídeos de YouTube. Tu
6:29
objetivo es clonar el estilo y lenguaje
6:31
de las fuentes transcritas
6:33
proporcionadas. Analiza detenidamente
6:35
longitud de frase, vocabulario, uso del
6:38
humor y sarcasmo, uso de expresiones no
6:41
formales, estilo de transiciones. Cuando
6:43
te pida escribir un guion, no utilices
6:45
un lenguaje genérico de inteligencia
6:46
artificial, como en este vídeo veremos o
6:49
parecidos. En su lugar, escribe
6:52
exactamente como lo haría el guionista
6:54
de los vídeos de referencia. prioriza la
6:56
retención de la audiencia y la creación
6:58
de hooks fuertes desde el inicio, así
7:00
como roturas de patrón para generar
7:03
picos de retención. Y le damos a
7:06
guardar. Y ahora ya podemos preguntar a
7:09
nuestro motor de escritura y le vamos a
7:11
decir lo siguiente. Revisa las
7:13
transcripciones de los vídeos de
7:15
referencia para identificar la audiencia
7:17
objetivo y estilo. Escribe un guion
7:19
completo basado en este esquema de
7:22
duración aproximadamente 5 minutos.
7:24
Estructura. emita la estructura hook y
7:26
estrategias de retención utilizadas en
7:28
los vídeos de referencia. Formato solo
7:31
texto hablado voice over, no incluya
7:34
descripciones, etcétera. Tema del guion,
7:37
seres humanos futuristas, mitad
7:39
biológicos, mitad electrónicos, que
7:41
habitan el planeta Marte siglos después
7:43
de que la Tierra se convierta en un
7:45
planeta inhabitable. Y le vamos a
7:48
enviar.
7:50
Y aquí tenemos el guion generado que
7:52
está chulísimo aplicando el análisis de
7:56
patrones, estructura y estilo de los
7:59
vídeos que hemos subido como fuentes.
8:01
Recuerda guardarlo como nota para no
8:04
perderlo, ¿vale? Ya lo tendremos aquí a
8:06
la derecha. Siempre
8:09
llegamos a un punto clave. Tenemos ya
8:12
las herramientas y el guion, pero ahora
8:14
puede ser que generes la imagen o el
8:16
vídeo y que no salga exactamente lo que
8:19
tienes en mente. El problema es que cada
8:22
modelo o herramienta de inteligencia
8:23
artificial utiliza un lenguaje
8:25
específico para la descripción de los
8:28
contenidos que quieres generar. Todo
8:30
esto está en la documentación de la
8:32
herramienta, pero no te preocupes que no
8:33
te la tienes que estudiar, ni siquiera
8:35
la tienes que leer porque vamos a
8:37
encargar esta tarea a Notebook LM. Vamos
8:41
a crear un nuevo cuaderno
8:43
que en este caso se va a llamar motor de
8:47
generación. Para buscar la guía de
8:49
prompting de cada herramienta o modelo,
8:51
tendrás que poner algo así en Google,
8:54
por ejemplo, BO31 official pront guide.
8:58
Aquí lo tenemos.
9:03
Declean 3.0. Pues algo así.
9:08
Aquí lo tenemos.
9:15
Nano banana.
9:19
Aquí está.
9:28
Si no existe una documentación oficial
9:30
de alguna herramienta, siempre puedes
9:32
buscar una guía de calidad creada por la
9:35
comunidad, que casi seguro que habrá.
9:37
Ahora nos vamos a nuestro cuaderno
9:39
añadir fuentes, sitios web y pegamos las
9:42
URLs de las guías oficiales de las
9:44
herramientas que vayamos a utilizar y le
9:46
damos a insertar.
9:49
Y como siempre es superimportante
9:52
configurar el cuaderno. Vamos a
9:54
personalizado
9:56
y vamos a ponerle este prom de sistema.
9:59
Actúa como un ingeniero de proms. Tu
10:01
objetivo es generar proms para
10:03
generación de contenido. Siempre
10:05
consulta las fuentes antes de responder.
10:09
Ten en cuenta cuando te pidan un prom
10:11
todo esto, utilizar la síntasis de
10:14
parámetros exacta que aparecen las
10:15
fuentes.
10:17
No inventes comandos que no existan en
10:19
la documentación.
10:21
Aparte de generar el prom, dame una
10:23
explicación detallada de los elementos
10:25
más importantes y ajustes técnicos que
10:27
has incluido, así como el por qué para
10:30
que me sirva de aprendizaje para
10:33
aprender a crear promps. Y le damos a
10:36
guardar. Como has visto, al final del
10:39
prom dicho que quiero que me explique,
10:42
aparte de darme un prom, que me explique
10:44
los principales elementos que ha
10:45
incluido para que me sirva de
10:47
aprendizaje. Y vamos ahora a pedirle a
10:49
nuestro motor de generación que cree
10:52
esta imagen basándote en la
10:54
documentación disponible en tus fuentes.
10:56
crear un prom para generar una imagen
10:58
con nano banana sobre aquí he puesto una
11:02
parte de esa historia que me ha dado el
11:05
otro cuaderno y luego al final del prom
11:08
explícame qué ajustes técnicos estás
11:10
aplicando y por qué y le damos a enviar.
11:13
Aquí tenemos la respuesta. Por un lado
11:15
tenemos el prom hasta aquí que lo ha
11:18
puesto automáticamente en inglés porque
11:20
es lo que recomienda la documentación
11:23
oficial técnica de pront. Y luego más
11:26
abajo tenemos la explicación de ajustes
11:29
técnicos y aprendizaje para que podamos
11:33
aprender de ese pron que ha generado
11:36
este cuaderno de motor de generación.
11:38
Ahora estamos ya en Google Flow. Voy a
11:42
pegar el prom que me ha dado mi cuaderno
11:45
y aquí vamos a poner imagen 169, tres
11:48
imágenes nano banana 2 y le damos a
11:51
enviar. Y aquí tenemos ya las imágenes
11:54
que están chulísimas. Voy a descargar
11:55
esta para verla en detalle.
11:59
Y como veis, fijaos qué chula.
12:07
Y vamos ahora a generar un vídeo con
12:09
BO3.
12:11
Y le vamos a poner lo siguiente. Genera
12:14
un pron para una toma FPV de dron a alta
12:18
velocidad, en este caso con BO31. Aquí
12:21
tenemos todas las fuentes para BO31,
12:24
para Nano Banana, para Clean. En cuanto
12:27
al tema, pues es el mismo que he puesto
12:30
antes. Basándote en la guía técnica
12:33
disponible incluye parámetros de
12:34
movimiento de cámara y efectos de
12:36
distorsión propios de este tipo de toma,
12:38
dejando espacio para propuestas
12:40
creativas. Genera el prom con la
12:42
estructura y los tecnicismos correctos y
12:44
al final del prom explícame qué ajustes
12:46
técnicos estás aplicando y por qué. y le
12:49
damos a enviar.
12:51
Y aquí tenemos el prom
12:54
que ya lo voy a copiar
12:57
y luego más abajo la explicación.
13:00
Volvemos a Google Flow ahora para vídeo
13:03
169 un vídeo omniflash y 10 segundos.
13:08
Pegamos nuestro prom
13:11
y le damos a enviar.
13:13
Y aquí tenemos ya el vídeo generado.
13:26
Te dejo todos los promps que he
13:28
utilizado en el primer comentario, en el
13:30
comentario fijo. Llegamos al final del
13:32
vídeo, pero no te vayas todavía porque
13:34
por aquí te dejo un vídeo superinesante
13:36
con el nuevo Flow, Flow 2.0. todos los
13:40
detalles, herramientas, todo. Por aquí
13:42
te dejo otro vídeo también superinesante
13:45
para que aprendas como nunca con el
13:48
método científico usando Notebook LM. Y
13:52
por aquí te dejo otro vídeo también muy
13:54
interesante para que aprendas a crear
13:56
personajes consistentes tanto en la
13:58
generación de imágenes como vídeos.
14:00
Yeah.
