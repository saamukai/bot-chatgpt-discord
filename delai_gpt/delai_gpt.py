#!/usr/bin/python3

import discord
import openai
import time
import json

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

token = 'TOKEN_BOT_DISCORD'
openai.api_key = 'TOKEN_API_OPENAI'
models = openai.Model.list()
channel_id_discord = 'CHANNEL_RESPONSE_ID'
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print(f"bot conectado como {client.user}")


@client.event
async def on_message(message):
  channel_id_response = str(message.channel.id)
  user_message = str(message.content)

  if message.author.bot:
    return

  if channel_id_response == channel_id_discord:

    # Ignora a interação do bot
    if message.content.startswith('/'):
      return

    try:
      thinking_message = await message.channel.send("Pensando...🤔")

      response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {
          "role": "system",
          "content": "Você é um bot que responde perguntas e seu nome é Gênio da Lâmpada \
            e deve iniciar todas suas resposta com e se apresentar com o seu nome."
        },
        {
          "role": "assistant",
          "content": user_message
        }])

      # Remove a mensagem "pensando..."
      await thinking_message.delete()

      # pega a resposta
      answer = response['choices'][0]['message']['content']

      embed = discord.Embed(
        description=
        f"** <:bear:1105288251264213073> | PERGUNTA :**\n {message.content}\n\n**<a:robot:1105288917932060794> | DELAI RESPONDE :**\n {answer}",
        color=discord.Color.default())
      # embed.set_author(
      #   name='DELAS ARTIFICAL INTELIGENCE',
      #   icon_url=
      #   'https://cdn.discordapp.com/attachments/1091197321989083247/1106040160245776434/image.jpg'
      # )
      embed.set_image(
        url=
        'https://cdn.discordapp.com/attachments/1106216030373695518/1106216137580097577/delas_gpt.png'
      )

      await message.channel.send(embed=embed)
    except Exception as e:
      print(f"Ocorreu um erro na chamada da API: {e}")
      await thinking_message.delete()  # Remove a mensagem "pensando..."
      await message.channel.send(f"Ocorreu um erro na chamada da API: {e}")
      time.sleep(5)  # Espera 10 segundos
      await on_message(message)  # Tenta novamente


client.run(token)
