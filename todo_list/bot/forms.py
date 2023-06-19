from aiogram.dispatcher.filters.state import State, StatesGroup


class Form_new_task(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()


class Form_Answer(StatesGroup):
    waiting_for_code = State()
    waiting_for_task_info = State()