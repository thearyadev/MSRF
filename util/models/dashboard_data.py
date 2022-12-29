from pydantic import BaseModel
from util import GeneratedDashboardDataModel
from rich import print

class DashboardData(GeneratedDashboardDataModel): ...


if __name__ == "__main__":
    p = "F:\Documents\Python Projects\MSRF-DEV\dashboard_data_schema_source.json"
    with open(p, "r") as f:
        import json
        dashboard = DashboardData(**json.load(f))
        print(dashboard.userStatus.levelInfo)
