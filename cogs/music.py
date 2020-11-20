import discord
# import random
# import json
import asyncio
import youtube_dl
# import shutil
# import os
# from discord.utils import get
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, context):
        channel = context.author.voice.channel
        if context.voice_client is not None:
            return await context.voice_client.move_to(channel)

        await channel.connect()
        await context.send(f'Joined {channel}')
    # @commands.command()
    # async def join(self, context):
    #     global voice
    #     channel = context.message.author.voice.channel
    #     voice = get(self.client.voice_clients, guild=context.guild)
    #
    #     if voice and voice.is_connected():
    #         await voice.move_to(channel)
    #     else:
    #         voice = await channel.connect()
    #     await context.send(f'Joined {channel}')

    @commands.command()
    async def stop(self, context):
        await context.voice_client.disconnect()

    # @commands.command()
    # async def leave(self, context):
    #     global voice
    #     channel = context.message.author.voice.channel
    #     voice = get(self.client.voice_clients, guild=context.guild)
    #
    #     if voice and voice.is_connected():
    #         await voice.disconnect()
    #         await context.send(f'Left {channel}')

    @commands.command()
    async def play(self, context, *, query):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        context.voice_client.play(source, after=lambda e: print('Player error %s' % e) if e else None)

        await context.send(f'Now playing: {query}')

    # @commands.command(aliases=['p'])
    # async def play(self, context, url: str):
    #     global voice
    #
    #     def check_queue():
    #         Queue_infile = os.path.isdir("./Queue")
    #         if Queue_infile is True:
    #             DIR = os.path.abspath(os.path.realpath("Queue"))
    #             length = len(os.listdir(DIR))
    #             still_q = length - 1
    #             try:
    #                 first_file = os.listdir(DIR)[0]
    #             except:
    #                 print("No more queued song(s)\n")
    #                 queues.clear()
    #                 return
    #             main_location = os.path.dirname(os.path.realpath(__file__))
    #             song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
    #             if length != 0:
    #                 print("Song done, playing next queued\n")
    #                 print(f'Songs still in queue: {still_q}')
    #                 song_there = os.path.isfile("song.mp3")
    #                 if song_there:
    #                     os.remove("song.mp3")
    #                 shutil.move(song_path, main_location)
    #                 for file in os.listdir("./"):
    #                     if file.endswith(".mp3"):
    #                         os.rename(file, 'song.mp3')
    #
    #                 voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    #                 voice.source = discord.PCMVolumeTransformer(voice.source)
    #                 voice.source.volume = 0.07
    #
    #             else:
    #                 queues.clear()
    #                 return
    #
    #         else:
    #             queues.clear()
    #             print("No songs were queued before ending of the last song\n")
    #
    #     song_there = os.path.isfile("song.mp3")
    #     try:
    #         if song_there:
    #             os.remove("song.mp3")
    #             queues.clear()
    #             print("Removed old song file")
    #     except PermissionError:
    #         print("Trying to delete song file, but it's being played")
    #         await context.send("Error: Music Playing")
    #         return
    #
    #     Queue_infile = os.path.isdir("./Queue")
    #     try:
    #         Queue_folder = "./Queue"
    #         print("Removed old Queue folder")
    #
    #         if Queue_infile is True:
    #             print("Removed old Queue folder")
    #             shutil.rmtree(Queue_folder)
    #     except:
    #         print("No old Queue folder")
    #
    #     await context.send("Getting everything ready now")
    #
    #     voice = get(self.client.voice_clients, guild=context.guild)
    #
    #     ydl_opts = {
    #         'format': 'bestaudio/best',
    #         'quiet': True,
    #         'postprocessors': [{
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #             'preferredquality': '192'
    #         }],
    #     }
    #
    #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #         print("Downloading audio now\n")
    #         ydl.download([url])
    #
    #     for file in os.listdir("./"):
    #         if file.endswith(".mp3"):
    #             name = file
    #             print(f'Renamed file: {file}\n')
    #             os.rename(file, "song.mp3")
    #
    #     voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    #     voice.source = discord.PCMVolumeTransformer(voice.source)
    #     voice.source.volume = 0.07
    #
    #     nname = name.rsplit("-", 2)
    #     await context.send(f"Playing: {nname[0]}")
    #     print("playing\n")

    # @commands.command()
    # async def pause(self, context):
    #     global voice
    #     voice = get(self.client.voice_clients, guild=context.guild)
    #
    #     if voice and voice.is_playing():
    #         print("Music paused")
    #         voice.pause()
    #         await context.send("Music paused")
    #     else:
    #         print("Music not playing, failed to pause")
    #         await context.send("Music not playing, failed to pause")

    @commands.command()
    async def yt(self, context, *, url):
        async with context.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop)
            context.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await context.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, context, *, url):
        async with context.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            context.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await context.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, context, volume: int):
        if context.voice_client is None:
            return await context.send("Not connected to a voice channel.")

        context.voice_client.source.volume = volume / 100
        await context.send(f'Changed volume to {volume}')

    # @commands.command()
    # async def resume(self, context):
    #     global voice
    #     voice = get(self.client.voice_clients, guild=context.guild)
    #
    #     if voice and voice.is_paused():
    #         print("Resuming music")
    #         voice.resume()
    #         await context.send("Resumed music")
    #     else:
    #         print("Music is not paused")
    #         await context.send("Music is not paused")
    #
    # @commands.command()
    # async def skip(self, context):
    #     global voice
    #     voice = get(self.client.voice_clients, guild=context.guild)
    #
    #     queues.clear()
    #
    #     if voice and voice.is_playing():
    #         print("Music skipped")
    #         voice.stop()
    #         await context.send("Music skipped")
    #     else:
    #         print("No music playing, failed to skip")
    #         await context.send("No music playing, failed to skip")
    #
    # @commands.command()
    # async def queue(self, context, url:str):
    #     Queue_infile = os.path.isdir("./Queue")
    #     if Queue_infile is False:
    #         os.mkdir("Queue")
    #     DIR = os.path.abspath(os.path.realpath("Queue"))
    #     q_num = len(os.listdir(DIR))
    #     q_num += 1
    #     add_queue = True
    #     while add_queue:
    #         if q_num in queues:
    #             q_num += 1
    #         else:
    #             add_queue = False
    #             queues[q_num] = q_num
    #
    #     queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")
    #
    #     ydl_opts = {
    #         'format': 'bestaudio/best',
    #         'quiet': True,
    #         'outtmpl': queue_path,
    #         'postprocessors': [{
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #             'preferredquality': '192',
    #         }]
    #     }
    #
    #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #         print("Downloading audio now\n")
    #         ydl.download([url])
    #     await context.send("Adding song " + str(q_num) + " to the queue")
    #
    #     print("Song added to the queue\n")


def setup(client):
    client.add_cog(Music(client))
