from pydantic import BaseModel


class Review(BaseModel):
    """
       VO for Review
    """

    class Summary(BaseModel):
        negative_total: int
        positive_total: int
        motivation_total: int
        sample_negative: int
        sample_positive: int
        sample_motivation: int

    payload: dict[str, dict]
    summary: Summary
