"""The rule catalogue. Rule identifiers are stable: reports, events, waivers and lessons refer to them.

Advice text lives here, in the tool, and nowhere else. Lessons fed back to an agent are assembled from
this table and from counts, never from text found in a repository, so that repository content cannot
inject instructions through the learning loop.
"""
from __future__ import annotations

# id: (level, title, advice, waivable)
RULES: dict[str, tuple[str, str, str, bool]] = {
    "IWOS-G001": ("error", "Protected artefact changed without a proposal citation",
                  "Do not edit a protected artefact unless a maintainer directed it under an accepted proposal; cite that proposal in the pull request.", False),
    "IWOS-G002": ("error", "Protected artefact changed without regenerating the lock",
                  "When a protected artefact changes under an accepted proposal, run `iwos lock` in the same change.", False),
    "IWOS-G003": ("error", "Architecture changed without a decision-record citation",
                  "Before changing an architecture path, find or write the decision record that authorises it and cite it in the pull request.", True),
    "IWOS-G004": ("error", "No authority citation",
                  "State in the pull request description which work package, decision, proposal or issue authorises the change.", True),
    "IWOS-G005": ("error", "Control file changed without a proposal citation",
                  "The constitution file, the waiver register and the validator configuration define the rules; change them only under an accepted proposal.", False),
    "IWOS-W001": ("warning", "Lock changed although no protected artefact did",
                  "Regenerate the lock only when a protected artefact changed.", False),
    "IWOS-W002": ("warning", "Every commit is attributed to an agent",
                  "A human must review and merge.", False),
    "IWOS-W003": ("warning", "Agent attribution rests on disclosure alone",
                  "Commit under an agent identity or add a co-author trailer so that attribution is recorded in history.", False),
    "IWOS-W004": ("note", "No agent disclosed",
                  "If an agent worked on the change, disclose it.", False),
    "IWOS-W005": ("warning", "No valid constitution on the base revision",
                  "The base revision holds no valid constitution, so the change was judged against the constitution in the working tree. Review the constitution file by hand.", False),
    "IWOS-W006": ("warning", "Waiver ignored",
                  "A waiver needs an identifier, a waivable rule, paths, an owner, a reason and an expiry date that has not passed.", False),
    "IWOS-W007": ("warning", "The automation that runs the gate changed",
                  "A result produced by a changed gate is not independent. Review the workflow or tool change by hand.", False),
    "IWOS-V001": ("error", "Integrity violation",
                  "A protected artefact and the lock disagree. Do not regenerate the lock to make the check pass; report it.", False),
    "IWOS-V002": ("error", "Credential pattern in content",
                  "Remove the value, rotate the credential and open an incident; never copy the value into a report.", False),
    "IWOS-V003": ("warning", "Other validation finding",
                  "Run `iwos validate` and resolve each finding.", False),
}


def level(rule: str) -> str:
    return RULES[rule][0]


def title(rule: str) -> str:
    return RULES[rule][1]


def advice(rule: str) -> str:
    return RULES[rule][2]


def waivable(rule: str) -> bool:
    return rule in RULES and RULES[rule][3]
