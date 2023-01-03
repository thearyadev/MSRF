import typing

from pydantic import BaseModel, root_validator
from .dashboard_json_models import DashboardDataModel
from rich import print


class DashboardData(DashboardDataModel): ...
