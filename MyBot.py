
# import discord
# from discord.ext import commands
# import sqlite3

# TOKEN = "YOUR_BOT_TOKEN"

# intents = discord.Intents.default()
# intents.members = True
# bot = commands.Bot(command_prefix='!', intents=intents)

# @bot.event
# async def on_ready():
#     await bot.tree.sync()
#     print(f"Bot is ready as {bot.user}")

# @bot.tree.command(name="view_inventory")
# async def view_inventory(interaction: discord.Interaction):
#     # Check the user's roles
#     user_roles = [role.name for role in interaction.user.roles]

#     # Connect to SQLite database
#     conn = sqlite3.connect("game_data.db")
#     cursor = conn.cursor()

#     # Check if there is an inventory for the user based on role
#     inventory = {}

#     for role in user_roles:
#         cursor.execute("SELECT item, quantity FROM inventory WHERE team = ?", (role,))
#         rows = cursor.fetchall()

#         if rows:
#             inventory[role] = {row[0]: row[1] for row in rows}

#     conn.close()

#     if inventory:
#         # Create the embed to display inventory
#         embed = discord.Embed(
#             title="Your Inventory",
#             description="Here are the items you own:",
#             color=discord.Color.gold()
#         )
#         embed.set_thumbnail(url="https://i.imgur.com/Ok6Y9nB.jpeg")
#         embed.set_author(
#             name="Game Bot",
#             url="https://i.imgur.com/Ok6Y9nB.jpeg",
#             icon_url="https://i.imgur.com/Ok6Y9nB.jpeg"
#         )
#         embed.set_image(url="https://i.imgur.com/Ok6Y9nB.jpeg")
#         embed.set_footer(
#             text="Inventory Last Updated: Jan 18, 2025",
#             icon_url="https://i.imgur.com/Ok6Y9nB.jpeg"
#         )
#         embed.timestamp = discord.utils.utcnow()

#         # Add the inventory items to the embed
#         for role, items in inventory.items():
#             embed.add_field(name=f"{role}'s Inventory", value="\n".join([f"{item}: {quantity}" for item, quantity in items.items()]), inline=False)

#         await interaction.response.send_message(embed=embed)
#     else:
#         await interaction.response.send_message("You don't have an inventory assigned.")

# bot.run(TOKEN)
import discord
from discord.ext import commands
import sqlite3

TOKEN = ""

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is ready as {bot.user}")

# Command to view inventory (same as before)
@bot.tree.command(name="view_inventory")
async def view_inventory(interaction: discord.Interaction):
    user_roles = [role.name for role in interaction.user.roles]

    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    inventory = {}
    for role in user_roles:
        cursor.execute("SELECT item, quantity FROM inventory WHERE team = ?", (role,))
        rows = cursor.fetchall()

        if rows:
            inventory[role] = {row[0]: row[1] for row in rows}

    conn.close()

    if inventory:
        embed = discord.Embed(
            title="Your Inventory",
            description="Here are the items you own:",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url="https://i.imgur.com/Ok6Y9nB.jpeg")
        embed.set_author(
            name="Game Bot",
            url="https://i.imgur.com/Ok6Y9nB.jpeg",
            icon_url="https://i.imgur.com/Ok6Y9nB.jpeg"
        )
        embed.set_image(url="https://i.imgur.com/Ok6Y9nB.jpeg")
        embed.set_footer(
            text="Inventory Last Updated: Jan 18, 2025",
            icon_url="https://i.imgur.com/Ok6Y9nB.jpeg"
        )
        embed.timestamp = discord.utils.utcnow()

        for role, items in inventory.items():
            embed.add_field(name=f"{role}'s Inventory", value="\n".join([f"{item}: {quantity}" for item, quantity in items.items()]), inline=False)

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("You don't have an inventory assigned.")


# Command to update inventory
@bot.tree.command(name="update_inventory")
async def update_inventory(interaction: discord.Interaction, team: str, item: str, new_quantity: int):
    """Update an inventory item for a given team."""
    # Check if user has the role (team) before allowing update
    user_roles = [role.name for role in interaction.user.roles]
    if team not in user_roles:
        await interaction.response.send_message(f"You don't have the '{team}' role, so you cannot update this inventory.")
        return

    # Connect to SQLite database
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    # Check if the item exists in the inventory for the specified team
    cursor.execute("SELECT * FROM inventory WHERE team = ? AND item = ?", (team, item))
    result = cursor.fetchone()

    if result:
        # Update the inventory
        cursor.execute("UPDATE inventory SET quantity = ? WHERE team = ? AND item = ?", (new_quantity, team, item))
        conn.commit()

        await interaction.response.send_message(f"Inventory updated: {item} for team '{team}' is now {new_quantity}.")
    else:
        await interaction.response.send_message(f"Item '{item}' not found in the inventory for team '{team}'.")

    conn.close()


bot.run(TOKEN)

# example - add comment made an example comment here, which will change file code for example - ok