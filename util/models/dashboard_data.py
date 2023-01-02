import typing

from pydantic import BaseModel, root_validator
from .dashboard_json_models import GeneratedDashboardDataModel
from rich import print


class DashboardData(GeneratedDashboardDataModel): ...
