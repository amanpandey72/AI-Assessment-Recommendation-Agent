"""
Guardrails for SHL AI Agent
Restricts the assistant to SHL assessment related queries.
"""

from typing import Tuple


class Guardrails:

    def __init__(self):

        self.allowed_keywords = [
            "assessment",
            "test",
            "exam",
            "hire",
            "hiring",
            "candidate",
            "developer",
            "engineer",
            "analyst",
            "manager",
            "graduate",
            "intern",
            "sales",
            "finance",
            "python",
            "java",
            "javascript",
            "sql",
            "excel",
            "aws",
            "cloud",
            "leadership",
            "personality",
            "aptitude",
            "cognitive",
            "behavior",
            "skill",
            "assessment recommendation",
            "compare"
        ]

    def is_in_scope(self, query: str) -> bool:

        query = query.lower()

        return any(keyword in query for keyword in self.allowed_keywords)

    def check(self, query: str) -> Tuple[bool, str]:

        if self.is_in_scope(query):
            return True, ""

        return (
            False,
            (
                "I'm designed to answer questions only about SHL assessments "
                "and assessment recommendations. Please ask about hiring, "
                "skills, assessments, comparisons, or candidate evaluation."
            )
        )


if __name__ == "__main__":

    guard = Guardrails()

    while True:

        query = input("\nQuery: ")

        if query.lower() == "exit":
            break

        allowed, message = guard.check(query)

        print("Allowed:", allowed)

        if not allowed:
            print("Response:", message)