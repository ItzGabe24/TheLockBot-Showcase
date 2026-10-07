# TheLockBot (Showcase)

An AI-powered sports analytics Discord bot built with Python, SQLite, and LLM integration.

This repository is a public overview of the project: what it does, how it is put together, and a few small generic code samples. The production source code is private.

> For informational and educational purposes only. Nothing here is financial or betting advice.

## What it does

- Analyzes sports data and posts structured, probability-based insights to Discord through slash commands.
- Covers multiple sports and market types, combining statistics, schedules, news, injuries, player availability, recent performance, and market data.
- Uses large language models to turn unstructured text (news, injury reports) into validated, structured data before any analysis runs.
- Stores every prediction, then grades it against the real outcome so model performance can be measured over time.
- Includes admin diagnostics that show where the model is strong or weak, so scoring rules can be improved with evidence.

## Architecture

```
Discord slash commands / scheduled tasks
              |
              v
   Data collection (stats, schedules, news, injuries, market data)
              |
              v
   LLM preprocessing: unstructured text -> validated JSON
              |
              v
   Analysis and scoring (probability, expected value, historical performance)
              |
              v
   Post to Discord  +  store in SQLite
              |
              v
   Grading and performance tracking (results -> calibration reports)
```

### Design notes

- **Async throughout.** discord.py and aiosqlite keep commands responsive while data is fetched in the background.
- **Structured output first.** LLM responses are parsed and validated as JSON before downstream code touches them, with retries on malformed output.
- **Measure, don't guess.** Predictions and outcomes are stored together so calibration (predicted probability vs. actual hit rate) can be checked and used to refine the scoring rules.
- **Operational basics.** Deployed to a cloud host with auto-deploy from GitHub, a persistent volume for the database, and failure alerts sent to a private Discord channel.

## Tech stack

Python, discord.py, SQLite (aiosqlite), LLM APIs, public sports data APIs, Git and GitHub, cloud deployment.

## Code samples

Small, generic examples of patterns used in the project. They contain no production logic, prompts, or data.

| File | What it shows |
| --- | --- |
| [`samples/slash_command_example.py`](samples/slash_command_example.py) | An async discord.py slash command that defers, reads from SQLite, and replies with an embed |
| [`samples/schema_example.sql`](samples/schema_example.sql) | A predictions table and a calibration query comparing predicted probability to actual hit rate |
| [`samples/structured_output_example.py`](samples/structured_output_example.py) | Validating LLM output as structured JSON, with retries on bad output |

## What is not here

The scoring logic, prompts, data pipelines, and tuning are kept private. I'm happy to walk through the real code in an interview or on a screen share.

## Author

Gabriel Vasquez, San Antonio, TX. GitHub: [@ItzGabe24](https://github.com/ItzGabe24)
