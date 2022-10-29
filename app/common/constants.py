from enum import Enum


class GenderChoices(str, Enum):
    M = "M"
    F = "F"
    O = "O"


default_profile_url = 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg'
database_url = "postgresql+asyncpg://postgres:password@localhost:5432/new_db2"
