from typing import Callable

import streamlit as st

from services.bugs import fetch as fetch_bugs
from services.features import fetch as fetch_features
from services.milestones import fetch as fetch_milestones
from services.tasks import fetch as fetch_tasks
from services.user_stories import fetch as fetch_stories


def completion_rate(title: str, fn: Callable):
    total = fn()

    if total:
        completed = len(
            [f for f in total if f.state in ["Closed", "Resolved", "Removed"]]
        )
        ratio = completed / len(total) if len(total) > 0 else 0

        st.metric(
            label=title,
            value=f"{completed}/{len(total)}",
            delta=f"completed {ratio:.0%}",
            delta_color=("inverse" if ratio < 0.5 else "normal"),
        )


def milesstone_completion_rate():
    milestones = fetch_milestones()
    past = [m.path for m in milestones if m.timeframe == "past"]
    completed = len(past)
    ratio = completed / len(milestones) if len(milestones) > 0 else 0

    st.metric(
        label="Milestones",
        value=f"{completed}/{len(milestones)}",
        delta=f"completed {ratio:.0%}",
        delta_color="off",
    )

    user_stories = [x for x in fetch_stories() if x.milestone and x.milestone in past]
    points = sum([x.story_points for x in user_stories])
    st.metric(
        label="Ave. Story Points per Milestone",
        value=f"{points/len(past):.1f}",
    )


def render():
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 200px !important;
                background-color: #F5F6F79A !important;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.5rem !important;
            }
            [data-testid="stMetricDelta"] svg {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        milesstone_completion_rate()
        st.divider()

        completion_rate("Features", fetch_features)
        completion_rate("User Stories", fetch_stories)
        completion_rate("Tasks", fetch_tasks)
        completion_rate("Bugs", fetch_bugs)
