## 💬 Personal Chatbot

Personal Chatbot using [LangChain](https://python.langchain.com/docs/introduction/) + [Ollama](https://ollama.com/download) + [Streamlit](https://docs.streamlit.io/).

> ⚠️ WIP

<img src="https://i.imgur.com/JeKhNgh.gif" width=500/>


## ✅ Requirements

Make sure you have [Ollama](https://ollama.com/download) installed on your machine.

## 🔨 Setting up locally

Create virtualenv and install dependencies

```sh
make setup
```

## ⚡️ Running the application

```sh
make run
```

## ✨ Linters and Formatters

Check for linting rule violations:

```sh
make check
```

Auto-fix linting violations:

```sh
make fix
```

## Configurations

Apart from `session_data`, the app uses `chat_config.json` file to maintain state between refreshes.


## Debugging

**VSCode**

Go to Run and Debug Section and press `Chat App Debug` on top right section.

**Others**

`breakpoint()`  FTW!

## 🤸‍♀️ Getting Help

```sh
make

# OR

make help
```
