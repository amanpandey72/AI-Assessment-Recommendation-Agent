"""
Prompt Builder for SHL AI Agent
"""

from typing import List, Dict


SYSTEM_PROMPT = """
You are an SHL Assessment Recommendation Assistant.

Your responsibilities are:

1. Recommend relevant SHL assessments.
2. Explain why they were chosen.
3. Compare assessments when asked.
4. Ask clarification questions if information is insufficient.
5. Never hallucinate.
6. Only answer using the provided assessment catalog.
7. If the answer is unavailable, politely say so.

Always be concise, professional and helpful.
"""


def format_assessments(results: List[Dict]) -> str:

    if not results:
        return "No assessments found."

    blocks = []

    for i, item in enumerate(results, start=1):

        block = f"""
Assessment {i}

Name: {item['name']}
Description: {item['description']}
Duration: {item['duration']}
Remote Testing: {item['remote']}
Adaptive: {item['adaptive']}
URL: {item['url']}
"""

        blocks.append(block)

    return "\n".join(blocks)


def build_prompt(
    query: str,
    retrieved_docs: List[Dict],
    conversation_history: List[Dict] | None = None,
):

    history = ""

    if conversation_history:

        for turn in conversation_history:

            role = turn.get("role", "user")

            content = turn.get("content", "")

            history += f"{role}: {content}\n"

    assessment_context = format_assessments(retrieved_docs)

    prompt = f"""
{SYSTEM_PROMPT}

Conversation History

{history}

User Query

{query}

Retrieved Assessments

{assessment_context}

Instructions

Answer ONLY using the retrieved assessments.

If multiple assessments satisfy the query,
recommend the best ones with reasons.

If clarification is required,
ask one short clarification question.

Never invent assessments.
"""

    return prompt


if __name__ == "__main__":

    docs = [
        {
            "name": "Java 8 (New)",
            "description": "Measures Java programming ability.",
            "duration": "18 minutes",
            "remote": "yes",
            "adaptive": "no",
            "url": "https://www.shl.com/"
        }
    ]

    prompt = build_prompt(
        "Need Java assessment",
        docs
    )

    print(prompt)