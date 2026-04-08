
---
title: Code Review Environment
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

#  Code Review, Debugging & Optimization Environment

##  Problem Statement
This project simulates a real-world software engineering workflow where an AI agent performs code review, identifies bugs, and generates corrected code.

The environment evaluates an agent’s ability to:
- Understand buggy code
- Detect syntax and logical errors
- Generate correct fixes
- Improve code reliability and robustness

This reflects real-world developer tasks such as debugging, reviewing pull requests, and maintaining production-quality code.

---

##  Objective
The goal is to benchmark AI agents on **multi-step reasoning in debugging tasks**, rather than simple code generation.

---

##  Tasks

The environment includes three levels of difficulty:

###  Easy Task (Syntax Errors)
- Fix basic syntax issues  
- Example: Missing brackets, incorrect indentation  

### Medium Task (Logical Errors)
- Identify incorrect logic in code  
- Example: Wrong condition or incorrect return values  

###  Hard Task (Complex Bugs & Edge Cases)
- Handle deeper issues such as:
  - Incorrect assumptions  
  - Edge case failures  
  - Inefficient implementations  

---

##  Grading System

Each agent output is evaluated using a deterministic scoring system from **0.0 to 1.0**.

###  Evaluation Criteria

| Metric | Description | Weight |
|--------|------------|--------|
| Correctness | Fix resolves the bug correctly | 0.5 |
| Code Structure | Clean and readable code | 0.2 |
| Logical Accuracy | Correct reasoning behind fix | 0.2 |
| Robustness | Handles edge cases | 0.1 |

---

##  Score Calculation

Final Score = correctness + structure + logic + robustness

---

##  Score Interpretation

- **1.0** → Fully correct fix  
- **0.5 – 0.9** → Partially correct  
- **0.0 – 0.4** → Incorrect solution  

---

##  API Endpoints

- `/reset` → Returns a new buggy code task  
- `/step` → Accepts agent fix and returns score  
- `/state` → Returns current task  

--

##  Use Case

This environment can be used to evaluate:
- LLM-based coding agents  
- Automated debugging systems  
- AI-assisted code review tools  

---

## Key Highlights

- Real-world software engineering scenario  
- Multi-level task difficulty  
- Deterministic grading system  
- Quantitative performance evaluation  