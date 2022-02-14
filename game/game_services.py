import asyncio
import pickle

from fastapi.exceptions import HTTPException
from db import db
from game.enum import TypeMessage


class Timer:
    def __init__(self):
        self.counter = 0
        self.amount_seconds = 0

    async def countdown(self, interval: int, manager):
        """
        Отсчёт времени для одного пользователя
        :interval: время для решения задания
        """
        self.counter = interval
        while self.counter > 0:
            await manager.broadcast(str(self.counter), TypeMessage.TIMER.name)
            self.counter -= 1
            self.amount_seconds += 1
            await asyncio.sleep(1)
        self.counter = 0
        self.amount_seconds = 0

    async def break_countdown(self):
        """Сброс времени"""
        self.counter = 0
        self.amount_seconds = 0


class Game:
    def __init__(self, db):
        self.level_task = 1  # уровень сложности вопросов(состоит из среднего уровня 2х игроков)
        self.db = db
        self.all_question = []
        self.game_id = None

    async def define_general_level(self, level_user_1, level_user_2):
        """
        Определение общего уровня сложности игроков
        :level_user_1: уровень первого игрока
        :level_user_2: уровень второго игрока
        """
        self.level_task = (level_user_1 + level_user_2) // 2

    async def get_random_task(self):
        # // TODO добавить уровень сложности для игроков в запрос к бд
        """Получение рандомных вопросов для игры"""
        try:
            task = (
                await self.db.get_random_question()
            )
            self.all_question = task
        except:
            raise HTTPException(
                status_code=400, detail="Ошибка получения заданий"
            )

    async def check_answer(self, user_answer):
        try:
            if self.current_question.right_answer == user_answer:
                return True
            else:
                return False
        except Exception:
            raise HTTPException(
                status_code=400, detail="Ошибка сравнения ответа пользователя"
            )

    async def record_answer(
        self,
        user_id: int,
        right_answer: bool,
        question_id: int,
        time: float,
        redis,
    ):
        """
        Метод для записи времени и верного ответа в redis
        :user_id: пользовательский id
        :right_answer: правильный ответ данный на задание(используется как bool значение)
        :question_id id: вопроса на который получен правильный ответ то пользователя
        :time: время за которое выполнено задание
        """
        try:
            key = f"br_game:{self.game_id}:{user_id}:{question_id}"
            answer_user = {"right_answer": int(right_answer), "time": time}
            await redis.set(key, pickle.dumps(answer_user))
        except Exception as e:
            print(e)

    async def calculation_result_game_user(self, user_id: int, redis):
        """Вычисление результата игры"""
        cur = b"0"
        while cur:
            cur, keys = await redis.scan(cur, match=f"br_game:{user_id}:*")
            print("Iteration results:", keys)
        # //TODO продолжить логику расчёта разультата(после расчёта удалить записи пользователя из redis)


game = Game(db)
