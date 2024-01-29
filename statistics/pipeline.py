from services.pipelines import fetch as fetch_pipelines
from utils.display import Table, as_table_group


def generate(title: str, streamlit: bool = False):
    """Generate statistics for pipelines.

    :param title: The title of the statistics.
    :param streamlit: Whether to display the statistics in Streamlit.
    """
    pipelines = fetch_pipelines()

    results = []
    for p in pipelines:
        total = len(p.runs)
        completed = len([x for x in p.runs if x.result == "succeeded"])

        runs = [x for x in p.runs if x.run_duration]
        ave_duration = 0
        if runs:
            total_duration = sum([run.run_duration for run in runs])  # type: ignore
            ave_duration = round(total_duration / len(runs))
        min_sec = divmod(ave_duration, 60)
        str_ave_duration = f"{min_sec[0]}m {min_sec[1]}s"
        results.append((p.name, total, completed, str_ave_duration))

    as_table_group(
        group_name=title,
        tables=[
            Table(
                title="Runs",
                headers=["name", "total", "completed", "ave duration"],
                data=results,
            )
        ],
        streamlit=streamlit,
    )
