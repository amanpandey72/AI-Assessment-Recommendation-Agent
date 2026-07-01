"""
Comparison Engine for SHL AI Agent
"""

from typing import Dict, List


class ComparisonEngine:

    def compare(self, assessments: List[Dict]) -> str:

        if len(assessments) < 2:
            return "At least two assessments are required for comparison."

        lines = []

        header = (
            f"{'Feature':<20}"
            + "".join(f"{a['name'][:25]:<30}" for a in assessments)
        )

        lines.append(header)
        lines.append("-" * len(header))

        def row(title, key):
            value = f"{title:<20}"
            for assessment in assessments:
                value += f"{str(assessment.get(key, 'N/A'))[:25]:<30}"
            lines.append(value)

        row("Duration", "duration")
        row("Remote", "remote")
        row("Adaptive", "adaptive")
        row("Job Levels", "job_levels")
        row("Languages", "languages")
        row("Categories", "categories")

        lines.append("\nDescriptions\n")

        for assessment in assessments:
            lines.append(f"• {assessment['name']}")
            lines.append(assessment["description"])
            lines.append("")

        return "\n".join(lines)


if __name__ == "__main__":

    engine = ComparisonEngine()

    assessment1 = {
        "name": "Java 8 (New)",
        "duration": "18 minutes",
        "remote": "yes",
        "adaptive": "no",
        "job_levels": ["Graduate"],
        "languages": ["English"],
        "categories": ["Programming"],
        "description": "Measures Java programming skills."
    }

    assessment2 = {
        "name": "Core Java",
        "duration": "13 minutes",
        "remote": "yes",
        "adaptive": "no",
        "job_levels": ["Professional"],
        "languages": ["English"],
        "categories": ["Programming"],
        "description": "Measures Core Java knowledge."
    }

    print(engine.compare([assessment1, assessment2]))