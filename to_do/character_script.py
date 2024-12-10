import requests
from .models import UserCharacter, Skills 

def get_character_data(user, character_name):
    """
    A script which is called by the profile view. Fetches Json data from the oldschool
    runescape hiscores using the name entered by the user. Takes only the 'skills' data
    and organises this data.
    """

    url = f'https://secure.runescape.com/m=hiscore_oldschool/index_lite.json?player={character_name}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json() 


        print("API Response JSON:", data)

        user_character, created = UserCharacter.objects.get_or_create(
            user=user,
            character_name=character_name
        )

        skills_list = data['skills']
        for skill in skills_list:
            Skills.objects.update_or_create(
                user_character=user_character,
                name=skill['name'],
                defaults={
                    "rank": skill.get("rank", None),
                    "level": skill.get("level", 1),
                    "experience": skill.get("xp", 0),
                }
            )
        return True
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
    return False

