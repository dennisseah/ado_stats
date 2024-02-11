from models.user_story import UserStory
from services.features import fetch as fetch_features
from services.workitems import fetch_work_items
from utils.data_utils import divide_chunks
from utils.display import Table, as_table


def validate():
    features = [
        f
        for f in fetch_features()
        if f.state != "Closed" and f.state != "Removed" and f.state != "Resolved"
    ]

    child_ids = []
    for feature in features:
        child_ids += feature.child_ids

    user_stories = []
    for chunk in divide_chunks(child_ids, 200):
        user_stories += fetch_work_items(item_ids=chunk, creator=UserStory.from_data)

    closed_user_stories = set([us.id for us in user_stories if us.is_completed()])

    data = []
    for feature in features:
        if feature.child_ids and all(
            [child_id in closed_user_stories for child_id in feature.child_ids]
        ):
            data.append((feature.id, feature.title, feature.state, feature.created_by))

    as_table(
        Table(
            title="Features with all child User Stories closed",
            headers=["ID", "Title", "State", "Created By"],
            data=data,
        )
    )


validate()
