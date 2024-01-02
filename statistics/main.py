from statistics.bug import generate as generate_bug
from statistics.feature import generate as generate_feature
from statistics.milestone import generate as generate_milestone
from statistics.pull_request import generate as generate_pull_request
from statistics.task import generate as generate_task
from statistics.user_story import generate as generate_user_story

import streamlit as st

from configurations.azdo_settings import Azdo_Settings

with_st = False

# command for streamlit and without streamlit respectively:
#
# `python -m streamlit run statistics/main.py`
# `python -m statistics.main`


if __name__ == "__main__":
    settings = Azdo_Settings.model_validate({})

    titles = [
        "Milestones",
        "Features",
        "User Stories",
        "Tasks",
        "Bugs",
        "Pull Requests",
    ]

    tabs = tabs = st.tabs(titles) if with_st else []

    for i, genr in enumerate(
        [
            generate_milestone,
            generate_feature,
            generate_user_story,
            generate_task,
            generate_bug,
            generate_pull_request,
            # generate_git_branches,
        ]
    ):
        if with_st:
            tab = tabs[i]
            with tab:  # type: ignore
                genr(settings=settings, title=titles[i], streamlit=True)
        else:
            genr(settings=settings, title=titles[i])
