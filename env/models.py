from pydantic import BaseModel

class Observation(BaseModel):
    task: int
    severity: float
    cvss_base: float
    cvss_temporal: float
    cvss_environmental: float

class ActionRequest(BaseModel):
    action: int
