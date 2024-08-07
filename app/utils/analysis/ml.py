import os
import logging
from openai import OpenAI
from typing import List


logger = logging.getLogger(__name__)


class ChatGPTApi:
    """Class that is used to call chatgpt, you need to have your openai API key as an environemnt variable named OPENAI_API_KEY"""

    def __init__(self) -> None:
        assert (
            os.getenv("OPENAI_API_KEY") is not None
        ), "No API key detected, please setup your API key as an environement variable under the name OPENAI_API_KEY"
        self.client = OpenAI()

    def call(self, *, message) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=message,
        )
        logger.debug(response)
        return str(response.choices[0].message.content)

    def identify_sensitive_files(self, files: List[dict]) -> str:
        """Identify sensitive files using GPT"""

        message = [
            {
                "role": "system",
                "content": (
                    f"You will be provided with a list of files paths"
                    "Your task is to identify which files are most likely to contain sensitive code,"
                    "base your expectations on the path of the file."
                    "understand that a main file is a file that is likely to contain the main logic of the application"
                    "those types of files are usually the most sensitive ones."
                    "remove all files which are irrelevent to the analysis"
                    "sort paths from most sensitive to least sensitive"
                    "Output is formatted as JSON with key sensitiveFiles containing a list of objects with keys:"
                    "path, which is the path of the file containing sensitive code"
                    "language, which is the programming language of the file"
                ),
            },
            {
                "role": "user",
                "content": "[{'path': 'cloned_repo/main.py', 'language': 'Python'}]",
            },
            {
                "role": "assistant",
                "content": '{ "sensitiveFiles": [ { "path": "cloned_repo/main.py", "language": "Python" } ] }',
            },
            {
                "role": "user",
                "content": str(files),
            },
        ]
        return self.call(message=message)

    def in_depth_analysis(
        self, code: str, language: str = "python", audit_type: str = "security"
    ) -> str:
        """Analyse code in depth using GPT"""
        if code is None or code == "":
            return ""
        if audit_type == "security":
            message = [
                {
                    "role": "system",
                    "content": (
                        f"You will be provided with a piece of {language} code"
                        "Your task is to check code security."
                        "If you find a possible security issue, you should provide a comment and a code suggestion to fix the issue (it must be code replacing existing one). "
                        "you should provide a comment and a code suggestion to fix the issue"
                        "Output is formatted as JSON with key 'issues' containing a list "
                        "each entry of the list corresponds to a different issue in the code"
                        "formatted as JSON objects with keys:"
                        f"language, which is always {language}"
                        "lineNumber, which is starting line where the issue occurs"
                        "initialCode, which is the code that is causing the issue ensure to include previous and next lines which are relevant"
                        "solvingCode, which is a possible solution to the issue in code"
                        "comment, which is a short description of the issue"
                        "suggestion, which is a description of a possible solution to the issue"
                    ),
                },
            ]
        else:
            message = [
                {
                    "role": "system",
                    "content": (
                        f"You will be provided with a piece of {language} code"
                        "Your task is to check code reliability."
                        "If you find an unhandeled error/exception," 
                        "you should provide a comment and a code suggestion to fix the issue"
                        "Output is formatted as JSON with key 'issues' containing a list "
                        "each entry of the list corresponds to a different issue in the code"
                        "formatted as JSON objects with keys:"
                        "lineNumber, which is starting line where the issue occurs"
                        "initialCode, which is the code that is causing the issue ensure to include previous and next lines which are relevant"
                        "solvingCode, which is a possible solution to the issue in code"
                        "comment, which is a short description of the issue"
                        "suggestion, which is a description of a possible solution to the issue"
                    ),
                },
            ]
        message.append(
            {
                "role": "user",
                "content": code,
            },
        )
        return self.call(message=message)
