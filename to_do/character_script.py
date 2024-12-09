import requests
from .models import UserCharacter, Skills 

def get_character_data(user, character_name):
    url = f'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={character_name}'
    response = requests.get(url)

    if response.status_code == 200:
        user_character, created = UserCharacter.objects.get_or_create(
            user=user, character_name=character_name
        )

        skills = response.text.splitlines()
        skill_names = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a", "a","a", "a", "a", "a", "a", "a", "a", "a"]

        for i, skill_data in enumerate(skills):
            rank, level, experience = skill_data.split(",")
            Skills.objects.update_or_create(
                user_character=user_character,
                name=skill_names[i],
                defaults={
                    "rank": int(rank) if rank.isdigit() else None,
                    "level": int(level) if level.isdigit() else 1,
                    "experience": int(experience) if experience.isdigit() else 0,
                }
            )
        return True
    return False