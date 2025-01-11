import asyncio
import aiogram
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

bot = aiogram.Bot("Bot_Token")
dp = aiogram.Dispatcher()


@dp.message(Command("start"))
async def start(message: aiogram.types.Message):
    kb = InlineKeyboardBuilder()
    webapp = aiogram.types.WebAppInfo(url="https://bastau-bot.github.io/test3/")
    button = aiogram.types.InlineKeyboardButton(text="Play", web_app=webapp)
    button1 = aiogram.types.InlineKeyboardButton(text="Instructions", callback_data="instr")
    kb.add(button)
    kb.add(button1)
    photo = FSInputFile("hello_.png")
    await bot.send_photo(message.from_user.id, caption="""<b>Welcome to the Financial Freedom Bot! 💰📈</b>\n\nHere, you’ll learn the basics of managing money, saving, investing, and making smart financial decisions. Whether you're just starting or want to improve your financial skills, we're here to guide you step by step.\n\n<i>Let’s build a solid foundation for your financial future together! 🚀</i>""",
                         parse_mode="HTML",
                         photo=photo,
                         reply_markup=kb.as_markup())
    """photo = FSInputFile("C:/Users/Lenovo/Documents/ok.jpg")"""
"""    await bot.send_photo(message.from_user.id, photo=photo, caption=f"Hello {message.chat.first_name}", reply_markup=kb.as_markup())
"""


@dp.callback_query(aiogram.F.data == "instr")
async def instr(callback: aiogram.types.CallbackQuery):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="""<b>How to Play:</b>\n\n<b>1. Choose a Topic 💡: </b>Select from topics like budgeting, saving, investing, or debt management.\n\n<b>2. Interactive Lessons 📝: </b>Complete short lessons and quizzes to deepen your understanding of financial concepts.\n\n<b>3. Track Your Progress 📊: </b>Follow your progress as you learn how to make smart financial decisions.\n\n<b>4. Simulations & Scenarios 🎮: </b>Practice with real-life scenarios like building a budget or planning an investment.\n\n<b>5. Earn Badges & Rewards 🏅: </b>Achieve milestones, earn badges, and become more financially literate!""",
                           parse_mode="HTML")

@dp.message(Command("test"))
async def test(message: aiogram.types.Message):
    kb = InlineKeyboardBuilder()
    button = aiogram.types.InlineKeyboardButton(text="yes" , callback_data="yes")
    button1 = aiogram.types.InlineKeyboardButton(text="no" , callback_data="no")
    kb.add(button)
    kb.add(button1)
    await bot.send_message(chat_id=message.chat.id,
                           text="""<b>Ready to Test Your Financial Knowledge? 💡</b>\nYou’re about to take a quick quiz that will challenge your understanding of essential financial concepts, like budgeting, saving, and investing. Don’t worry, it’s designed to be fun and educational! 🚀\n\nEach question is worth 1 point, so try your best to answer them all.\nDon’t stress if you don’t know everything—this is a great chance to learn something new!\nIf you score 3 or more points, you’re doing great! If not, keep practicing, and you’ll improve in no time.\n<i>When you’re ready, type yes and let's see how well you manage your finances. <b>Good luck!</b> 💰📊</i>""",
                           parse_mode="HTML",
                           reply_markup=kb.as_markup())
polls = [
    {
        'question': 'What is a budget?',
        'options': ['A) A list of items you want to buy',
                    'B) A plan for how you will spend your money',
                    'C) A record of all your past expenses',
                    'D) A loan from the bank'],
        'correct_option_id': 1
    },
    {
        'question': 'Which of these is the best way to grow your savings over time?',
        'options': ['A) Keeping money under the mattress',
                    'B) Investing in stocks or bonds',
                    'C) Spending less than you earn',
                    'D) Using a credit card for all purchases'],
        'correct_option_id': 1  # B is correct, but we'll handle C as well
    },
    {
        'question': 'What does a credit score represent?',
        'options': ['A) How much money you have saved',
                    'B) Your ability to repay loans',
                    'C) The number of loans you have',
                    'D) The amount of money you owe to the bank'],
        'correct_option_id': 1
    },
    {
        'question': 'Why is it important to have an emergency fund?',
        'options': ['A) To buy something expensive later',
                    'B) To cover unexpected expenses without going into debt',
                    'C) To lend money to friends',
                    'D) To avoid paying taxes'],
        'correct_option_id': 1
    },
    {
        'question': 'What is compound interest?',
        'options': ['A) Interest calculated on the original amount only',
                    'B) Interest earned on both the original amount and the interest that has been added',
                    'C) Interest you pay on loans',
                    'D) A fee charged by the bank for keeping your money'],
        'correct_option_id': 1
    }
]

current_poll_index = 0  # Keep track of the current poll
user_scores = {}

@dp.callback_query(aiogram.F.data == "yes")
async def start_poll(callback: aiogram.types.CallbackQuery):
    global current_poll_index
    current_poll_index = 0  # Reset to the first poll
    await send_poll(callback.message.chat.id, current_poll_index)


async def send_poll(chat_id, poll_index):
    if poll_index < len(polls):
        poll = polls[poll_index]
        await bot.send_poll(
            chat_id,
            question=poll['question'],
            options=poll['options'],
            type='quiz',
            correct_option_id=poll['correct_option_id'],
            is_anonymous=False
        )
    else:
        await bot.send_message(chat_id, "You've completed all the polls! Thank you for participating.")

ol = 0

@dp.poll_answer()
async def handle_poll_answer(poll_answer: aiogram.types.PollAnswer):
    user_id = poll_answer.user.id  # Get the user ID of the person who answered
    user_scores[user_id] = 0
    selected_option_id = poll_answer.option_ids[0]  # Get the selected option ID
    global current_poll_index
    global ol
    if current_poll_index < len(polls):
        correct_option_id = polls[current_poll_index]['correct_option_id']
        # Determine response based on the selected option
        if selected_option_id == correct_option_id:
            ol = ol + 1
            user_scores[user_id] += 1  # Increment score for correct answer
            response_message = "Great choice! You selected the correct answer."
        elif current_poll_index == 1 and selected_option_id == 2:  # Handle spending less than you earn
            ol = ol + 1
            response_message = "That's a great point! Spending less than you earn is crucial for growing savings."
            user_scores[user_id] += 1
        else:
            response_message = "Thanks for participating! You selected the wrong answer."
        # Send feedback to the user
        await bot.send_message(user_id, response_message)
        # Move to the next poll
        current_poll_index += 1
    await send_poll(user_id, current_poll_index)
    # If all polls are answered, send the final score
    if current_poll_index >= len(polls):
        if ol == 5:
            await bot.send_message(user_id, "<b>5 Correct Answers:</b> Excellent! You have strong financial knowledge.", parse_mode="HTML")
            current_poll_index = 0
            ol = 0
        elif ol == 4 or ol == 3:
            await bot.send_message(user_id, f'<b>{ol} Correct Answers:</b> Great! You’re on the right track.', parse_mode="HTML")
            current_poll_index = 0
            ol = 0
        elif ol == 1 or ol == 2:
            await bot.send_message(chat_id=user_id, text=f'{ol} Correct Answers: Needs Improvement. Keep learning and practicing.', parse_mode="HTML")
            current_poll_index = 0
            ol = 0
        elif ol == 0:
            await bot.send_message(user_id, "<b>0 Correct Answers: </b>Bad. Don't worry, you'll improve with more practice!", parse_mode="HTML")
            current_poll_index = 0
            ol = 0

@dp.callback_query(aiogram.F.data == "no")
async def no(callback: aiogram.types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    webapp = aiogram.types.WebAppInfo(url="https://bastau-bot.github.io/test3/")
    button = aiogram.types.InlineKeyboardButton(text="Play", web_app=webapp)
    kb.add(button)
    await bot.send_message(callback.from_user.id, "If you are not ready, you can just play.",
                           reply_markup=kb.as_markup())


async def main():
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())