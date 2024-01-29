import logging

import requests

from configurations.azdo_settings import Azdo_Settings
from models.pipeline import Pipeline, PipelineRun


def fetch_ids() -> list[Pipeline]:
    """Fetch pipeline identifiers from Azure DevOps

    :return: A list of pipeline identifiers.
    """
    settings = Azdo_Settings.model_validate({})
    logging.info("[STARTED] Fetching pipeline ids")

    url = f"{settings.get_rest_base_uri()}/pipelines"

    response = requests.get(
        url,
        auth=("", settings.azdo_pat),
        headers={"Accept": "application/json; api-version=7.0"},
    )

    if response.status_code == 200:
        logging.info("[COMPLETED] Fetching pipeline ids")
        return [Pipeline.from_data(p) for p in response.json()["value"]]

    logging.error(f"Error fetching pipeline ids: {response.text}")
    raise ValueError("Cannot fetch pipeline identifiers")


def fetch_runs(pipeline_id: str) -> list[PipelineRun]:
    """Fetch pipeline runs from Azure DevOps

    :param pipeline_id: The pipeline identifier to fetch runs for.
    :return: A list of pipeline runs.
    """
    settings = Azdo_Settings.model_validate({})
    logging.info(f"[STARTED] Fetching pipeline runs for {pipeline_id}")

    url = f"{settings.get_rest_base_uri()}/pipelines/{pipeline_id}/runs"

    response = requests.get(
        url,
        auth=("", settings.azdo_pat),
        headers={"Accept": "application/json; api-version=7.0"},
    )

    if response.status_code == 200:
        logging.info(f"[COMPLETED] Fetching pipeline runs for {pipeline_id}")
        return [PipelineRun.from_data(x) for x in response.json()["value"]]

    logging.error(f"Error fetching pipeline runs for {pipeline_id}: {response.text}")
    raise ValueError("Cannot fetch pipeline runs")


def fetch() -> list[Pipeline]:
    """Fetch pipeline runs from Azure DevOps

    :return: A list of pipelines with runs.
    """
    pipelines = fetch_ids()

    for p in pipelines:
        p.runs = fetch_runs(pipeline_id=p.id)

    return [p for p in pipelines if p.runs]
