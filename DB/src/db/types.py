from enum import StrEnum

class UserRole(StrEnum):
    ENERGY = "Модуль Энергии"
    STORAGE = "Модуль Памяти"
    CONNECTIONS = "Модуль Связи"
    SECURITY = "Модуль Безопасности"
    RHYTHM = "Модуль Ритма"
    CRITICS = "Модуль Критики"

class ReactionsTypes(StrEnum):
    FIRE = "Огонь"
    CRINGE = "Кринж"