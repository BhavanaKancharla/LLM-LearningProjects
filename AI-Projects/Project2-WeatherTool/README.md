# Project 2 - Weather Tool Calling

This project teaches tool calling: the model decides when it needs a function, Python runs that function, then the model turns the tool result into a final answer.

## Setup

```powershell
py -m pip install -r requirements.txt
```

Create `.env`:

```env
GEMINI_API_KEY=your_gemini_key_here
```

## Run

```powershell
py weather_tool.py
```

Try:

```text
What is the weather in Bangalore?
```

## Concept

Flow:

```text
User question -> Gemini requests get_weather(city) -> Python runs tool -> Gemini writes final answer
```
