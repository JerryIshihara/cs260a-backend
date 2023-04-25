# Project Name

A brief description of your project.

## Prerequisites

-   Python 3.8x
-   Pip

## Getting Started

These instructions will get you up and running with a local development environment.

### 1. Create a Python virtual environment

It's recommended to create a virtual environment to isolate project dependencies. To create a virtual environment, follow these steps:

```bash
python3 -m venv venv
```

Activate the virtual environment:

-   On macOS and Linux:

```bash
source venv/bin/activate
```

-   On Windows:

```bash
.\venv\Scripts\activate
```

### 2. Install dependencies

With the virtual environment activated, install the project dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root directory with the necessary environment variables. Use the provided `.env.template` file as a template, and replace the placeholders with your actual values.

### 4. Create empty sqlite database file

```bash
mkdir database && touch database/database.db
```

### 5. Run the Flask app

To run the Flask app, execute the following command:

```bash
python app.py
```

The app should now be running at http://localhost:8000 by default.
