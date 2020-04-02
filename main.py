import discord
TOKEN = 'MzQ0NDE5Mjk5MjczNzM2MTky.XoHxWQ._O_TGgUnt4lX4fCxWojGmcWiZSw'
CODE_C_ID = 693841407730778123
GUILD = 627089852080586752
client = discord.Client()


def code_language(msg: str):
    py_snippets = ["import", " #  ", "# ", '"""', "def ", "@", "len(", "len (", " in ", ".join(", ".join (",
                   "print(", "print ("]
    c_snippets = ["#include", "//", "///", "/*", "*/", "&", "|", "~", "for(", "for (", "while (", "while(", ";",
                  "scanf(", "scanf (", "printf(", "pritntf (", "unsigned", ".h>", '.h"', '.c"', "){", ") {",
                  "int main()", "&&", "||"]
    c_occ = sum([snippet in msg for snippet in c_snippets])
    py_occ = sum([snippet in msg for snippet in py_snippets])
    if py_occ + c_occ == 0:
        return None
    elif c_occ > py_occ:
        return "c"
    return "py"


def format_as_code(msg, language) -> str:
    formatted_str = f"**Scritto da:** __{msg.author.name}{msg.author.discriminator}__\n**Linguaggio:** __{language}__\n"
    if "```" not in msg.content:
        formatted_str += "```" + language + "\n" + msg.content + "\n```"
    else:
        formatted_str += msg.content
    formatted_str += "\n" + "+"*50
    return formatted_str


async def message_writer(msg: str):
    print("Imma send:", msg)
    code_channel = client.get_channel(CODE_C_ID)
    print(code_channel)
    await code_channel.send(msg)


async def delete_message(msg):
    try:
        await msg.delete()
    except discord.Forbidden:
        print("Insufficient permissions!")
    except discord.NotFound:
        print("Message was not found!")
    except discord.HTTPException:
        print("Failed to delete message!")


@client.event
async def on_ready():
    for guild in client.guilds:
        print(guild)
    print(f"Bot {client.user} has connected to Discord's server")


@client.event
async def on_message(message):
    print("Got a message!", "Message:\n", message.content, "\n channel:", message.channel, "\n code_channel:")
    if message.channel.id == CODE_C_ID and not message.author.bot:
        print(message.content)
        print("received message in code channel")
        code_lang = code_language(message.content)
        print("The code language is:", code_lang)
        if code_lang:
            print("I'm going to write the message!")
            await message_writer(format_as_code(message, code_lang))
        await delete_message(message)


client.run(TOKEN)
# f = open("test.txt", "r")
# message = f.readlines()
# print(code_language(str(message)))
