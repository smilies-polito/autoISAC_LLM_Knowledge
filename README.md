# Assessing LLMs Knowledge of Automotive Cyberthreats
### Benchmarking the Auto-ISAC Framework

This repository contains the data and resources accompanying the paper:

> **Scarano, N., Mannella, L., Savino, A., & Di Carlo, S. (2025).**  
> *Assessing LLMs models’ knowledge of automotive cyberthreats benchmarking Auto-ISAC framework.*  
> In Proceedings of the 2025 Cyber Security in Cars Workshop (CSCS ’25), Taipei, Taiwan.  
> DOI: [10.1145/3736130.3762690](https://doi.org/10.1145/3736130.3762690)

---

## 🧠 Overview

The project evaluates how **Large Language Models (LLMs)** understand and reason about **automotive cybersecurity** concepts defined in the **Auto-ISAC** (Automotive Information Sharing and Analysis Center) framework.

A dedicated pipeline based on GPT-4o was used to:
1. Generate domain-specific cybersecurity questions grounded in Auto-ISAC threat procedures.  
2. Manually validate and refine the questions.  
3. Benchmark five state-of-the-art LLMs against responses from 17 human domain experts.

All data supporting the study—including Auto-ISAC threat descriptions, generated question sets, and visualization artifacts—is released here for academic use.

---

## 📂 Repository Structure

'''
accessing_llms_knowledge/
├── autoISAC/
│ ├── procedures.json # Auto-ISAC threat matrix source
│ └── v4.00.json # Full Auto-ISAC reference file
│
├── chunks/
│ ├── group_1.json … group_14.json
│ # Thematic chunks of Auto-ISAC data used as GPT inputs
│
├── question_generation_data/
│ ├── questions_no_answer.json # Raw LLM-generated questions
│ ├── questions_with_answer.json # Final validated questions + answers
│ ├── questions/
│ │ ├── mcqs_group_.json # Multiple-choice question sets
│ └── questions_tf/
│ ├── tfqs_group_.json # True/False question sets
│
├── imgs/
│ └── score_distribution_plot.png # LLM vs human performance visualization
│
└── ReadMe.md
'''


## 📊 Contents

| File / Folder | Description |
|----------------|-------------|
| `autoISAC/` | Raw Auto-ISAC threat data used as the domain knowledge base. |
| `chunks/` | Preprocessed subsets (“chunks”) of the Auto-ISAC data supplied to GPT-4o during question generation. |
| `question_generation_data/questions/` | Automatically generated multiple-choice questions. |
| `question_generation_data/questions_tf/` | Automatically generated true/false questions. |
| `question_generation_data/questions_with_answer.json` | Final curated dataset of 25 validated questions (10 MCQ + 15 T/F). |
| `imgs/score_distribution_plot.png` | Graph comparing LLM accuracy with human expert scores. |
