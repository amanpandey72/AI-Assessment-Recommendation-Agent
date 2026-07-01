"""
Clarification Logic for SHL AI Agent
"""

from typing import Optional
import re


class ClarificationEngine:

    def __init__(self):

        self.roles = [
            "developer",
            "engineer",
            "manager",
            "analyst",
            "sales",
            "marketing",
            "finance",
            "intern",
            "graduate",
            "executive",
            "consultant",
            "hr",
            "support",
            "qa",
            "tester",
            "scientist"
        ]

    def needs_clarification(self, query: str) -> bool:

        query = query.lower()

        # Very short queries
        if len(query.split()) <= 3:
            return True

        # Generic requests
        generic_patterns = [
            "recommend assessment",
            "recommend test",
            "best assessment",
            "best test",
            "assessment",
            "test",
            "recommend",
            "hire someone",
            "need assessment",
            "suggest assessment",
        ]

        for pattern in generic_patterns:
            if pattern == query:
                return True

        # No role mentioned
        role_found = any(role in query for role in self.roles)

        if not role_found:
            return True

        return False

    def clarification_question(self, query: str) -> Optional[str]:

        query = query.lower()

        if len(query.split()) <= 3:
            return (
                "Could you tell me the target job role "
                "or the primary skills you want to assess?"
            )

        if not any(role in query for role in self.roles):
            return (
                "Which job role or skills are you hiring for? "
                "For example: Java Developer, Data Analyst, "
                "Graduate Engineer, Sales Executive, etc."
            )

        return None


if __name__ == "__main__":

    engine = ClarificationEngine()

    while True:

        q = input("\nQuery : ")

        if q.lower() == "exit":
            break

        print("Needs Clarification :", engine.needs_clarification(q))
        print("Question :", engine.clarification_question(q))