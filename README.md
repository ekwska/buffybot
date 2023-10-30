<h1 align="center">🦇 BuffyBot 🧛‍♀️</h1>

---

<div align="center"><img src="img/popcorn.gif"></div>

<div align="center"><i>"If the apocalypse comes, beep me"</i></div>

---

## 📖 Table of Contents

<details>
<summary><strong>Click to expand contents</strong></summary>

* [Functionality](#functionality)
* [How to run BuffyBot locally](#running-locally)
* [Support](#support)

</details>

------


## <a name="functionality"></a>🖥️ Functionality

`BuffyBot` uses slash commands, the available ones are

- `/buffy-save season episode`: Saves your progress in the current season. e.g `/buffy-save 1 1` to save that you are 
 watching or just finished `Season 1 Episode 1`. 
- `/buffy-progress`: Posts a progress bar with your status through finishing Buffy!
- `/buffy-next`: Posts the season, episode number and title of the next episode with a link to the Wikipedia page.
- `/buffy-current`: Posts the season, episode number and title of the last saved episode with a link to the Wikipedia 
 page.

## <a name="running-locally"></a>🏃 How to run BuffyBot locally

> The bot can also be run locally on a device, which requires Python and Poetry to be installed. BuffyBot will only be 
> online as long as the command is running, so if you turn your computer off or close the process, BuffyBot will go
> offline too! However, this method is good for testing and experimentation if you don't want to faff around with 
> Heroku 🦇

1. First, clone the repo using `git clone https://github.com/ekwska/buffybot`
2. Next install the dev dependencies:
* [Poetry](https://python-poetry.org/docs/#installation)
* [Python 3.9](https://www.python.org/downloads/release/python-390/)
2. Create a new [Discord Application](https://discordapp.com/developers/applications) in the `Discord Developer Portal`
* Name your app (e.g `SpikeForever`) click the **Create App** button
* Copy the apps **CLIENT ID** somewhere
* Scroll down to the **Bot** section
* Click the **Create a Bot User** button
* Click the **Yes, do it!** button
* Copy the bot's **TOKEN** somewhere
3. Rename the file `.env.example` to `.env`, and replace the value of `DISCORD_TOKEN` with the bots **TOKEN** you copied
 above.
4. Now invite the bot to any server where you have admin privileges using the below link, making sure to replace 
 **CLIENT_ID** with your client ID from above.

```
https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=2147552256&scope=bot
```

This will give the bot:

- `bot` scope
- `Read Messages`/`View Channels` permission
- `Send Messages` permission
- `Read Message History` permission
- `Use Slash Commands` permission

5. Open a terminal and navigate to the `buffybot` folder using `cd buffybot`
6. Run `poetry install`
7. Run `poetry run buffybot`, and you should see something like:

```bash
$ poetry run buffybot
WARNING:discord.state:Guilds intent seems to be disabled. This may cause state related issues.
WARNING:discord.client:PyNaCl is not installed, voice will NOT be supported
Master table exists, loading!
/home/bird/Documents/src/buffybot/buffybot/bot.py:17: RuntimeWarning: coroutine 'BotBase.add_cog' was never awaited
  bot.add_cog(BuffyBot(bot))
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
2023-10-30 15:55:42 INFO     discord.client logging in using static token
INFO:discord.client:logging in using static token
2023-10-30 15:55:43 INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: ddbd4a88030eb22572f161004e9f4e51).
INFO:discord.gateway:Shard ID None has connected to Gateway (Session ID: ddbd4a88030eb22572f161004e9f4e51).
BuffyBot#3743 has connected to Discord! Version 2.3.2
Master table exists, loading!
BuffyBot#3743 has loaded the BuffyBot extension!
Synced 4 commands.
```

5. You should have a working `BuffyBot`! Test it out by saving your progress using:
* `/buffy-save 1 1` to save that you are on the first episode.
* `/buffy-progress` to show how far you are through Buffy.
* `/buffy-next` to show you the title, season and episode number of the next episode (and a handy wikipedia link).

# <a name="support"></a>🏥 Support

If you run into any issues, please open a [Pull Request](https://github.com/ekwska/BuffyBot/pulls) 🐛