from pydantic import BaseModel, Field


class Task(BaseModel):
    question: str = Field(..., description="Вопрос")
    answer1: str = Field(..., description="Первый вариант ответа")
    answer2: str = Field(..., description="Второй вариант ответа")
    answer3: str = Field(..., description="Третий вариант ответа")
    answer4: str = Field(..., description="Четвертый вариант ответа")
