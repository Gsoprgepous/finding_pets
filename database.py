{
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "# database.py\n",
        "import sqlite3\n",
        "\n",
        "def create_connection():\n",
        "    conn = sqlite3.connect('pets.db')\n",
        "    return conn\n",
        "\n",
        "def create_table():\n",
        "    conn = create_connection()\n",
        "    c = conn.cursor()\n",
        "    c.execute('''CREATE TABLE IF NOT EXISTS pets\n",
        "                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, photo_path TEXT, breed TEXT)''')\n",
        "    conn.commit()\n",
        "    conn.close()\n",
        "\n",
        "def add_pet_to_db(user_id, photo_path, breed):\n",
        "    conn = create_connection()\n",
        "    c = conn.cursor()\n",
        "    c.execute(\"INSERT INTO pets (user_id, photo_path, breed) VALUES (?, ?, ?)\", (user_id, photo_path, breed))\n",
        "    conn.commit()\n",
        "    conn.close()\n",
        "\n",
        "def get_pets_from_db(user_id):\n",
        "    conn = create_connection()\n",
        "    c = conn.cursor()\n",
        "    c.execute(\"SELECT * FROM pets WHERE user_id=?\", (user_id,))\n",
        "    rows = c.fetchall()\n",
        "    conn.close()\n",
        "    return rows\n"
      ],
      "metadata": {
        "id": "HS1BvlzEwY9o"
      },
      "execution_count": 30,
      "outputs": []
    }
  ],
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}
