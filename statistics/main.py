from statistics.bug import generate as generate_bug
from statistics.pull_request import generate as generate_pull_request
from statistics.task import generate as generate_task
from statistics.user_story import generate as generate_user_story

from configurations.azdo_settings import Azdo_Settings

if __name__ == "__main__":
    settings = Azdo_Settings.model_validate({})

    print()
    print("USER STORIES")
    print("============")
    generate_user_story(settings)
    print()
    print("TASKS")
    print("=====")
    generate_task(settings)
    print()
    print("BUGS")
    print("====")
    generate_bug(settings)
    print()
    print("PULL REQUESTS")
    print("=============")
    generate_pull_request(settings)
    print()
