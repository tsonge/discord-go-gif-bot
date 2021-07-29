from sgfmill import sgf
import os
import subprocess
import discord
from dotenv import load_dotenv

load_dotenv()

# note that this program requires the compiled sgf_to_gif binary executable 
# to be in project root
# from https://github.com/rooklift/sgf_to_gif

# bot commands:
# # :set sgf 

# # :play all moves

# # :play moves 15 to 20

# # :play from move 25, h5 h3 h6 j3

# todo:
# # :play h5 h3 h6 j3
# # ^ from blank goban

client = discord.Client()

@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))

# initial state for our global 'game' variable
with open("game.sgf", "rb") as f:
    game = sgf.Sgf_game.from_bytes(f.read())

@client.event
async def on_message(message):

  global game

  if message.author == client.user:
    return

  if len(message.attachments) > 0 and \
     message.attachments[0].filename.endswith('.sgf') and \
     message.content.startswith(':set sgf'):
    bytes = await message.attachments[0].read()
    game = sgf.Sgf_game.from_string(bytes.decode('utf-8'))
    await message.channel.send('sgf set!')

  if message.content.startswith(':play from move'):
    # note: from move 0 doesn't work
    board_size = game.get_size()
    msg = message.content.split(' ')
    stop_at_move_no = int(msg[3][:-1])

    unparsed_appended_moves = msg[4:]

    # unparsed_appended_moves looks like
    # unparsed_appended_moves = [
    #   'e8',
    #   'd7',
    #   'd8',
    # ]

    appended_moves = []

    # note: uses 'j' instead of 'i' for the x-axis column name

    for ind, x in enumerate(unparsed_appended_moves):
      xaxisnumber = ord(x[0])-97 if ord(x[0]) <= 104 else ord(x[0])-98 # the j instead of i thingy
      appended_moves.append(('b' if ((stop_at_move_no % 2)+ind) % 2 == 0 else 'w', (int(x[1:])-1,xaxisnumber)))

    # appended_moves should look like
    # appended_moves = [
    #   ('b', (0,0)),
    #   ('w', (1,0)),
    #   ('b', (2,0)), # note that first number represents y-axis, grows from bottom-left from 0,0
    # ]

    copied_game = sgf.Sgf_game(size=board_size)

    count = 0

    # now we copy moves up till given stop_at_move_no
    for node in game.get_main_sequence():
        if count > stop_at_move_no:
          break

        move = node.get_move()
        # print(count, move)
        # print(move[0], move[1])

        if count == 0:
          count = count + 1
          continue

        new_node = copied_game.extend_main_sequence()
        new_node.set_move(move[0], move[1])

        count = count + 1

    # now we copy over appended moves
    for move in appended_moves:
        new_node = copied_game.extend_main_sequence()
        new_node.set_move(move[0], move[1])

    # render to gif
    with open('output.sgf', "wb") as f:
        f.write(copied_game.serialise())
    subprocess.run(['./sgf_to_gif', '-d', '100', '-t', str(stop_at_move_no), 'output.sgf'])
    output_gif_filename = 'output.' + str(stop_at_move_no + len(appended_moves)) + '.gif'
    subprocess.run(['ffmpeg', '-i', output_gif_filename, '-movflags', 'faststart', '-pix_fmt', 'yuv420p', '-vf', "scale=trunc(iw/2)*2:trunc(ih/2)*2", 'output.mp4'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    await message.channel.send(file=discord.File('output.mp4'))
    subprocess.run('rm output*', shell=True)

  # do something like... :play from empty wb4 wb2 bb3 be19 
  if message.content.startswith(':play from empty'):
    game = sgf.Sgf_game(size=19)
    msg = message.content.split(' ')
    unparsed_appended_moves = msg[3:]

    # unparsed_appended_moves looks like
    # unparsed_appended_moves = [
    #   'we8',
    #   'wd7',
    #   'bd8',
    #   'bd18',
    # ]

    appended_moves = []

    # note: uses 'j' instead of 'i' for the x-axis column name
    for ind, x in enumerate(unparsed_appended_moves):
      xaxisnumber = ord(x[1])-97 if ord(x[1]) <= 104 else ord(x[1])-98 # the j instead of i thingy
      appended_moves.append((x[0], (int(x[2:])-1,xaxisnumber)))

    # now it looks like
    # appended_moves = [
    #     ('b', (0,0)),
    #     ('w', (1,0)),
    #     ('b', (2,0)), # note that first number represents y-axis, grows from bottom-left from 0,0
    #     ('b', (3,0)), # note that first number represents y-axis, grows from bottom-left from 0,0
    #     ('b', (1,1)), # note that first number represents y-axis, grows from bottom-left from 0,0
    # ]

    for move in appended_moves:
        new_node = game.extend_main_sequence()
        new_node.set_move(move[0], move[1])

    # render to gif
    with open('output.sgf', "wb") as f:
        f.write(game.serialise())
    subprocess.run(['./sgf_to_gif', '-d', '100', 'output.sgf'])
    subprocess.run(['ffmpeg', '-i', 'output.gif', '-movflags', 'faststart', '-pix_fmt', 'yuv420p', '-vf', "scale=trunc(iw/2)*2:trunc(ih/2)*2", 'output.mp4'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    await message.channel.send(file=discord.File('output.mp4'))
    subprocess.run('rm output*', shell=True)


  if message.content.startswith(':play all moves'):

    white_player = game.get_player_name('w')
    black_player = game.get_player_name('b')
    await message.channel.send('white is ' + white_player)
    await message.channel.send('black is ' + black_player)

    with open('output.sgf', "wb") as f:
        f.write(game.serialise())
    subprocess.run(['./sgf_to_gif', '-d', '100', 'output.sgf'])
    subprocess.run(['ffmpeg', '-i', 'output.gif', '-movflags', 'faststart', '-pix_fmt', 'yuv420p', '-vf', "scale=trunc(iw/2)*2:trunc(ih/2)*2", 'output.mp4'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    await message.channel.send(file=discord.File('output.mp4'))
    subprocess.run('rm output*', shell=True)

  if message.content.startswith(':play moves') and 'to' in message.content:
    msg = message.content.split(' ')
    starting_move = str(int(msg[2])-1)
    ending_move = msg[4]
    with open('output.sgf', "wb") as f:
        f.write(game.serialise())
    subprocess.run(f'./sgf_to_gif -d 100 -t "{starting_move} {ending_move}" output.sgf', shell=True)
    gif_filename = 'output.' + ending_move + '.gif'
    subprocess.run(['ffmpeg', '-i', gif_filename, '-movflags', 'faststart', '-pix_fmt', 'yuv420p', '-vf', "scale=trunc(iw/2)*2:trunc(ih/2)*2", 'output.mp4'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    await message.channel.send(file=discord.File('output.mp4'))
    subprocess.run('rm output*', shell=True)


client.run(os.getenv('DISCORD_BOT_TOKEN'))