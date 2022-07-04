from dataclasses import dataclass
from typing import Optional

from src.utils.decorators import nested_dataclass


@dataclass
class _NequiResponseStatus:
    StatusCode: str
    StatusDesc: str


@dataclass
class _NequiResponseDestination:
    ServiceName: str
    ServiceOperation: str
    ServiceRegion: str
    ServiceVersion: str


@nested_dataclass
class _NequiResponseHeader:
    Channel: str
    ResponseDate: str
    MessageID: str
    ClientID: str
    Status: _NequiResponseStatus
    Destination: Optional[_NequiResponseDestination] = None


@nested_dataclass
class _NequiResponseBody:
    any: dict


@nested_dataclass
class _NequiResponseMessage:
    ResponseHeader: _NequiResponseHeader
    ResponseBody: _NequiResponseBody


@nested_dataclass
class NequiResponse:
    ResponseMessage: _NequiResponseMessage
