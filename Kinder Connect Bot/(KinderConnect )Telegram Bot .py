# pip install python-telegram-bot --upgrade
from db import save_result
import os
from telegram import Update ,InlineKeyboardButton ,InlineKeyboardMarkup,InputMediaPhoto,InputFile
from telegram.ext import Application,CommandHandler,ContextTypes,MessageHandler,filters,CallbackQueryHandler
from telegram.ext import ContextTypes , CallbackContext,ConversationHandler
import random
import logging
import random


# Replace with Your Own bot token from BotFather
TOKEN = "7827825014:AAF2Q5BFp0Bn3lEY506ToJMHrJRpX6dQOaA"
user_scores = {}
# Define paths
IMAGE_PATH = "images"
AUDIO_PATH = "audio"
# # Define a command handler 
# async def start(update:Update,context):
#     await update.message.reply_text("👋 Hello!! I'm your learning KindeConnect Bot. Let's play and learn together!?")
# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I'm your magical KinderConnect Bot! 🎉\n"
        "Let's have fun learning together with games and activities:\n\n"
        "🧮 /math – Practice simple addition\n"
        "🎲 /counting – Count the fruits\n"
        "🎨 /colors – Identify the color\n"
        "🐾 /animals – Guess the animal\n"
        "🧠 /quiz – Answer a fun picture quiz\n"
        "📚 /storytime – Listen to a story\n"
        "🚗 /transport – Where does the vehicle move? (Land/Water/Air)\n"
        "🎧 /transport_sound – Guess the vehicle by its sound\n"
        "🌑 /transport_shadow – Guess from vehicle shadows\n"
        "🍎 /healthy_food_game – Is the food healthy or unhealthy?\n"
        "🍱 /lunchbox_game – Put food in the lunchbox or trash\n"
        "🧲 /opposites – Find the opposite word!\n\n"
        "🎯 Just type one of the commands above to start playing!"
    )
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("👋 Hello! I'm your magical KinderConnect Bot! 🎉\nLet's have fun learning together:\n\n"
#                                     "🧮 /math - Answer with addition/subtraction.Number comparison (bigger/smaller).Shape recognition,Matching numbers to quantities\n"
#                                     "🎲 /counting - Count the Apples\n"
#                                     "🎨 /colors - Name the Color\n"
#                                     "🐾 /animals - Guess the Animal\n"
#                                     "🧠 /quiz - Picture Quiz\n"
#                                     "📚 /storytime - Listen to a Story")

# Transport types and where they move
transport_data = [
    {"name": "Car", "file": "car.jpg", "moves": "Land"},
    {"name": "Boat", "file": "boat.jpg", "moves": "Water"},
    {"name": "Plane", "file": "plane.jpg", "moves": "Air"},
    {"name": "Train", "file": "train.jpg", "moves": "Land"},
]

# Start the transport game
def transport(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🚗 Let's learn about transportation!\nCan you guess where each vehicle moves?\n\n🌍 Choose: Land, Water, or Air")
    send_next_transport(update, context, 0)

# Send each transport image with choice buttons
def send_next_transport(update_or_callback, context: CallbackContext, index: int) -> None:
    if index >= len(transport_data):
        context.bot.send_message(chat_id=update_or_callback.effective_chat.id, text="🎉 Great job! You've completed this activity!")
        return

    vehicle = transport_data[index]
    image_path = os.path.join(IMAGE_PATH, vehicle["file"])
    keyboard = [
        [
            InlineKeyboardButton("🏞️ Land", callback_data=f"move_{index}_Land"),
            InlineKeyboardButton("🌊 Water", callback_data=f"move_{index}_Water"),
            InlineKeyboardButton("☁️ Air", callback_data=f"move_{index}_Air")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_photo(chat_id=update_or_callback.effective_chat.id, photo=open(image_path, 'rb'),
                           caption=f"What is this? Where does it move?", reply_markup=reply_markup)

# Handle answers
def handle_transport_answer(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    data = query.data.split("_")  # move_0_Land → ["move", "0", "Land"]
    index = int(data[1])
    answer = data[2]
    correct = transport_data[index]["moves"]

    if answer == correct:
        feedback = "✅ Correct!"
    else:
        feedback = f"❌ Oops! This moves on {correct}."

    query.edit_message_caption(caption=feedback)
    send_next_transport(query, context, index + 1)

quiz_data = [
    {
        "question": "What is this?",
        "image": "https://cdn.pixabay.com/photo/2013/07/12/18/39/sun-153246_960_720.png",
        "answer": "Sun",
        "options": ["Sun", "Moon", "Star"]
    },
    {
        "question": "What shape is this?",
        "image": "https://cdn.pixabay.com/photo/2012/04/10/17/22/circle-26620_960_720.png",
        "answer": "Circle",
        "options": ["Triangle", "Square", "Circle"]
    },
    {
        "question": "What object is this?",
        "image": "https://cdn.pixabay.com/photo/2016/04/01/09/30/ball-1300175_960_720.png",
        "answer": "Ball",
        "options": ["Ball", "Apple", "Balloon"]
    }
]

DRAWINGS = [
    "assets/drawings/Cat.png",
    "assets/drawings/Dog.png",
    "assets/drawings/lower.png",
    "assets/drawings/butterfly.png"
]


animal_data = [
    {
        "name": "Dog",
        "emoji": "🐶",
        "image": "https://cdn.pixabay.com/photo/2017/01/31/20/16/dog-2029214_960_720.png",
        "sound": "https://www.soundjay.com/animal/dog-bark-1.ogg"
    },
    {
        "name": "Cat",
        "emoji": "🐱",
        "image": "https://cdn.pixabay.com/photo/2017/01/31/20/16/cat-2029213_960_720.png",
        "sound": "https://www.soundjay.com/animal/cat-meow-2.ogg"
    },
    {
        "name": "Cow",
        "emoji": "🐮",
        "image": "https://cdn.pixabay.com/photo/2013/07/13/13/40/cow-160041_960_720.png",
        "sound": "https://www.soundjay.com/animal/cow-moo1.ogg"
    }
]

story_data = [
    {
        "title": "Goldilocks and the Three Bears",
        "performer": "Storyteller",
        "file": "stories/goldilocks.mp3"
    },
    {
        "title": "The Three Little Pigs",
        "performer": "Storyteller",
        "file": "stories/three_little_pigs.mp3"
    },
    {
        "title": "Little Red Riding Hood",
        "performer": "Storyteller",
        "file": "stories/little_red_riding_hood.mp3"
    }
]

# Define a list of fruit counting examples
fruit_counts = [
    {"emoji": "🍊", "name": "orange", "count": 3},
    {"emoji": "🥝", "name": "kiwi", "count": 4},
    {"emoji": "🍋", "name": "lemon", "count": 2},
    {"emoji": "🍓", "name": "strawberry", "count": 5},
    {"emoji": "🍇", "name": "grapes", "count": 6},
    {"emoji": "🍎", "name": "apple", "count": 1},
    {"emoji": "🍌", "name": "banana", "count": 3},
    {"emoji": "🍍", "name": "pineapple", "count": 2}
]

async def counting_game(update: Update, context: CallbackContext):
    # Pick a random fruit question
    fruit = random.choice(fruit_counts)
    correct = fruit["count"]

    # Create a string of repeated emojis
    fruit_display = fruit["emoji"] * correct

    # Generate answer choices
    options = list(set([
        correct,
        correct + 1,
        max(1, correct - 1),
        correct + 2
    ]))
    random.shuffle(options)

    # Create buttons
    keyboard = [[InlineKeyboardButton(str(opt), callback_data=f"count_{opt}")] for opt in options]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Store the correct answer for later use
    context.user_data["counting_correct"] = correct

    await update.message.reply_text(
        f"🔢 How many {fruit['name']}s do you see?\n\n{fruit_display}",
        reply_markup=reply_markup
    )

async def handle_count_answer(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    selected = int(query.data.split("_")[1])
    correct = context.user_data.get("counting_correct")

    if selected == correct:
        await query.edit_message_text(f"✅ Yes! That’s {correct} fruits! 🥳\n🎉 Great job!")
    else:
        await query.edit_message_text(f"❌ Oops! That’s not quite right.\nThere were {correct} fruits. 🍒 Try again!")

    # Offer to play again
    keyboard = [
        [InlineKeyboardButton("🔁 Try Another", callback_data="counting")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("🎮 What would you like to do next?", reply_markup=reply_markup)



# apple_image = "🍎"

# async def counting_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     count = random.choice([3, 5, 7])  # Random number of apples
#     apple_row = apple_image * count

#     options = [count - 2, count, count + 2]
#     random.shuffle(options)

#     keyboard = [
#         [InlineKeyboardButton(str(opt), callback_data="correct" if opt == count else "wrong")]
#         for opt in options
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await update.message.reply_text(
#         f"{apple_row}\n\nHow many apples do you see?",
#         reply_markup=reply_markup
#     )
async def color_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define available colors
    colors = [
        ("🔴", "Red"),
        ("🟢", "Green"),
        ("🔵", "Blue"),
        ("🟡", "Yellow"),
        ("🟣", "Purple"),
        ("🟠", "Orange")
    ]

    emoji, correct_color = random.choice(colors)

    # Prepare 3 options: 1 correct + 2 incorrect
    options = [correct_color]
    while len(options) < 3:
        opt = random.choice(colors)[1]
        if opt not in options:
            options.append(opt)
    random.shuffle(options)

    keyboard = [
        [InlineKeyboardButton(opt, callback_data="correct" if opt == correct_color else "wrong")]
        for opt in options
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"{emoji}\n\nWhat color is this?",
        reply_markup=reply_markup
    )
async def drawing_game(update, context: ContextTypes.DEFAULT_TYPE):
    drawing_path = random.choice(DRAWINGS)

    try:
        with open(drawing_path, "rb") as img:
            await update.message.reply_photo(
                photo=img,
                caption="🎨 Can you color this picture? Ask an adult to print it or color it digitally! You can send me your colored version when you're done!"
            )
    except FileNotFoundError:
        await update.message.reply_text("❌ Drawing not found.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
    finally:
        os.remove(drawing_path)

async def receive_coloring(update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        await update.message.reply_text("🎉 Wow! Great coloring! Keep it up!")
    else:
        await update.message.reply_text("📷 You can send a photo of your colored drawing!")

async def quiz_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quiz = random.choice(quiz_data)
    context.user_data["last_quiz"] = quiz  # store the current quiz

    keyboard = [
        [InlineKeyboardButton(opt, callback_data="correct" if opt == quiz["answer"] else "wrong")]
        for opt in quiz["options"]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=quiz["image"],
        caption=quiz["question"],
        reply_markup=reply_markup
    )
    await update.message.reply_text("Click the correct answer to move to the next question!")

# async def story_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton(story["title"], callback_data=f'story_{index}')]
#         for index, story in enumerate(story_data)
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("📚 Choose a story to listen to:", reply_markup=reply_markup)

async def story_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(story["title"], callback_data=f"story_{i}")] for i, story in enumerate(story_data)]
    await update.message.reply_text("📖 Choose a story to listen to:", reply_markup=InlineKeyboardMarkup(keyboard))

# # HANDLE story selection
# async def story_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     index = int(query.data.split("_")[1])
#     story = story_data[index]
#     if os.path.exists(story["file"]):
#         with open(story["file"], 'rb') as audio:
#             await query.message.reply_audio(audio=audio, caption=f"📘 {story['title']}", performer=story["performer"])
#     else:
#         await query.message.reply_text("❌ Sorry, that story is unavailable.")

async def story_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith('story_'):
        index = int(data.split('_')[1])
        if 0 <= index < len(story_data):
            story = story_data[index]
            file_path = story["file"]

            if os.path.exists(file_path):
                with open(file_path, 'rb') as audio_file:
                    await query.message.reply_audio(
                        audio=audio_file,
                        caption=f"📖 {story['title']}",
                        performer=story["performer"],
                        title=story["title"]
                    )
            else:
                await query.message.reply_text(f"❌ Sorry, the story '{story['title']}' is currently unavailable.")
        else:
            await query.message.reply_text("❌ Invalid story selection.")

async def animal_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Choose a random animal
    correct = random.choice(animal_data)
    correct_name = correct["name"]
    image_url = correct["image"]
    context.user_data["last_animal"] = correct

    # Create answer choices
    options = [correct_name]
    while len(options) < 3:
        other = random.choice(animal_data)["name"]
        if other not in options:
            options.append(other)
    random.shuffle(options)

    # Prepare buttons
    keyboard = [
        [InlineKeyboardButton(opt, callback_data="correct" if opt == correct_name else "wrong")]
        for opt in options
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send image and question
    await update.message.reply_photo(
        photo=image_url,
        caption="🐾 What animal is this?",
        reply_markup=reply_markup

    )



async def math_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    num1 = random.randint(1, 5)
    num2 = random.randint(1, 5)
    correct = num1 + num2

    # Save correct answer
    context.user_data["math_correct"] = correct

    # Generate choices
    choices = [correct]
    while len(choices) < 4:
        n = random.randint(2, 10)
        if n not in choices:
            choices.append(n)
    random.shuffle(choices)

    keyboard = [
        [InlineKeyboardButton(str(c), callback_data=f"math_{c}") for c in choices]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    question = f"🧮 What is {num1} + {num2}?"
    await update.message.reply_text(question, reply_markup=reply_markup)
    

# Define a callback function for the math game
# async def math_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     query.answer()
#     user_id = update.effective_user.id
#     correct = context.user_data["math_correct"]
#     answer = int(query.data.split("_")[1])
# animal_data = [
#     {
#         "name": "Dog",
#         "emoji": "🐶",
#         "image": "https://cdn.pixabay.com/photo/2017/01/31/20/16/dog-2029214_960_720.png"
#     },
#     {
#         "name": "Cat",
#         "emoji": "🐱",
#         "image": "https://cdn.pixabay.com/photo/2017/01/31/20/16/cat-2029213_960_720.png"
#     },
#     {
#         "name": "Cow",
#         "emoji": "🐮",
#         "image": "https://cdn.pixabay.com/photo/2013/07/13/13/40/cow-160041_960_720.png"
#     }
# ]


# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     if query.data == "correct":
#         await query.edit_message_text("✅ Correct! Great job!\n\nType /counting to play again.")
#     else:
#         await query.edit_message_text("❌ Not quite. Let's try again!\n\nType /counting to retry.")

# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     response = "✅ Correct!" if query.data == "correct" else "❌ Try again!"
#     await query.edit_message_text(f"{response}\n\n👋 Hello! Type /counting or /colors to play again.")

    
# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     user_id = query.from_user.id
#     await query.answer()

#     # Init score
#     if user_id not in user_scores:
#         user_scores[user_id] = {"correct": 0, "wrong": 0}

#     if query.data == "correct":
#         user_scores[user_id]["correct"] += 1
#         result = "✅ Correct!"

#         # Optional: play sound from animal game
#         animal = context.user_data.get("last_animal")
#         if animal and "sound" in animal:
#             await query.message.reply_audio(audio=animal["sound"], caption="🔊 Animal Sound!")

#     else:
#         user_scores[user_id]["wrong"] += 1
#         result = "❌ Try again!"

#     score = user_scores[user_id]
#     message = (
#         f"{result}\n\n"
#         f"🎯 Your Score:\n"
#         f"✅ {score['correct']} correct\n"
#         f"❌ {score['wrong']} wrong\n\n"
#         "👋 Type /counting, /colors, /animals or /quiz to play again."
#     )

#     await query.edit_message_text(message)

# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     user_id = query.from_user.id
#     await query.answer()
    
#     # 🎯 COUNTING GAME
#     if query.data == "counting":
#         await query.edit_message_text("🎲 Count the Apples\n\n"
#                                        "🔢 Type a number from 1 to 100")
#         context.user_data["last_counting"] = None
#         return None
    
#     # 🎯 QUIZ GAME
#     if query.data.startswith("quiz_"):
#         quiz_id = int(query.data.split("_")[1])
#         quiz = context.user_data.get("quizzes")[quiz_id]
#         await query.edit_message_text(quiz["question"], reply_markup=InlineKeyboardMarkup([quiz["buttons"]]))
#         context.user_data["last_quiz"] = quiz
#         return None
#     # 🎯 ANIMAL GAME
#     if query.data.startswith("animal_"):
#         animal_id = int(query.data.split("_")[1])
#         animal = context.user_data.get("animals")[animal_id]
#         await query.edit_message_text(animal["text"], reply_markup=InlineKeyboardMarkup([animal["buttons"]]))
#         context.user_data["last_animal"] = animal
#         return None
    
#     # Init score
#     if user_id not in user_scores:
#         user_scores[user_id] = {"correct": 0, "wrong": 0}
# # 🎯 COUNTING GAME
#     if query.data.startswith("count_"):
#         selected = int(query.data.split("_")[1])
#         correct = context.user_data.get("counting_correct")
#     # Init score if not already set
#     if user_id not in user_scores:
#         user_scores[user_id] = {"correct": 0, "wrong": 0}

#     # ✅ COUNTING GAME LOGIC
#     if query.data.startswith("count_"):
#         selected = int(query.data.split("_")[1])
#         correct = context.user_data.get("counting_correct")

#         if selected == correct:
#             user_scores[user_id]["correct"] += 1
#             await query.edit_message_text(f"✅ Yes! That’s {correct} fruits! 🥳\n🎉 Great job!")
#         else:
#             user_scores[user_id]["wrong"] += 1
#             await query.edit_message_text(f"❌ Oops! That’s not quite right.\nThere were {correct} fruits. 🍒 Try again!")

#         # Offer replay options
#         keyboard = [
#             [InlineKeyboardButton("🔁 Try Another", callback_data="counting")],
#             [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)

#         await query.message.reply_text("🎮 What would you like to do next?", reply_markup=reply_markup)
#         return

#     elif query.data == "counting":
#         await counting_game(update, context)
#         return

#     # 🧚 STORY GAME
#     elif query.data.startswith("story_"):
#         await story_selection(update, context)
#         return

#     # 🐾 DEFAULT GAME RESPONSE
#     if query.data == "correct":
#         user_scores[user_id]["correct"] += 1
#         result = "✅ Correct!"

#         # Optional: play sound from animal game
#         animal = context.user_data.get("last_animal")
#         if animal and "sound" in animal:
#             await query.message.reply_audio(audio=animal["sound"], caption="🔊 Animal Sound!")
#     else:
#         user_scores[user_id]["wrong"] += 1
#         result = "❌ Try again!"

#     score = user_scores[user_id]
#     message = (
#         f"{result}\n\n"
#         f"🎯 Your Score:\n"
#         f"✅ {score['correct']} correct\n"
#         f"❌ {score['wrong']} wrong\n\n"
#         "👋 Type /counting, /colors, /animals or /quiz to play again."
#     )

#     await query.edit_message_text(message)
# //////////////////////////////////////////////////////

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    data = query.data

    # Init score if not already set
    if user_id not in user_scores:
        user_scores[user_id] = {"correct": 0, "wrong": 0}

    # 🎯 COUNTING GAME LOGIC
    if data.startswith("count_"):
        selected = int(data.split("_")[1])
        correct = context.user_data.get("counting_correct")

        if selected == correct:
            user_scores[user_id]["correct"] += 1
            await query.edit_message_text(f"✅ Yes! That’s {correct} fruits! 🥳\n🎉 Great job!")
        else:
            user_scores[user_id]["wrong"] += 1
            await query.edit_message_text(f"❌ Oops! That’s not quite right.\nThere were {correct} fruits. 🍒 Try again!")
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 Play Again", callback_data="math")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ])
        await query.message.reply_text("🧮 Would you like to try another math question?", reply_markup=keyboard)
        return
    
        # keyboard = [
        #     [InlineKeyboardButton("🔁 Try Another", callback_data="counting")],
        #     [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        # ]
        # await query.message.reply_text("🎮 What would you like to do next?", reply_markup=InlineKeyboardMarkup(keyboard))
        # return

    elif data == "counting":
        await counting_game(update, context)
        return

    # 🧮 MATH GAME LOGIC
    if data.startswith("math_"):
        selected = int(data.split("_")[1])
        correct = context.user_data.get("math_correct")

        if selected == correct:
            user_scores[user_id]["correct"] += 1
            await query.edit_message_text(f"✅ Correct! {correct} is the right answer. 🧠")
        else:
            user_scores[user_id]["wrong"] += 1
            await query.edit_message_text(f"❌ Oops! The correct answer was {correct}.")

        keyboard = [
            [InlineKeyboardButton("🔁 Play Again", callback_data="math")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        await query.message.reply_text("🧮 Would you like to try another math question?", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif data == "math":
        await math_game(update, context)
        return

    # 📚 STORY SELECTION
    if data.startswith("story_"):
        await story_selection(update, context)
        return

    # 🐾 ANIMAL GAME - Correct/Wrong Answer
    if data in ["correct", "wrong"]:
        if data == "correct":
            user_scores[user_id]["correct"] += 1
            result = "✅ Correct!"

            animal = context.user_data.get("last_animal")
            if animal and "sound" in animal:
                await query.message.reply_audio(audio=animal["sound"], caption="🔊 Animal Sound!")
        else:
            user_scores[user_id]["wrong"] += 1
            result = "❌ Try again!"

        score = user_scores[user_id]
        message = (
            f"{result}\n\n"
            f"🎯 Your Score:\n"
            f"✅ {score['correct']} correct\n"
            f"❌ {score['wrong']} wrong\n\n"
            "👋 Type /counting, /colors, /animals, /quiz or /math to play again."
        )
        await query.edit_message_text(message)
        return


# ///////////////////////////////////////////////////
# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     user_id = query.from_user.id
#     await query.answer()

#     # Init score
#     if user_id not in user_scores:
#         user_scores[user_id] = {"correct": 0, "wrong": 0}

#     if query.data == "correct":
#         user_scores[user_id]["correct"] += 1
#         result = "✅ Correct!"

#         # Optional: play sound from animal game
#         animal = context.user_data.get("last_animal")
#         if animal and "sound" in animal:
#             await query.message.reply_audio(audio=animal["sound"], caption="🔊 Animal Sound!")
#     elif query.data.startswith("story_"):
#         await story_selection(update, context)
#         return
#     else:
#         user_scores[user_id]["wrong"] += 1
#         result = "❌ Try again!"

#     score = user_scores[user_id]
#     message = (
#         f"{result}\n\n"
#         f"🎯 Your Score:\n"
#         f"✅ {score['correct']} correct\n"
#         f"❌ {score['wrong']} wrong\n\n"
#         "👋 Type /counting, /colors, /animals or /quiz to play again."
#     )

#     await query.edit_message_text(message)

# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     response = "✅ Correct!" if query.data == "correct" else "❌ Try again!"
#     await query.edit_message_text(f"{response}\n\n👋 Hello! Type /counting, /colors or /animals to play again.")
# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     user_id = query.from_user.id

#     # Initialize score if not present
#     if user_id not in user_scores:
#         user_scores[user_id] = {"correct": 0, "wrong": 0}

#     # Update score
#     if query.data == "correct":
#         user_scores[user_id]["correct"] += 1
#         result = "✅ Correct!"

#         # Play sound if from animal game
#         animal = context.user_data.get("last_animal")
#         if animal and "sound" in animal:
#             await query.message.reply_audio(audio=animal["sound"], caption="🔊 What the animal says!")

#     else:
#         user_scores[user_id]["wrong"] += 1
#         result = "❌ Try again!"

#     score = user_scores[user_id]
#     message = (
#         f"{result}\n\n"
#         f"🎯 Your Score:\n"
#         f"✅ {score['correct']} correct\n"
#         f"❌ {score['wrong']} wrong\n\n"
#         "👋 Type /counting, /colors or /animals to play again."
#     )

#     await query.edit_message_text(message)

# Counting game command
# async def counting_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # Example image of apples
#     image_url = "https://cdn.pixabay.com/photo/2014/12/21/23/28/apple-575507_960_720.png"
#     apple_image = "🍎"

#     # Multiple choice buttons
#     keyboard = [
#         [InlineKeyboardButton("3", callback_data="wrong")],
#         [InlineKeyboardButton("5", callback_data="correct")],
#         [InlineKeyboardButton("7", callback_data="wrong")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     with open(image_url, "rb") as photo:
#         await update.message.reply_photo(
#             photo=image_url,
#             caption="🍎 How many apples do you see?",
#             reply_markup=reply_markup
#         )

# Button response handler
# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     if query.data == "correct":
#         await query.edit_message_caption(caption="✅ Correct! Great job!")
#     else:
#         await query.edit_message_caption(caption="❌ Oops! Try again!")
# # Define a message handler(responds to all text messages)
# async def handle_message(update: Update ,context:ContextTypes.DEFAULT_TYPE):
#     text= update.message_text
#     await update.message.reply_text(f"You Said:{text}")
# async def counting_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("3", callback_data='wrong')],
#         [InlineKeyboardButton("5", callback_data='correct')],
#         [InlineKeyboardButton("7", callback_data='wrong')],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_photo(
#         photo="https://example.com/apples.jpg",
#         caption="🍎 How many apples are there?",
#         reply_markup=reply_markup
#     )
# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     if query.data == 'correct':
#         await query.edit_message_caption(caption="✅ Correct! Well done!")
#     else:
#         await query.edit_message_caption(caption="❌ Oops! Try again.")

# async def story_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_audio(
#         audio=open("stories/goldilocks.mp3", "rb"),
#         caption="📖 Goldilocks and the Three Bears"
#     )
# async def draw_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_photo(
#         photo="https://example.com/coloring/cat.png",
#         caption="🎨 Can you color this cat? Use crayons or a coloring app!"
#     )

# transport_data = [
#     {"name": "Car", "image": "images/car.jpg", "moves_on": "Land"},
#     {"name": "Boat", "image": "images/boat.jpg", "moves_on": "Water"},
#     {"name": "Plane", "image": "images/plane.jpg", "moves_on": "Air"},
#     {"name": "Train", "image": "images/train.jpg", "moves_on": "Land"},
# ]

# current_question = {}  # To store user sessions

# async def transport_intro(update: Update, context: CallbackContext):
#     await update.message.reply_text(
#         "🚗 Welcome to the *Transportation Modes* lesson!\n\nLet's learn where different vehicles move: Land, Water, or Air.",
#         parse_mode='Markdown'
#     )
#     await send_transport_question(update.effective_chat.id, context)


# async def send_transport_question(chat_id, context: CallbackContext):
#     import random
#     vehicle = random.choice(transport_data)
#     current_question[chat_id] = vehicle

#     keyboard = InlineKeyboardMarkup([
#         [
#             InlineKeyboardButton("🌳 Land", callback_data="Land"),
#             InlineKeyboardButton("🌊 Water", callback_data="Water"),
#             InlineKeyboardButton("✈️ Air", callback_data="Air")
#         ]
#     ])

#     with open(vehicle['image'], 'rb') as img:
#         await context.bot.send_photo(
#             chat_id=chat_id,
#             photo=img,
#             caption=f"Where does this vehicle move?",
#             reply_markup=keyboard
#         )


# async def handle_transport_answer(update: Update, context: CallbackContext):
#     query = update.callback_query
#     await query.answer()

#     chat_id = query.message.chat.id
#     user_choice = query.data
#     correct = current_question.get(chat_id, {}).get("moves_on")
#     vehicle = current_question.get(chat_id, {}).get("name")

#     if user_choice == correct:
#         await query.edit_message_caption(
#             caption=f"✅ Correct! The {vehicle} moves on {correct}.",
#             reply_markup=None
#         )
#     else:
#         await query.edit_message_caption(
#             caption=f"❌ Oops! The {vehicle} actually moves on {correct}.",
#             reply_markup=None
#         )

#     # Wait a bit and send a new question
#     import asyncio
#     await asyncio.sleep(2)
#     await send_transport_question(chat_id, context)
# --- Sound-based activity data
transport_sounds = [
    {"answer": "Car", "sound": "car.mp3"},
    {"answer": "Plane", "sound": "plane.mp3"},
    {"answer": "Boat", "sound": "boat.mp3"},
    {"answer": "Train", "sound": "train.mp3"},
]

# --- Shadow-based activity data
transport_shadows = [
    {"answer": "Car", "shadow": "car_shadow.jpg"},
    {"answer": "Plane", "shadow": "plane_shadow.jpg"},
    {"answer": "Boat", "shadow": "boat_shadow.jpg"},
    {"answer": "Train", "shadow": "train_shadow.jpg"},
]

# Start sound quiz
def transport_sound_quiz(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🎧 Listen and guess the vehicle!")
    send_next_sound(update, context, 0)

def send_next_sound(update_or_callback, context: CallbackContext, index: int) -> None:
    if index >= len(transport_sounds):
        context.bot.send_message(chat_id=update_or_callback.effective_chat.id, text="👏 Well done! That was the sound quiz!")
        return

    sound_data = transport_sounds[index]
    sound_path = os.path.join(AUDIO_PATH, sound_data["sound"])

    keyboard = [[
        InlineKeyboardButton("🚗 Car", callback_data=f"sound_{index}_Car"),
        InlineKeyboardButton("🚂 Train", callback_data=f"sound_{index}_Train"),
        InlineKeyboardButton("✈️ Plane", callback_data=f"sound_{index}_Plane"),
        InlineKeyboardButton("🚢 Boat", callback_data=f"sound_{index}_Boat"),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_audio(chat_id=update_or_callback.effective_chat.id, audio=open(sound_path, 'rb'),
                           caption="What vehicle is this?", reply_markup=reply_markup)

def handle_sound_answer(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    _, index, guess = query.data.split("_")
    index = int(index)
    correct = transport_sounds[index]["answer"]

    if guess == correct:
        feedback = "✅ Correct!"
    else:
        feedback = f"❌ That's not right. It's a {correct}!"

    query.edit_message_caption(caption=feedback)
    send_next_sound(query, context, index + 1)

# Start shadow quiz
def transport_shadow_quiz(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🌑 Can you guess the vehicle from its shadow?")
    send_next_shadow(update, context, 0)

def send_next_shadow(update_or_callback, context: CallbackContext, index: int) -> None:
    if index >= len(transport_shadows):
        context.bot.send_message(chat_id=update_or_callback.effective_chat.id, text="🎉 Great job! That was the shadow quiz!")
        return

    data = transport_shadows[index]
    image_path = os.path.join(IMAGE_PATH, data["shadow"])

    keyboard = [[
        InlineKeyboardButton("🚗 Car", callback_data=f"shadow_{index}_Car"),
        InlineKeyboardButton("🚂 Train", callback_data=f"shadow_{index}_Train"),
        InlineKeyboardButton("✈️ Plane", callback_data=f"shadow_{index}_Plane"),
        InlineKeyboardButton("🚢 Boat", callback_data=f"shadow_{index}_Boat"),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_photo(chat_id=update_or_callback.effective_chat.id, photo=open(image_path, 'rb'),
                           caption="Which vehicle is this shadow?", reply_markup=reply_markup)

def handle_shadow_answer(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    _, index, guess = query.data.split("_")
    index = int(index)
    correct = transport_shadows[index]["answer"]

    if guess == correct:
        feedback = "✅ Correct!"
    else:
        feedback = f"❌ Nope. That was a {correct}!"

    query.edit_message_caption(caption=feedback)
    send_next_shadow(query, context, index + 1)



# Game state
HEALTHY_GAME, HEALTHY_ANSWER = range(2)

# Food dataset (you can expand this list)
food_items = [
    {"name": "Apple", "image": "images/apple.jpg", "audio": "audio/apple.mp3", "is_healthy": True},
    {"name": "Burger", "image": "images/burger.jpg", "audio": "audio/burger.mp3", "is_healthy": False},
    {"name": "Carrot", "image": "images/carrot.jpg", "audio": "audio/carrot.mp3", "is_healthy": True},
    {"name": "Fries", "image": "images/fries.jpg", "audio": "audio/fries.mp3", "is_healthy": False},
]

current_food_index = 0

def healthy_food_game(update, context):
    global current_food_index
    current_food_index = 0
    food = food_items[current_food_index]

    keyboard = [
        [InlineKeyboardButton("✅ Healthy", callback_data='healthy'),
         InlineKeyboardButton("❌ Unhealthy", callback_data='unhealthy')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(food["image"], "rb") as img, open(food["audio"], "rb") as aud:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=img)
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=aud)
        update.message.reply_text("Is this food Healthy or Unhealthy?", reply_markup=reply_markup)

    return HEALTHY_ANSWER

def handle_healthy_response(update, context):
    global current_food_index
    query = update.callback_query
    query.answer()

    food = food_items[current_food_index]
    correct = (query.data == 'healthy' and food["is_healthy"]) or (query.data == 'unhealthy' and not food["is_healthy"])

    if correct:
        query.edit_message_text("✅ Correct!")
    else:
        query.edit_message_text("❌ Oops! That's not right.")

    current_food_index += 1

    if current_food_index < len(food_items):
        next_food = food_items[current_food_index]
        keyboard = [
            [InlineKeyboardButton("✅ Healthy", callback_data='healthy'),
             InlineKeyboardButton("❌ Unhealthy", callback_data='unhealthy')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(next_food["image"], "rb") as img, open(next_food["audio"], "rb") as aud:
            context.bot.send_photo(chat_id=query.message.chat_id, photo=img)
            context.bot.send_audio(chat_id=query.message.chat_id, audio=aud)
            context.bot.send_message(chat_id=query.message.chat_id, text="Is this food Healthy or Unhealthy?", reply_markup=reply_markup)
        return HEALTHY_ANSWER
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text="🎉 Well done! You finished the game.")
        return ConversationHandler.END

# Add these to your conversation handler
healthy_food_handler = ConversationHandler(
    entry_points=[CommandHandler('healthy_food_game', healthy_food_game)],
    states={
        HEALTHY_ANSWER: [CallbackQueryHandler(handle_healthy_response)]
    },
    fallbacks=[]
)

###🎮 Game 2: “Put it in the Lunchbox or Trash Can”

# Game state
LUNCHBOX_GAME, LUNCHBOX_ANSWER = range(2)

# You can reuse this list or customize
food_items_lunchbox = [
    {"name": "Apple", "image": "images/apple.jpg", "audio": "audio/apple.mp3", "is_healthy": True},
    {"name": "Donut", "image": "images/donut.jpg", "audio": "audio/donut.mp3", "is_healthy": False},
    {"name": "Salad", "image": "images/salad.jpg", "audio": "audio/salad.mp3", "is_healthy": True},
    {"name": "Soda", "image": "images/soda.jpg", "audio": "audio/soda.mp3", "is_healthy": False},
]

current_lunchbox_index = 0

def lunchbox_game(update, context):
    global current_lunchbox_index
    current_lunchbox_index = 0
    food = food_items_lunchbox[current_lunchbox_index]

    keyboard = [
        [InlineKeyboardButton("🍱 Put in Lunchbox", callback_data='lunchbox'),
         InlineKeyboardButton("🗑️ Put in Trash Can", callback_data='trash')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(food["image"], "rb") as img, open(food["audio"], "rb") as aud:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=img)
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=aud)
        update.message.reply_text("Where should this food go?", reply_markup=reply_markup)

    return LUNCHBOX_ANSWER

def handle_lunchbox_response(update, context):
    global current_lunchbox_index
    query = update.callback_query
    query.answer()

    food = food_items_lunchbox[current_lunchbox_index]
    correct = (
        (query.data == 'lunchbox' and food["is_healthy"]) or
        (query.data == 'trash' and not food["is_healthy"])
    )

    if correct:
        query.edit_message_text("✅ Good job! That’s the right place.")
    else:
        query.edit_message_text("❌ Try again! That doesn’t belong there.")

    current_lunchbox_index += 1

    if current_lunchbox_index < len(food_items_lunchbox):
        next_food = food_items_lunchbox[current_lunchbox_index]
        keyboard = [
            [InlineKeyboardButton("🍱 Put in Lunchbox", callback_data='lunchbox'),
             InlineKeyboardButton("🗑️ Put in Trash Can", callback_data='trash')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        with open(next_food["image"], "rb") as img, open(next_food["audio"], "rb") as aud:
            context.bot.send_photo(chat_id=query.message.chat_id, photo=img)
            context.bot.send_audio(chat_id=query.message.chat_id, audio=aud)
            context.bot.send_message(chat_id=query.message.chat_id, text="Where should this food go?", reply_markup=reply_markup)
        return LUNCHBOX_ANSWER
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text="🎉 Excellent! You finished sorting the foods.")
        return ConversationHandler.END

# Add this to dispatcher
lunchbox_handler = ConversationHandler(
    entry_points=[CommandHandler('lunchbox_game', lunchbox_game)],
    states={
        LUNCHBOX_ANSWER: [CallbackQueryHandler(handle_lunchbox_response)]
    },
    fallbacks=[]
)

###🧲 Game 1: Find the Opposite
# @dp.message_handler(lambda message: message.text == "🧲 Opposites Game")
# async def start_opposites_game(message: types.Message):
#     await message.answer("Let's play the *Opposites Game*! 😊\n\nI'll show you a word or image, and you choose its opposite!", parse_mode="Markdown")
#     await send_opposite_question(message.chat.id)

# opposites = [
#     {"question": "Hot 🔥", "options": ["Cold ❄️", "Warm ☀️", "Boiling ♨️"], "answer": "Cold ❄️"},
#     {"question": "Big 🐘", "options": ["Small 🐜", "Heavy 🧱", "Loud 🔊"], "answer": "Small 🐜"},
#     {"question": "Fast 🏃", "options": ["Slow 🐢", "Busy 🚗", "Speedy 🚀"], "answer": "Slow 🐢"},
#     {"question": "Happy 😀", "options": ["Sad 😢", "Funny 😂", "Excited 🤩"], "answer": "Sad 😢"},
# ]

# user_opposite_index = {}

# async def send_opposite_question(chat_id):
#     index = random.randint(0, len(opposites) - 1)
#     user_opposite_index[chat_id] = index
#     q = opposites[index]
#     buttons = [KeyboardButton(option) for option in q["options"]]
#     markup = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
#     await bot.send_message(chat_id, f"What is the opposite of: *{q['question']}*?", parse_mode="Markdown", reply_markup=markup)

# @dp.message_handler(lambda message: message.chat.id in user_opposite_index)
# async def handle_opposite_answer(message: types.Message):
#     index = user_opposite_index[message.chat.id]
#     correct = opposites[index]["answer"]
#     if message.text == correct:
#         await message.answer("✅ Correct! Great job!")
#     else:
#         await message.answer(f"❌ Oops! The correct answer was: {correct}")
#     await send_opposite_question(message.chat.id)
# # Opposites questions
# opposites = [
#     {"question": "Hot 🔥", "options": ["Cold ❄️", "Warm ☀️", "Boiling ♨️"], "answer": "Cold ❄️"},
#     {"question": "Big 🐘", "options": ["Small 🐜", "Heavy 🧱", "Loud 🔊"], "answer": "Small 🐜"},
#     {"question": "Fast 🏃", "options": ["Slow 🐢", "Busy 🚗", "Speedy 🚀"], "answer": "Slow 🐢"},
#     {"question": "Happy 😀", "options": ["Sad 😢", "Funny 😂", "Excited 🤩"], "answer": "Sad 😢"},
#     {"question": "Day 🌞", "options": ["Night 🌙", "Morning 🌅", "Sunlight 🌤️"], "answer": "Night 🌙"},
#     {"question": "Up ⬆️", "options": ["Down ⬇️", "High 🏔️", "Above ☁️"], "answer": "Down ⬇️"},
#     {"question": "Full 🍽️", "options": ["Empty 🍵", "Tasty 😋", "Clean 🧽"], "answer": "Empty 🍵"},
# ]

# # Store current question per user
# user_opposite_index = {}

# # Start command
# @dp.message_handler(commands=["start"])
# async def start_game(message: types.Message):
#     markup = ReplyKeyboardMarkup(resize_keyboard=True)
#     markup.add(KeyboardButton("🧲 Opposites Game"))
#     await message.answer("👋 Hello! Welcome to the Educational Bot!\n\nChoose a game below to begin:", reply_markup=markup)

# # Start Opposites Game
# @dp.message_handler(lambda message: message.text == "🧲 Opposites Game")
# async def start_opposites_game(message: types.Message):
#     await message.answer("🎉 Let's play the *Opposites Game*! I will show you a word or emoji, and you choose its opposite.", parse_mode="Markdown")
#     await send_opposite_question(message.chat.id)

# # Send an opposite question
# async def send_opposite_question(chat_id):
#     index = random.randint(0, len(opposites) - 1)
#     user_opposite_index[chat_id] = index
#     q = opposites[index]
#     buttons = [KeyboardButton(option) for option in q["options"]]
#     markup = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
#     await bot.send_message(chat_id, f"❓ What is the *opposite* of: *{q['question']}*?", parse_mode="Markdown", reply_markup=markup)

# # Handle user's answer
# @dp.message_handler(lambda message: message.chat.id in user_opposite_index)
# async def handle_opposite_answer(message: types.Message):
#     index = user_opposite_index[message.chat.id]
#     correct = opposites[index]["answer"]
#     user_answer = message.text
#     is_correct = user_answer == correct

#     # Save result to database
#     save_result(
#         user_id=message.from_user.id,
#         question=opposites[index]["question"],
#         selected_answer=user_answer,
#         correct_answer=correct,
#         is_correct=is_correct
#     )

#     # Send response
#     if is_correct:
#         await message.answer("✅ Correct! You're awesome! 🎉")
#     else:
#         await message.answer(f"❌ Oops! The correct answer was: {correct}")
#     await send_opposite_question(message.chat.id)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CallbackContext, CommandHandler, MessageHandler, filters
import random

# List of opposites questions
opposites = [
    {"question": "Hot 🔥", "options": ["Cold ❄️", "Warm ☀️", "Boiling ♨️"], "answer": "Cold ❄️"},
    {"question": "Big 🐘", "options": ["Small 🐜", "Heavy 🧱", "Loud 🔊"], "answer": "Small 🐜"},
    {"question": "Fast 🏃", "options": ["Slow 🐢", "Busy 🚗", "Speedy 🚀"], "answer": "Slow 🐢"},
    {"question": "Happy 😀", "options": ["Sad 😢", "Funny 😂", "Excited 🤩"], "answer": "Sad 😢"},
    {"question": "Day 🌞", "options": ["Night 🌙", "Morning 🌅", "Sunlight ☀️"], "answer": "Night 🌙"},
    {"question": "Up ⬆️", "options": ["Down ⬇️", "High 🏔️", "Above ☁️"], "answer": "Down ⬇️"},
    {"question": "Full 🍽️", "options": ["Empty 🍵", "Tasty 😋", "Clean 🪝"], "answer": "Empty 🍵"},
]

# Track user question state
user_opposite_index = {}

# Command handler to start the opposites game
async def opposites_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    index = random.randint(0, len(opposites) - 1)
    user_opposite_index[user_id] = index
    question = opposites[index]

    buttons = [[KeyboardButton(option)] for option in question["options"]]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        f"🧲 What is the *opposite* of: *{question['question']}*?",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# Handler for user text response (answering opposites)
async def handle_opposites_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_opposite_index:
        return  # Skip if not in game

    index = user_opposite_index[user_id]
    correct = opposites[index]["answer"]
    user_answer = update.message.text

    if user_answer == correct:
        await update.message.reply_text("✅ Correct! Great job! 🎉")
    else:
        await update.message.reply_text(f"❌ Oops! The correct answer was: {correct}")

    # Ask another question
    await opposites_game(update, context)








#Main function to run the Bot
def main():
    app=Application.builder().token(TOKEN).build()
        # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("counting", counting_game))
    app.add_handler(CommandHandler("colors", color_game))
    app.add_handler(CommandHandler("animals", animal_game))
    app.add_handler(CommandHandler("quiz", quiz_game))
    app.add_handler(CommandHandler("storytime", story_time))
    app.add_handler(CommandHandler("math", math_game))
    # CallbackQuery Handler (for buttons)
    app.add_handler(CallbackQueryHandler(button_handler))

    # Message handler for user sending colored drawings
    app.add_handler(MessageHandler(filters.PHOTO, receive_coloring))
    # Add handlers to dispatcher
    app.add_handler(CommandHandler("transport", transport))
    app.add_handler(CallbackQueryHandler(handle_transport_answer, pattern=r"^move_\d+_"))
    app.add_handler(CommandHandler("transport_sound", transport_sound_quiz))
    app.add_handler(CommandHandler("transport_shadow", transport_shadow_quiz))
    app.add_handler(CallbackQueryHandler(handle_sound_answer, pattern=r"^sound_\d+_"))
    app.add_handler(CallbackQueryHandler(handle_shadow_answer, pattern=r"^shadow_\d+_"))
    app.add_handler(healthy_food_handler)
    app.add_handler(lunchbox_handler)
    app.add_handler(CommandHandler("opposites", opposites_game))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_opposites_answer))
    # app.add_handler(CommandHandler("transport", transport_intro))
    # app.add_handler(CallbackQueryHandler(handle_transport_answer))
    #Add  command and message handlers
    # app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler("counting", counting_game))
    # app.add_handler(CallbackQueryHandler(button_handler))
    # app.add_handler(CommandHandler("colors", color_game))
    # app.add_handler(CommandHandler("animals", animal_game))
    # app.add_handler(CommandHandler("quiz", quiz_game))
    # app.add_handler(CommandHandler("storytime", story_time))
    # app.add_handler(CallbackQueryHandler(story_selection, pattern='^story_'))
    # app.add_handler(CommandHandler("drawinggame", drawing_game))
    # app.add_handler(MessageHandler(filters.PHOTO, receive_coloring))
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))




    # Start Telegram Bot(Kinder Connect)
    print("🧸 KinderConnect Bot is running...")
    app.run_polling()



if __name__ == '__main__':
    main()

# Step4 :run your Bot
#save the script as bot.py and run it using python bot.py