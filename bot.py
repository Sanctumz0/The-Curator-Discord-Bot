import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# ── Config ──────────────────────────────────────────────────────────────────
load_dotenv()
TOKEN = os.environ.get("TOKEN")

ROLE_SP = 1474399644820963489
ROLE_EG = 1474400779443110010
ROLE_WW = 1474400504191910042
ROLE_TH = 1474400856664313939
ROLE_UNSORTED = 1475964643515039906

QUESTIONS = [
    {
        "title": "Question 1 of 10",
        "question": "Which Xentrico moment feels most like you right now?",
        "a": "Sitting alone, really taking in *are you okay?* — thinking about your life",
        "b": "Feeling fired up listening to *Objection* — like you need to go do something bigger",
        "c": "Playing *bow chi wa wa* on a drive, just enjoying the moment",
        "d": "Listening to *miss neighbour* and thinking about someone specific",
        "weight": 8
    },
    {
        "title": "Question 2 of 10",
        "question": "Which of my songs do you connect with the most right now?",
        "a": "are you okay?",
        "b": "Objection",
        "c": "bow chi wa wa",
        "d": "miss neighbour",
        "weight": 8
    },
    {
        "title": "Question 3 of 10",
        "question": "When you replay my music, it's usually because…",
        "a": "I'm trying to understand something deeper",
        "b": "It makes me want to create or chase something",
        "c": "It just feels good in the moment",
        "d": "It reminds me of someone or something personal",
        "weight": 4
    },
    {
        "title": "Question 4 of 10",
        "question": "What hits you the hardest in my music?",
        "a": "The meaning behind the lyrics",
        "b": "The energy and drive",
        "c": "The vibe and atmosphere",
        "d": "The emotions tied to love and connection",
        "weight": 4
    },
    {
        "title": "Question 5 of 10",
        "question": "Be honest — what do you do after listening to one of my songs?",
        "a": "Sit and think for a while",
        "b": "Feel motivated to do something",
        "c": "Just keep the vibe going",
        "d": "Think about someone or a moment",
        "weight": 4
    },
    {
        "title": "Question 6 of 10",
        "question": "If one of my songs played during a key moment in your life, what would it be?",
        "a": "A moment of self-reflection",
        "b": "A turning point — chasing something bigger",
        "c": "A carefree memory with friends",
        "d": "A moment involving someone you care about",
        "weight": 4
    },
    {
        "title": "Question 7 of 10",
        "question": "What kind of listener are you when it comes to my music?",
        "a": "I listen closely to understand everything",
        "b": "I connect with the energy and expression",
        "c": "I just enjoy how it feels",
        "d": "I attach it to people and emotions",
        "weight": 4
    },
    {
        "title": "Question 8 of 10",
        "question": "Which line would hit you the hardest?",
        "a": "A line that makes you question your life",
        "b": "A line that pushes you to go harder",
        "c": "A line that just sounds good and feels right",
        "d": "A line about love or missing someone",
        "weight": 4
    },
    {
        "title": "Question 9 of 10",
        "question": "When you think about my music, what stands out most?",
        "a": "The depth",
        "b": "The ambition",
        "c": "The vibe",
        "d": "The romance",
        "weight": 4
    },
    {
        "title": "Question 10 of 10 — Final Question",
        "question": "Which space in Xentrico's Playground feels like home to you?",
        "a": "Quiet streets where you can think",
        "b": "Loud, expressive, creative spaces",
        "c": "Calm streets where nothing is rushed",
        "d": "Soft, emotional places tied to memories",
        "weight": 4
    },
]

RESULTS = {
    "sp": {
        "title": "Sandra Park.",
        "description": "The quiet heart of Xentrico's Playground was always yours.\n\nYou're one of the deep thinkers — the kind of person who sits with difficult thoughts instead of running from them. You hear emotions in music that others miss. You read between the lines. You're not afraid of the long conversations.\n\n*Real strength is being able to feel everything and still show up.*",
        "color": 0x7289DA,
        "footer": "Sandra Park • Xentrico's Playground",
        "role_id": ROLE_SP
    },
    "eg": {
        "title": "Ember Grove.",
        "description": "You belong on the louder side of Xentrico's Playground.\n\nYou don't just feel things — you turn them into something. A song. A design. A new way of doing things. You challenge what doesn't make sense and build your own lane.\n\n*Why follow the path when you could build your own?*",
        "color": 0xE84545,
        "footer": "Ember Grove • Xentrico's Playground",
        "role_id": ROLE_EG
    },
    "ww": {
        "title": "Willow Way.",
        "description": "The slowest part of Xentrico's Playground is yours.\n\nYou don't need everything to mean something. You know how to just be there — present, easy, real. Music plays, the moment is good, and that's enough. You're grounded in a way most people have to work for.\n\n*Sometimes it's enough to just be here.*",
        "color": 0x57F287,
        "footer": "Willow Way • Xentrico's Playground",
        "role_id": ROLE_WW
    },
    "th": {
        "title": "Thandora.",
        "description": "The most romantic part of Xentrico's Playground has been waiting for you.\n\nYou replay lyrics the way you replay conversations. You attach songs to people. You hold onto moments longer than most — not because you can't let go, but because some things deserve to be kept.\n\n*Love isn't something you move on from easily. It's something you carry.*",
        "color": 0xEB459E,
        "footer": "Thandora • Xentrico's Playground",
        "role_id": ROLE_TH
    }
}

# ── State ────────────────────────────────────────────────────────────────────
# quiz_state[user_id] = {"q": int, "sp": int, "eg": int, "ww": int, "th": int}
quiz_state: dict[int, dict] = {}

# ── Bot setup ────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ── Helpers ──────────────────────────────────────────────────────────────────
def build_question_embed(q_index: int) -> discord.Embed:
    q = QUESTIONS[q_index]
    embed = discord.Embed(
        title=q["title"],
        color=0x5865F2
    )
    embed.add_field(
        name=q["question"],
        value=f"🅐  {q['a']}\n🅑  {q['b']}\n🅒  {q['c']}\n🅓  {q['d']}",
        inline=False
    )
    footer = "Type A, B, C, or D"
    if q_index == 8:
        footer += " • One more after this"
    if q_index == 9:
        footer += " • This is your last answer"
    embed.set_footer(text=footer)
    return embed

def build_answer_buttons(q_index: int) -> discord.ui.View:
    view = AnswerView(q_index)
    return view

def determine_winner(scores: dict) -> str:
    winner = "sp"
    top = scores["sp"]
    for district in ["eg", "ww", "th"]:
        if scores[district] > top:
            winner = district
            top = scores[district]
    return winner

# ── Answer View (buttons) ────────────────────────────────────────────────────
class AnswerView(discord.ui.View):
    def __init__(self, q_index: int):
        super().__init__(timeout=300)
        self.q_index = q_index

    async def handle_answer(self, interaction: discord.Interaction, answer: str):
    await interaction.response.defer(ephemeral=True)
    
    user_id = interaction.user.id

    if user_id not in quiz_state:
        await interaction.followup.send(
            "Your session expired. Run `/sort` to start again.",
            ephemeral=True
        )
        return

    state = quiz_state[user_id]

    if state["q"] != self.q_index:
        await interaction.followup.send(
            "Please answer the current question.",
            ephemeral=True
        )
        return

    q = QUESTIONS[self.q_index]
    weight = q["weight"]

    state[answer] += weight
    state["q"] += 1

    for item in self.children:
        item.disabled = True
    await interaction.message.edit(view=self)

    if state["q"] >= len(QUESTIONS):
        winner = determine_winner(state)
        result = RESULTS[winner]

        embed = discord.Embed(
            title=result["title"],
            description=f"Welcome home, {interaction.user.mention}.\n\n{result['description']}",
            color=result["color"]
        )
        embed.set_footer(text=result["footer"])

        guild = interaction.guild
        role = guild.get_role(result["role_id"])
        unsorted_role = guild.get_role(ROLE_UNSORTED)

        if role:
            await interaction.user.add_roles(role)
        if unsorted_role:
            await interaction.user.remove_roles(unsorted_role)

        del quiz_state[user_id]

        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        next_q_index = state["q"]
        embed = build_question_embed(next_q_index)
        view = build_answer_buttons(next_q_index)
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="A", style=discord.ButtonStyle.secondary)
    async def button_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_answer(interaction, "sp")

    @discord.ui.button(label="B", style=discord.ButtonStyle.secondary)
    async def button_b(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_answer(interaction, "eg")

    @discord.ui.button(label="C", style=discord.ButtonStyle.secondary)
    async def button_c(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_answer(interaction, "ww")

    @discord.ui.button(label="D", style=discord.ButtonStyle.secondary)
    async def button_d(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_answer(interaction, "th")

# ── Slash commands ───────────────────────────────────────────────────────────
@bot.tree.command(name="sort", description="Begin your sorting into Xentrico's Playground.")
async def sort(interaction: discord.Interaction):
    user_id = interaction.user.id

    quiz_state[user_id] = {"q": 0, "sp": 0, "eg": 0, "ww": 0, "th": 0}

    embed = discord.Embed(
        title="Welcome to Xentrico's Playground.",
        description="This place has four districts. Each one has its own energy, its own kind of people, its own way of moving through the world.\n\nAnswer honestly. There are no wrong answers — only the ones that are true for you.\n\n*Ten questions. One district. Yours.*",
        color=0x2b2d31
    )
    embed.set_footer(text="Only you can see this")

    await interaction.response.send_message(embed=embed, ephemeral=True)

    q_embed = build_question_embed(0)
    view = build_answer_buttons(0)
    await interaction.followup.send(embed=q_embed, view=view, ephemeral=True)


@bot.tree.command(name="sortreset", description="Reset a user's sorting session and roles. Admin only.")
@app_commands.checks.has_permissions(manage_roles=True)
async def sortreset(interaction: discord.Interaction, user: discord.Member):
    if user.id in quiz_state:
        del quiz_state[user.id]

    guild = interaction.guild
    for role_id in [ROLE_SP, ROLE_EG, ROLE_WW, ROLE_TH]:
        role = guild.get_role(role_id)
        if role and role in user.roles:
            await user.remove_roles(role)

    unsorted_role = guild.get_role(ROLE_UNSORTED)
    if unsorted_role:
        await user.add_roles(unsorted_role)

    await interaction.response.send_message(
        f"Session and roles reset for {user.mention}. They can retake the quiz.",
        ephemeral=True
    )

# ── Events ───────────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} — slash commands synced.")

# ── Run ──────────────────────────────────────────────────────────────────────
bot.run(TOKEN)
