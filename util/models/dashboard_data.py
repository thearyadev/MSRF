import typing

from pydantic import BaseModel, root_validator
from .codegen_models import GeneratedDashboardDataModel
from rich import print


class DashboardData(GeneratedDashboardDataModel): ...

