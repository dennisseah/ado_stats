from statistics.base import aggr_accumulated, aggr_state, lifecycle

from configurations.azdo_settings import Azdo_Settings
from services.features import fetch as fetch_features


def generate(settings: Azdo_Settings):
    features = fetch_features(settings)

    print("Feature by states")
    aggr_state(data=features)

    print("Contributors to features")
    lifecycle(data=features)

    print("Accumulated features")
    aggr_accumulated(data=features)
