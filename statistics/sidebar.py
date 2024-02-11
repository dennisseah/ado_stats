from typing import Any

import streamlit as st
from tabulate import tabulate

from services.bugs import fetch as fetch_bugs
from services.features import fetch as fetch_features
from services.git_repositories import fetch as fetch_repositories
from services.milestones import fetch as fetch_milestones
from services.pull_requests import fetch as fetch_pull_requests
from services.tasks import fetch as fetch_tasks
from services.user_stories import fetch as fetch_stories


class Sidebar:
    def __init__(self, streamlit: bool):
        self.streamlit = streamlit

    def completion_rate(
        self, title: str, total: list[Any], attr_name: str = "state"
    ) -> tuple[str, str] | None:
        if total:
            completed = len(
                [
                    f
                    for f in total
                    if getattr(f, attr_name)
                    in [
                        "Closed",
                        "Resolved",
                        "Removed",
                        "completed",
                        "abandoned",
                        "Done",
                    ]
                ]
            )
            ratio = completed / len(total) if len(total) > 0 else 0

            if self.streamlit:
                st.metric(
                    label=title,
                    value=f"{completed}/{len(total)}",
                    delta=f"completed {ratio:.0%}",
                    delta_color=("inverse" if ratio < 0.5 else "normal"),
                )

            return (title, f"{completed}/{len(total)} ({ratio:.0%})")
        return None

    def milesstone_completion_rate(self) -> list[tuple[str, str]]:
        milestones = fetch_milestones()
        past = [m.path for m in milestones if m.timeframe == "past"]
        completed = len(past)
        ratio = completed / len(milestones) if len(milestones) > 0 else 0

        if self.streamlit:
            st.metric(
                label="Milestones",
                value=f"{completed}/{len(milestones)}",
                delta=f"completed {ratio:.0%}",
                delta_color="off",
            )

        user_stories = [
            x for x in fetch_stories() if x.milestone and x.milestone in past
        ]
        points = sum([x.story_points for x in user_stories])

        if self.streamlit:
            st.metric(
                label="Ave. Story Points per Milestone",
                value=f"{points/len(past):.1f}",
            )

        return [
            ("Milestones", f"{completed}/{len(milestones)} ({ratio:.0%})"),
            ("Ave. Story Points per Milestone", f"{points/len(past):.1f}"),
        ]

    def render_streamlit(self):
        with st.sidebar:
            self.milesstone_completion_rate()
            st.markdown("---")

            self.completion_rate("Features", fetch_features())
            self.completion_rate("User Stories", fetch_stories())
            self.completion_rate("Tasks", fetch_tasks())
            self.completion_rate("Bugs", fetch_bugs())

            pull_requests = []
            for repo in fetch_repositories():
                pull_requests += fetch_pull_requests(repo)

            self.completion_rate(
                title="Pull Requests", total=pull_requests, attr_name="status"
            )

    def render(self):
        if self.streamlit:
            st.markdown(
                """
                <style>
                    section[data-testid="stSidebar"] {
                        width: 200px;
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
            self.render_streamlit()
        else:
            rows = self.milesstone_completion_rate()

            features = self.completion_rate("Features", fetch_features())
            if features:
                rows.append(features)

            stories = self.completion_rate("User Stories", fetch_stories())
            if stories:
                rows.append(stories)

            tasks = self.completion_rate("Tasks", fetch_tasks())
            if tasks:
                rows.append(tasks)

            bugs = self.completion_rate("Bugs", fetch_bugs())
            if bugs:
                rows.append(bugs)

            pull_requests = []
            for repo in fetch_repositories():
                pull_requests += fetch_pull_requests(repo)

            prs = self.completion_rate(
                title="Pull Requests", total=pull_requests, attr_name="status"
            )
            if prs:
                rows.append(prs)

            print(tabulate(rows, headers=["Title", "Completion Rate"], tablefmt="grid"))
