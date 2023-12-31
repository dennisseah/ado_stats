from datetime import datetime

from pydantic import BaseModel

from utils.date_utils import to_date, to_week


class WorkItem(BaseModel):
    id: str
    title: str
    description: str
    type: str
    area_path: str
    milestone: str
    state: str
    created_date: datetime
    created_week: str | None
    created_by: str
    changed_date: datetime | None
    changed_week: str | None
    changed_by: str
    closed_date: datetime | None
    closed_week: str | None
    closed_by: str | None
    assigned_to: str | None
    story_points: int

    @classmethod
    def from_data(cls, data: dict) -> "WorkItem":
        fields = data["fields"]
        area_paths = fields["System.AreaPath"].split("\\")
        area_path = area_paths[1] if len(area_paths) > 1 else ""

        created_date = to_date(fields["System.CreatedDate"])
        changed_date = to_date(fields.get("System.ChangedDate", None))
        closed_date = to_date(fields.get("Microsoft.VSTS.Common.ClosedDate", None))

        created_week = to_week(created_date)
        changed_week = to_week(changed_date)
        closed_week = to_week(closed_date)

        return WorkItem(
            id=str(data["id"]),
            title=fields["System.Title"],
            description=fields.get("System.Description", ""),
            type=fields["System.WorkItemType"],
            area_path=area_path,
            milestone=fields.get("System.IterationPath", None),
            state=fields["System.State"],
            created_date=created_date,  # type: ignore
            created_week=created_week,
            created_by=fields["System.CreatedBy"]["uniqueName"],
            changed_date=changed_date,
            changed_week=changed_week,
            story_points=fields.get("Microsoft.VSTS.Scheduling.StoryPoints", 5),
            changed_by=(
                fields["System.ChangedBy"].get("uniqueName")  # type: ignore
                if "System.ChangedBy" in fields
                else None
            ),
            assigned_to=(
                fields["System.AssignedTo"].get("uniqueName")  # type: ignore
                if "System.AssignedTo" in fields
                else None
            ),
            closed_date=closed_date,
            closed_week=closed_week,
            closed_by=(
                fields["Microsoft.VSTS.Common.ClosedBy"]["uniqueName"]  # type: ignore
                if "Microsoft.VSTS.Common.ClosedBy" in fields
                else None
            ),
        )
