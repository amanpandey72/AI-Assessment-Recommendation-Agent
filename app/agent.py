"""
Main SHL AI Agent
"""

from app.retriever import Retriever
from app.clarification import ClarificationEngine
from app.comparison import ComparisonEngine
from app.guardrails import Guardrails


class SHLAgent:

    def __init__(self):

        self.retriever = Retriever()
        self.guardrails = Guardrails()
        self.clarifier = ClarificationEngine()
        self.comparison = ComparisonEngine()

    def recommend(self, query: str):

        # ----------------------------------
        # 1. Guardrails
        # ----------------------------------
        allowed, message = self.guardrails.check(query)

        if not allowed:
            return {
                "status": "refused",
                "response": message
            }

        lower = query.lower()

        # ----------------------------------
        # 2. Comparison Queries
        # ----------------------------------
        if (
            "compare" in lower
            or "difference" in lower
            or " vs " in lower
        ):

            results = self.retriever.search(query)

            if len(results) < 2:
                return {
                    "status": "not_found",
                    "response": "I couldn't find enough assessments to compare."
                }

            comparison = self.comparison.compare(results[:2])

            return {
                "status": "comparison",
                "response": comparison,
                "results": results[:2]
            }

        # ----------------------------------
        # 3. Clarification
        # ----------------------------------
        if self.clarifier.needs_clarification(query):

            return {
                "status": "clarification",
                "response": self.clarifier.clarification_question(query)
            }

        # ----------------------------------
        # 4. Retrieve Assessments
        # ----------------------------------
        results = self.retriever.search(query)

        if not results:
            return {
                "status": "not_found",
                "response": "No matching SHL assessments found."
            }

        # ----------------------------------
        # 5. Recommendation Response
        # ----------------------------------
        answer = []

        answer.append("Recommended SHL Assessments\n")

        for i, item in enumerate(results[:5], start=1):

            answer.append(
                f"""
{i}. {item['name']}

Duration : {item.get('duration', 'N/A')}
Remote : {item.get('remote', 'N/A')}
Adaptive : {item.get('adaptive', 'N/A')}

Description:
{item.get('description', 'No description available.')}

URL:
{item.get('url', 'N/A')}
"""
            )

        return {
            "status": "success",
            "response": "\n".join(answer),
            "results": results[:5]
        }


if __name__ == "__main__":

    agent = SHLAgent()

    print("=" * 60)
    print("SHL AI Assessment Agent")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        query = input("\nYou: ")

        if query.lower() == "exit":
            break

        response = agent.recommend(query)

        print("\nAssistant:\n")
        print(response["response"])