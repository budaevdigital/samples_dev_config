import os
from typing import Any
import logging

import openai
import requests

logging.getLogger(__name__)

# Инициализация API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Получение информации о Pull Request
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("GITHUB_REF").split('/')[2]
TOKEN = os.getenv("GITHUB_TOKEN")


def get_review(comments: str) -> list[Any]:
    """Функция для запроса ревью у ChatGPT."""
    get_response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Review the following code:\n{comments}\nProvide feedback and suggestions for improvement.",
        max_tokens=200
    )
    return get_response.choices[0].text.strip()


def get_files_with_changes_from_pull_request() -> dict[dict | str, Any]:
    """Запрос изменений в Pull Request."""
    get_response = requests.get(
        f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files",
        headers={"Authorization": f"token {TOKEN}"}
    )
    return get_response.json()


def analyze_code_and_send_in_openai_reviewer(files: dict[dict | str, Any]) -> None:
    """Анализ изменений и отправка их в ChatGPT."""

    for file in files:
        review = get_review(file.get("patch"))

        # Создание комментария в Pull Request
        review_comment = f"**File: {file.get('filename')}**\n\n{review}"
        requests.post(
            f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments",
            headers={"Authorization": f"token {TOKEN}"},
            json={"body": review_comment}
        )


def main():
    logging.info("Запуск запроса запроса ревью")
    get_files_for_review = get_files_with_changes_from_pull_request()
    analyze_code_and_send_in_openai_reviewer(get_files_for_review)
    logging.info("Завершение ревью")


if __name__ == "__main__":
    main()
