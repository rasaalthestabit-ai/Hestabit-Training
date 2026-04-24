import json
import random
import os

# REPRODUCIBILITY
random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(BASE_DIR, exist_ok=True)

raw_path = os.path.join(BASE_DIR, "raw_data.jsonl")

data = []

# ---------------------------
# QA DATA
# ---------------------------

policies = {
    "leave": "rules governing employee time off including sick leave and vacation",
    "attendance": "guidelines for employee presence and punctuality",
    "payroll": "process of calculating and distributing employee salaries",
    "recruitment": "process of hiring new employees",
    "performance review": "evaluation of employee performance over time",
    "termination": "procedures followed when ending employment",
    "promotion": "process of advancing employees to higher roles",
    "grievance": "mechanism for handling employee complaints"
}

qa_styles = [
    "Explain in simple terms",
    "Provide a professional HR explanation"
]

qa_input_templates = [
    "What is the {policy} policy in a company?",
    "Explain the {policy} policy.",
    "Define the {policy} policy in HR.",
    "What does the {policy} policy mean?",
    "How does the {policy} policy work?"
]

qa_output_templates = [
    "In HR, the {policy} policy refers to {definition}.",
    "The {policy} policy is defined as {definition}."
]

for _ in range(450):
    policy = random.choice(list(policies.keys()))
    data.append({
        "instruction": random.choice(qa_styles),
        "input": random.choice(qa_input_templates).format(policy=policy),
        "output": random.choice(qa_output_templates).format(
            policy=policy,
            definition=policies[policy]
        )
    })


# ---------------------------
# REASONING DATA (FIXED LOGIC)
# ---------------------------

def decide_action(n):
    if n <= 1:
        return "take no action"
    elif n <= 3:
        return "provide counseling"
    elif n <= 6:
        return "issue a warning"
    elif n <= 8:
        return "conduct a formal review"
    else:
        return "initiate disciplinary action"

scenarios = [
    "An employee has been late {n} times this month.",
    "An employee missed deadlines {n} times.",
    "An employee showed poor performance in {n} tasks.",
    "An employee violated company policy {n} times."
]

reasoning_styles = [
    "Analyze the situation and provide a decision with reasoning",
    "Act as an HR manager and suggest action",
    "Evaluate the scenario and recommend next steps"
]

reasoning_outputs = [
    "HR should {action} because repeated issues affect productivity and workplace standards. Further steps may be needed if the behavior continues.",
    "Based on the frequency of the issue, HR should {action}. Continued behavior may require stricter measures.",
]

for _ in range(450):
    n = random.randint(0, 12)  # includes edge cases
    scenario = random.choice(scenarios).format(n=n)
    action = decide_action(n)

    data.append({
        "instruction": random.choice(reasoning_styles),
        "input": f"{scenario} What should HR do?",
        "output": random.choice(reasoning_outputs).format(action=action)
    })


# ---------------------------
# EXTRACTION DATA (IMPROVED)
# ---------------------------

names = ["Amit", "Sara", "John", "Priya", "Rahul", "Neha", "Arjun"]
roles = ["Software Engineer", "HR Manager", "Data Analyst", "Product Manager"]
companies = ["TCS", "Google", "Infosys", "Amazon", "Wipro"]
years = [1, 2, 3, 5, 7, 10]

templates = [
    "{name} worked as a {role} at {company} for {years} years.",
    "{name} has been employed at {company} as a {role} for {years} years.",
    "{name}, a {role}, worked at {company} for {years} years.",
    "{name}, who worked at {company}, served as a {role} for {years} years.",
    "For {years} years, {name} was employed at {company} as a {role}.",
    "{company} employed {name} as a {role} for a duration of {years} years.",
    "{name} worked at {company} for {years} years as a {role} in the organization."
]

for _ in range(450):
    name = random.choice(names)
    role = random.choice(roles)
    company = random.choice(companies)
    yr = random.choice(years)

    text = random.choice(templates).format(
        name=name,
        role=role,
        company=company,
        years=yr
    )

    data.append({
        "instruction": "Extract structured information from the text",
        "input": text,
        "output": json.dumps({
            "name": name,
            "role": role,
            "company": company,
            "years": yr
        })
    })


# ---------------------------
# FINALIZE
# ---------------------------

random.shuffle(data)

# Ensure total ~1350 samples balanced
data = data[:1350]

with open(raw_path, "w") as f:
    for item in data:
        f.write(json.dumps(item) + "\n")

print(f"✅ Generated {len(data)} raw samples")
print(f"Saved to: {raw_path}")