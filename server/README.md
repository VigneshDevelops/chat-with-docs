# App

This project is a FastAPI application.

## Table of Contents

- [Installation](#installation)
  - [Installing Poetry CLI](#installing-poetry-cli)
    - [Linux and macOS](#linux-and-macos)
    - [Windows (WSL)](#windows-wsl)
    - [Windows (Powershell)](#windows-powershell)
  - [Installing Dependencies](#installing-dependencies)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)

## Installation

### Installing Poetry CLI

To manage your project dependencies and environments, you'll need to install Poetry CLI. Follow the instructions based on your operating system:

#### Linux and macOS

Use the following command to install Poetry CLI:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Note: On some systems, `python` may still refer to Python 2 instead of Python 3. We always suggest using the `python3` binary to avoid ambiguity.

#### Windows (WSL)

In the Windows Subsystem for Linux (WSL), you can install Poetry using the same command as in Linux:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

#### Windows (Powershell)

Use the following command to install Poetry CLI using Powershell:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### Installing Dependencies

After installing Poetry, navigate to the project directory and install the dependencies using the following command:

```sh
poetry install
```

This will install all dependencies specified in the `pyproject.toml` file.

## Environment Variables

This project uses environment variables for configuration. You need to create a `.env` file inside the `server/` directory and specify the necessary environment variables as shown in the provided `.env.example` file.

- **OpenAI API Key**: Set the `OPENAI_API_KEY` environment variable in your `.env` file to access GPT and Ada embedding models.
- **Pinecone API Key and Index**: Set the `PINECONE_API_KEY` and `PINECONE_INDEX` environment variables in your `.env` file to connect to Pinecone as the vector database.

## Running the Project

To run the project, first make sure you are inside the project directory. Then, use the following command to run the application:

```sh
poetry run dev
```

This will execute the FastAPI application using Uvicorn as the server.

## API Documentation

You can access the FastAPI Swagger documentation at `http://localhost:8000/docs` once the server is running. This documentation provides an overview of the available endpoints, request and response formats, and other details about your FastAPI application.

---
