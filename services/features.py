from configurations.azdo_settings import Azdo_Settings
from models.feature import Feature
from services.workitems import get_all_items


def fetch(settings: Azdo_Settings):
    return get_all_items(settings=settings, kind="Feature", creator=Feature.from_data)
