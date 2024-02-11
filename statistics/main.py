from statistics.bug import generate as generate_bug
from statistics.burndown import generate as generate_burndown
from statistics.feature import generate as generate_feature
from statistics.git_branches import generate as generate_git_branches
from statistics.milestone import generate as generate_milestone
from statistics.pull_request import generate as generate_pull_request
from statistics.sidebar import Sidebar
from statistics.task import generate as generate_task
from statistics.user_story import generate as generate_user_story

import streamlit as st

from configurations.azdo_settings import Azdo_Settings

# command for streamlit and without streamlit respectively:
#
# `python -m streamlit run statistics/main.py`
# `python -m statistics.main`


def main(with_st: bool = False):
    settings = Azdo_Settings.model_validate({})

    titles = [
        "Burndown Chart",
        "Milestones",
        "Features",
        "User Stories",
        "Tasks",
        "Bugs",
        "Pull Requests",
        # "Pipelines",
        "Git Branches",
    ]

    if with_st:
        col1, col2 = st.columns([8, 1])

        with col1:
            st.markdown(settings.azdo_org_name)
            if settings.crew:
                st.markdown(settings.crew)

        with col2:
            st.button("MVE", type="secondary", disabled=True)
    else:
        print(settings.azdo_org_name)
        if settings.crew:
            print(settings.crew)
        print()

    Sidebar(streamlit=with_st).render()

    tabs = st.tabs(titles) if with_st else []

    for i, genr in enumerate(
        [
            generate_burndown,
            generate_milestone,
            generate_feature,
            generate_user_story,
            generate_task,
            generate_bug,
            generate_pull_request,
            # generate_pipeline,
            generate_git_branches,
        ]
    ):
        if with_st:
            tab = tabs[i]
            with tab:  # type: ignore
                genr(title=titles[i], streamlit=True)
        else:
            genr(title=titles[i])


if __name__ == "__main__":
    import sys

    with_st = "statistics/main.py" == sys.argv[0]
    main(with_st=with_st)
