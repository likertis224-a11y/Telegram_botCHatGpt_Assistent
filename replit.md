# Replit Agent Guide

## Overview

This is a Telegram bot built with Python using the aiogram framework. The bot provides a simple interactive menu system with features like viewing a class schedule and user profile. It uses reply keyboard markup for navigation with a flow: `/start` → "🚀 Запуск" (Launch) → Main Menu with "📅 Расписание" (Schedule) and "👤 Мой профиль" (My Profile) options. The bot interface is in Russian, suggesting it's targeted at Russian-speaking students.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Framework**: aiogram (async Telegram Bot framework for Python)
- **Python async**: Uses `asyncio` for asynchronous message handling
- **Dispatcher pattern**: aiogram's `Dispatcher` handles routing of incoming messages to handler functions
- **Filters**: Uses `Command` filter for slash commands and `F.text` filter for button text matching

### Application Structure
- **Single-file architecture**: The entire bot logic lives in `main.py`. As the bot grows, consider splitting into modules (handlers, keyboards, config, etc.)
- **Navigation flow**: Linear menu navigation using `ReplyKeyboardMarkup` buttons — start screen → main menu → feature screens
- **No database**: Currently no persistent storage; all data is hardcoded. If adding user profiles or dynamic schedules, a database (like SQLite or PostgreSQL) would be needed.
- **No state management**: The bot doesn't use aiogram's FSM (Finite State Machine) yet. If multi-step interactions are added (like forms or settings), FSM should be implemented.

### Security Concern
- The bot token is hardcoded directly in the source file. This should be moved to environment variables (e.g., using `os.getenv("BOT_TOKEN")`) for security.

### Entry Point
- `main.py` is the sole entry point. It defines the bot, dispatcher, keyboard layouts, and message handlers. The file appears to be incomplete (the schedule handler text is truncated).

## External Dependencies

### Python Packages
- **aiogram**: Core dependency — async Telegram Bot API framework (version 3.x based on the import style with `F` filters and `Command` from `aiogram.filters`)
- **asyncio**: Python standard library for async event loop

### External Services
- **Telegram Bot API**: The bot communicates with Telegram's servers using a bot token. The token is currently hardcoded and should be stored as an environment variable named `BOT_TOKEN` or similar.

### No Database
- No database is currently configured. If persistent storage is needed in the future, consider adding SQLite for simplicity or PostgreSQL for production use.