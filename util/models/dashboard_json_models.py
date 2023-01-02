from __future__ import annotations

import json
from typing import Any, List, Optional, Dict

from pydantic import BaseModel, Extra, Field
from rich import print

"""
This file models the data retrieved from rewards.bing.com.
The data is 4000 lines of JSON. Converted into Pydantic models. 
If the data is malformed or changed, this will cause errors. 
 """


class PcSearch(BaseModel):
    pointProgress: Optional[int] = None
    pointProgressMax: Optional[int] = None


class MobileSearch(BaseModel):
    pointProgressMax: Optional[int] = None
    pointProgress: Optional[int] = None


class Counters(BaseModel):
    pcSearch: Optional[List[PcSearch]] = None


class LevelInfo(BaseModel):
    activeLevel: Optional[str] = None
    activeLevelName: Optional[str] = None
    progress: Optional[int] = None
    progressMax: Optional[int] = None


class UserStatus(BaseModel):
    availablePoints: Optional[int] = None
    lifetimePoints: Optional[int] = None
    lifetimePointsRedeemed: Optional[int] = None
    counters: Optional[Counters] = None


class DailyPromotion(BaseModel):
    destinationUrl: Optional[str] = None
    complete: Optional[bool] = None
    promotionType: Optional[str] = None
    pointProgress: Optional[int] = None
    pointProgressMax: Optional[int] = None


class PunchCardParentAttributes(BaseModel):
    destination: Optional[str] = None


class PunchCardParentPromotion(BaseModel):
    name: Optional[str] = None
    pointProgress: Optional[int] = None
    pointProgressMax: Optional[int] = None
    destinationUrl: Optional[str] = None
    complete: Optional[bool] = None
    attributes: Optional[PunchCardParentAttributes] = None


class PunchCardChildPromotion(BaseModel):
    name: Optional[str] = None
    pointProgress: Optional[int] = None
    pointProgressMax: Optional[int] = None
    destinationUrl: Optional[str] = None
    complete: Optional[bool] = None
    promotionType: Optional[str] = None


class PunchCards(BaseModel):
    name: Optional[str] = None
    parentPromotion: Optional[PunchCardParentPromotion] = None
    childPromotion: Optional[List[PunchCardChildPromotion]] = None


class MorePromotion(BaseModel):
    complete: Optional[bool] = None
    promotionType: Optional[str] = None
    pointProgressMax: Optional[int] = None
    pointProgress: Optional[int] = None
    destinationUrl: Optional[str] = None


class DashboardDataModel(BaseModel):
    userStatus: Optional[UserStatus] = None
    dailySetPromotions: Optional[Dict[str, List[DailyPromotion]]] = None
    punchCards: Optional[List[PunchCards]] = None
    morePromotions: Optional[List[MorePromotion]] = None


if __name__ == '__main__':
    with open("../../dashboard_data_schema_source.json", "r") as file:
        data = json.load(file)
        print(DashboardDataModel(**data))
