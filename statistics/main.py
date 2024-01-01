from statistics.bug import generate as generate_bug
from statistics.feature import generate as generate_feature
from statistics.milestone import generate as generate_milestone
from statistics.pull_request import generate as generate_pull_request
from statistics.task import generate as generate_task
from statistics.user_story import generate as generate_user_story

from configurations.azdo_settings import Azdo_Settings

if __name__ == "__main__":
    settings = Azdo_Settings.model_validate({})

    generate_feature(settings)
    generate_milestone(settings)
    generate_user_story(settings)
    generate_task(settings)
    generate_bug(settings)
    generate_pull_request(settings)
    print()
