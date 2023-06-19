import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from forms import Form_Answer, Form_new_task
from config import TOKEN, DJANGO_SERVER_URL

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/newtask", "/tasks")
    await message.answer("Введите личный код", reply_markup=keyboard)
    await Form_Answer.waiting_for_code.set()


@dp.message_handler(state=Form_Answer.waiting_for_code)
async def link_account(message: types.Message, state: FSMContext):
    tg_username = message.from_user.username
    code = message.text
    response = requests.post(f'{DJANGO_SERVER_URL}/link-account/', data={
        'tg_username': tg_username,
        'code': code,
    })
    if response.status_code == 200:
        await message.answer("Ваш аккаунт был успешно связан.")
        await state.finish()
    else:
        await message.answer("Произошла ошибка при связывании вашего аккаунта. Пожалуйста, попробуйте еще раз.")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer("/newtask — создать новую задачу\n/tasks — просмотреть все задачи")


@dp.message_handler(commands=['newtask'])
async def new_task(message: types.Message):
    await message.answer("Пожалуйста, введите название задачи.")
    await Form_new_task.waiting_for_title.set()


@dp.message_handler(state=Form_new_task.waiting_for_title)
async def receive_title(message: types.Message, state: FSMContext):
    title = message.text
    await Form_new_task.next()
    await state.update_data(title=title)
    await message.answer("Введите описание задачи.")


@dp.message_handler(state=Form_new_task.waiting_for_description)
async def receive_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    task_data = await state.get_data()
    tg_username = message.from_user.username
    response = requests.post(f'{DJANGO_SERVER_URL}/create-task/', data={
        'tg_username': tg_username,
        'title': task_data['title'],
        'description': task_data['description'],
    })
    if response.status_code == 201:
        await state.finish()
        await message.answer("Задача успешно создана.")
    else:
        await state.finish()
        await message.answer("Задача не создана.")


@dp.message_handler(commands=['tasks'])
async def tasks(message: types.Message):
    tg_username = message.from_user.username
    response = requests.get(f'{DJANGO_SERVER_URL}/get-tasks/', params={
        'tg_username': tg_username,
    })
    if response.status_code == 200:
        try:
            tasks = response.json()
        except ValueError:
            await message.answer(f"Ответ сервера: {response.text}")
            return
        for task in tasks:
            await message.answer(
                f"Task: {task['title']}\nDescription: {task['description']}\nCompleted: {task['completed']}")
    else:
        await message.answer(f"Не удалось получить задачи. Код: {response.status_code}")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)