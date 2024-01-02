import logging

import requests

from configurations.azdo_settings import Azdo_Settings
from models.pipeline import Pipeline, PipelineRun


def fetch_ids(settings: Azdo_Settings) -> list[Pipeline]:
    logging.info("[STARTED] Fetching pipeline ids")

    url = f"{settings.get_rest_base_uri()}/pipelines"
    params: dict[str, str | int] = {"api-version": "7.0"}

    response = requests.get(url, params=params, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        logging.info("[COMPLETED] Fetching pipeline ids")
        return [Pipeline.from_data(p) for p in response.json()["value"]]

    logging.error(f"Error fetching pipeline ids: {response.text}")
    raise ValueError("Cannot fetch pipeline identifiers")


def fetch_runs(settings: Azdo_Settings, pipeline_id: str) -> list[PipelineRun]:
    logging.info(f"[STARTED] Fetching pipeline runs for {pipeline_id}")

    url = f"{settings.get_rest_base_uri()}/pipelines/{pipeline_id}/runs"
    params: dict[str, str | int] = {"api-version": "7.0"}

    response = requests.get(url, params=params, auth=("", settings.azdo_pat))

    if response.status_code == 200:
        logging.info(f"[COMPLETED] Fetching pipeline runs for {pipeline_id}")
        return [PipelineRun.from_data(x) for x in response.json()["value"]]

    logging.error(f"Error fetching pipeline runs for {pipeline_id}: {response.text}")
    raise ValueError("Cannot fetch pipeline runs")


def fetch(settings: Azdo_Settings) -> list[Pipeline]:
    pipelines = fetch_ids(settings=settings)

    for p in pipelines:
        p.runs = fetch_runs(settings=settings, pipeline_id=p.id)

    return [p for p in pipelines if p.runs]
