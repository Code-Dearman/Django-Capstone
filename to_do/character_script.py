import requests
from .models import UserCharacter, Skills 

def get_character_data(user, character_name):
    url = f'https://secure.runescape.com/m=hiscore_oldschool/index_lite.json?player={character_name}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # Parse the JSON response

        # Debugging: Print the entire JSON response to the console
        print("API Response JSON:", data)

        user_character, created = UserCharacter.objects.get_or_create(
            user=user,
            character_name=character_name
        )

        # Process skills directly from the list
        skills_list = data['skills']  # Extract the list directly
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

