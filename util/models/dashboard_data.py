import typing

from pydantic import BaseModel, root_validator
from rich import print

from .dashboard_json_models import DashboardDataModel


class DashboardData(DashboardDataModel): ...
