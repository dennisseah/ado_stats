from configurations.azdo_settings import Azdo_Settings
from models.bug import Bug
from services.workitems import get_all_items


def fetch(settings: Azdo_Settings):
    return get_all_items(settings=settings, kind="Bug", creator=Bug.from_data)
