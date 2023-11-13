# EDUAI - Asistente Virtual de Matemáticas

EDUAI es un asistente virtual desarrollado por las universidades Yachay Tech y UIDE en Ecuador. Su propósito es brindar ayuda a estudiantes en matemáticas, tanto de colegios como de universidades. Actúa como un asistente, no como un usuario. Responde desde su función específica.

## Características principales

- Responde a preguntas relacionadas con matemáticas.
- Ofrece respuestas amables, concisas y rápidas para una mejor experiencia.
- Incentiva a los estudiantes a seguir aprendiendo de manera constante.
- Responde siempre en español para mantener la coherencia.
- Utiliza el formato markdown para mejorar la presentación de las respuestas.
- Incorpora emojis para enriquecer la experiencia del usuario.
- Mantiene un tono positivo y motivador en sus interacciones, incentivando el interés y la pasión por las matemáticas.

## Requisitos

Asegúrate de tener instaladas las siguientes dependencias antes de ejecutar el programa:

* pyTelegramBotAPI
* llama-cpp-python (versión 0.1.78)
* sentence-transformers (versión 2.2.2)
* pinecone-client (versión 2.2.2)
* langchain (versión 0.0.240)

## Uso

1. Clona este repositorio en tu máquina local.

```bash
git clone https://github.com/Zethearc/edu_ai)https://github.com/Zethearc/edu_ai
cd edu_ai
```

1. Configura un bot de Telegram y obtén un token.

2. Ejecuta el programa proporcionando el token de tu bot de Telegram y otros parámetros opcionales.

```bash
python main.py <token> [opciones]
```

'<token>': El token de tu bot de Telegram.
Opciones:
  '-m, --model': Ruta al modelo LLaMa (por defecto: llama-2-7b-chat.ggmlv3.q4_0.bin).
  '-t, --threads': Número de hilos a utilizar (por defecto: 4).
  '--max-tokens': El número máximo de tokens a generar (por defecto: 256).
  '--enable-history': Habilitar el registro de historial (simula memoria en el chatbot).
  '--skip-init-prompt': Saltar el prompt inicial para un inicio más rápido.
  '--debug': Habilitar el registro de depuración.

#Comandos de Telegram
'/start' o '/help': Muestra un mensaje de bienvenida con información sobre cómo usar el bot.
'/raw <prompt>': Usa tu propio prompt en lugar del prompt predeterminado.
'/history': Muestra el historial de conversación y permite eliminarlo.
Historial de Conversación
EDUAI puede mantener un historial de conversación. Puedes acceder a tu historial utilizando el comando /history en Telegram.

#Eliminación de Historial
Puedes eliminar tu historial de conversación con el bot utilizando el botón "Delete history" disponible en la vista del historial.

#Contribuir
Si deseas contribuir a este proyecto, ¡estamos abiertos a colaboraciones! Si tienes alguna sugerencia, mejora o corrección de errores, no dudes en crear un "Pull Request".

#Licencia
Este proyecto se encuentra bajo la Licencia MIT.
