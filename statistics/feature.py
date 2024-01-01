from statistics.base import aggr_accumulated, aggr_state, lifecycle

from configurations.azdo_settings import Azdo_Settings
from services.features import fetch as fetch_features


def generate(settings: Azdo_Settings):
    features = fetch_features(settings)

    aggr_state(title="Feature by states", data=features)
    lifecycle(title="Feature Counts", data=features)
    aggr_accumulated(title="Accumulated features", data=features)
