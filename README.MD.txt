# Bots.py - CDPS SYSTEM AI Bot

Repositorio que contiene el bot principal de Telegram y el módulo Estrella Roja para procesamiento /atlas.

## Descripción

Este bot de Telegram integra varias funcionalidades, incluyendo:

- Comando `/atlas` para verificar tarjetas utilizando el módulo Estrella Roja.
- Uso de proxies rotativos.
- Motor local basado en llama-cpp.
- Otras integraciones como `/braulio` (PdfSimpli) y `/recarga` (Telcel).

## Archivos principales

- `bot_principal.py`: Código principal del bot, maneja comandos y funcionalidad general.
- `estrella_roja.py`: Módulo con la clase `Core` que contiene la lógica para el gateway Estrella Roja MercadoPago.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el bot.

## Instalación y ejecución

### Requisitos

- Python 3.10 o superior.
- Telegram bot token válido.

### Instalación de dependencias

```bash
pip install -r requirements.txt