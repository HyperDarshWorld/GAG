import discord
from discord import app_commands
from discord.ext import commands

TOKEN = "MTM3Nzk2OTk4NjY4MDkxODEyOQ.Gqzj9n.URkNQXZ7by_h4EyDe5HdPre2EwgBgbZjv34yvE"

# Replace these with actual Discord user IDs of your middlemen
MIDDLEMEN_IDS = [
    1209149201628536843,  # Middleman 1
    938317122998796298,   # Middleman 2
]

# Define fruit base values
FRUIT_VALUES = {
    "carrot": 10,
    "strawberry": 50,
    "blueberry": 400,
    "orange tulip": 600,
    "tomato": 800,
    "corn": 1300,
    "daffodil": 1000,
    "watermelon": 2500,
    "pumpkin": 3000,
    "apple": 3250,
    "bamboo": 4000,
    "coconut": 6000,
    "cactus": 15000,
    "dragon fruit": 50000,
    "mango": 100000,
    "grape": 850000,
    "mushroom": 150000,
    "pepper": 1000000,
    "cacao": 2500000,
    "beanstalk": 10000000,
}

# Define mutant multipliers
MUTANT_MULTIPLIERS = {
    "wet": 2,
    "chilled": 2,
    "chocolate": 2,
    "moonlit": 2,
    "bloodlit": 4,
    "plasma": 5,
    "frozen": 10,
    "golden": 20,
    "zombified": 25,
    "twisted": 30,
    "rainbow": 50,
    "shocked": 100,
    "celestial": 120,
    "disco": 125,
}

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # Needed for fetching users
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Register commands globally
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.tree.command(name="mm", description="Send a message to middlemen with a reason")
@app_commands.describe(reason="Reason for contacting middlemen")
async def mm(interaction: discord.Interaction, reason: str):
    sender = interaction.user
    failed = []

    for mid in MIDDLEMEN_IDS:
        try:
            user = await bot.fetch_user(mid)
        except discord.NotFound:
            failed.append(f"User ID {mid} not found")
            continue
        except Exception as e:
            failed.append(f"Error fetching user {mid}: {e}")
            continue

        try:
            await user.send(f"**Middleman Request**\nFrom: {sender} ({sender.id})\nReason: {reason}")
        except Exception as e:
            failed.append(f"Failed to DM {user}: {e}")

    if failed:
        await interaction.response.send_message(
            "Some issues occurred while notifying middlemen:\n" + "\n".join(failed), ephemeral=True
        )
    else:
        await interaction.response.send_message("Middlemen have been notified!", ephemeral=True)


@bot.tree.command(name="value", description="Calculate the value of a fruit with mutant multiplier")
@app_commands.describe(fruit="Type of fruit", mutant="Type of mutant multiplier")
async def value(interaction: discord.Interaction, fruit: str, mutant: str):
    fruit_lower = fruit.lower()
    mutant_lower = mutant.lower()

    if fruit_lower not in FRUIT_VALUES:
        await interaction.response.send_message(f"Unknown fruit '{fruit}'. Available fruits: {', '.join(FRUIT_VALUES.keys())}", ephemeral=True)
        return

    if mutant_lower not in MUTANT_MULTIPLIERS:
        await interaction.response.send_message(f"Unknown mutant '{mutant}'. Available mutants: {', '.join(MUTANT_MULTIPLIERS.keys())}", ephemeral=True)
        return

    base_value = FRUIT_VALUES[fruit_lower]
    multiplier = MUTANT_MULTIPLIERS[mutant_lower]
    total_value = base_value * multiplier

    await interaction.response.send_message(
        f"Fruit: **{fruit}**\nBase Value: {base_value}\nMutant Multiplier: {multiplier}\n\n**Total Value: {total_value}**"
    )

bot.run(TOKEN)
