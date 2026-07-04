# Learning Notes

## Step 1 - One-Shot Chat

Folder:

```text
Project1-Chat
```

What it teaches:

- Load an API key from `.env`
- Send one prompt to Gemini
- Print one answer

## Step 2 - Chat Loop With Memory

Folder:

```text
Project1-Chat-V2
```

What it teaches:

- A chatbot is a loop
- Memory is a list of previous messages
- Context is what you send to the model
- Temperature changes how creative/random the answer feels
- Max output tokens controls answer length

## Experiments

Try the same prompt with different temperatures:

```text
/temp 0.1
Write 3 startup ideas for AI learning apps.
```

```text
/temp 1.0
Write 3 startup ideas for AI learning apps.
```

Notice whether the second answer feels more varied or creative.
