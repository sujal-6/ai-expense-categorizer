# AI Expense Categorizer with Anomaly Detection

An intelligent expense processing system that uses a **Large Language Model (LLM)** to automatically categorize expenses and detect anomalous spending patterns. The system is optimized for performance using caching and includes statistical anomaly detection for financial auditing and monitoring.

---

# Table of Contents

* Overview
* Features
* System Architecture
* How It Works
* Categorization System
* Anomaly Detection System
* Prompt Engineering Strategy
* Cache System
* Project Structure
* Installation
* Usage
* Example
* Configuration
* Performance Optimizations
* Limitations
* Future Improvements
* Tech Stack

---

# Overview

The AI Expense Categorizer is designed to automate expense classification and anomaly detection using LLM-powered semantic understanding combined with statistical analysis.

It solves key problems such as:

* Manual expense categorization
* Inconsistent expense labeling
* Detection of abnormal or suspicious expenses
* Scalable processing of large expense datasets

The system uses:

* LLaMA3 via Ollama for classification
* JSON-based caching for performance optimization
* Statistical methods for anomaly detection
* Batch processing support

---

# Features

## Core Features

* LLM-based intelligent expense categorization
* Statistical anomaly detection
* Duplicate expense detection
* Batch processing support
* Persistent caching to reduce LLM calls
* Structured JSON output
* Robust validation and fallback handling

## Advanced Features

* Semantic understanding of expense descriptions
* Cache key optimization for fast retrieval
* Deterministic categorization for repeated inputs
* Modular and extensible architecture
* Fault-tolerant design

---

# System Architecture

```
Input Expense Data
        │
        ▼
Validation Layer
        │
        ▼
Cache Lookup ───────► Cache Hit ─────► Return Category
        │
        ▼ Cache Miss
LLM Classification (LLaMA3 via Ollama)
        │
        ▼
Output Validation
        │
        ▼
Cache Storage
        │
        ▼
Categorized Dataset
        │
        ▼
Anomaly Detection Engine
        │
        ▼
Final Output with Anomaly Flags
```

---

# How It Works

The system processes expenses in two main phases:

## Phase 1: Categorization

Each expense description is classified into one of the predefined categories using an LLM.

Steps:

1. Validate description
2. Check cache
3. If cached → return category
4. If not cached → send prompt to LLM
5. Validate response
6. Store result in cache
7. Return category

---

## Phase 2: Anomaly Detection

After categorization, statistical analysis is performed to identify abnormal expenses.

Methods used:

* Standard deviation analysis
* Mean deviation thresholds
* Duplicate detection

---

# Categorization System

## Supported Categories

```
Travel
Meals
Software
Utilities
Other
```

## Categorization Logic

Classification is based on semantic interpretation of expense descriptions.

Example:

| Description          | Category  |
| -------------------- | --------- |
| Uber ride to airport | Travel    |
| Lunch at restaurant  | Meals     |
| AWS subscription     | Software  |
| Electricity bill     | Utilities |

---

# Anomaly Detection System

The system uses multiple techniques:

## 1. Statistical Outlier Detection

Formula:

```
Anomaly if:
|amount - mean(category)| > 2 × std(category)
```

Detects unusually large or small expenses.

---

## 2. Deviation Detection

Flags expenses if:

```
amount > 1.5 × mean
or
amount < 0.5 × mean
```

Detects spending spikes.

---

## 3. Duplicate Detection

Flags duplicate entries based on:

```
(date, amount, description)
```

Prevents duplicate reimbursements.

---

## Output Fields Added

```
category
anomaly (True/False)
anomaly_reason
```

---

# Prompt Engineering Strategy

The prompt ensures strict structured output.

## Prompt Template

```
You are an expense classification assistant. Classify the following expense into ONE of these categories:
[Travel, Meals, Software, Utilities, Other]

Return ONLY a valid JSON object in this format:
{"category": "CategoryName"}

Expense Description: "[description]"
```

## Design Goals

* Prevent hallucinations
* Enforce structured output
* Restrict to valid categories
* Ensure deterministic results

---

# Cache System

The system uses a persistent JSON cache:

```
classification_cache.json
```

## Purpose

* Reduce LLM calls
* Improve performance
* Ensure consistent classification

## Cache Key Format

```
model_name:categories:description
```

## Benefits

* Faster execution
* Lower compute cost
* Deterministic outputs

---

# Project Structure

```
ai-expense-categorizer/
│
├── app.py
├── categorizer.py
├── anomaly_detection.py
├── process_data.py
├── reports.py
│
├── data/
│   └── expenses.csv
│
├── requirements.txt
└── README.md

```

---

# Installation

## Step 1: Clone Repository

```
git clone https://github.com/yourusername/ai-expense-categorizer.git
cd ai-expense-categorizer
```

---

## Step 2: Install Dependencies

```
pip install -r requirements.txt
```

---

## Step 3: Install Ollama

Download from:

https://ollama.com

---

## Step 4: Pull LLaMA3 Model

```
ollama pull llama3
```

---

# Usage

## Basic Usage

```python
from categorizer import categorize_expense

category = categorize_expense("Uber ride to airport")
print(category)
```

---

## Batch Usage

```python
import pandas as pd
from categorizer import categorize_dataframe

df = pd.read_csv("expenses.csv")

result = categorize_dataframe(df)

print(result.head())
```

---

## Run Anomaly Detection

```python
from anomaly_detector import detect_anomalies

result = detect_anomalies(df)
```

---

# Example

## Input

```
date,amount,description
2025-01-01,250,Uber ride
2025-01-02,5000,AWS subscription
2025-01-03,120,Lunch
```

## Output

```
date,amount,description,category,anomaly,anomaly_reason
2025-01-01,250,Uber ride,Travel,False,
2025-01-02,5000,AWS subscription,Software,True,Statistical outlier
2025-01-03,120,Lunch,Meals,False,
```

---

# Configuration

## Change Categories

Edit in:

```
categorizer.py
```

```
CATEGORIES = [
    "Travel",
    "Meals",
    "Software",
    "Utilities",
    "Other"
]
```

---

## Change Model

```
MODEL_NAME = "llama3"
```

---

# Performance Optimizations

The system uses several optimizations:

* Persistent caching
* Batch processing
* Unique description filtering
* JSON validation layer
* Minimal LLM calls

---

# Limitations

## Categorization Limitations

* Depends on LLM accuracy
* No confidence score
* Limited predefined categories
* Ambiguous descriptions may misclassify

## Anomaly Detection Limitations

* Uses statistical assumptions
* Limited contextual awareness
* Fixed thresholds
* No ML-based anomaly detection

## System Limitations

* Requires Ollama running locally
* Cache may become stale if categories change

---

# Future Improvements

* Confidence scoring
* Embedding-based classification
* Isolation Forest anomaly detection
* Semantic duplicate detection
* Dynamic categories
* Cloud deployment support
* API interface
* Dashboard visualization

---

# Tech Stack

## Core

* Python
* Pandas
* JSON

## AI/ML

* LLaMA3
* Ollama
* Prompt Engineering

## Detection

* Statistical Analysis
* Rule-Based Detection

---

# Use Cases

* Corporate expense management
* Financial auditing
* Fraud detection
* Personal finance tracking
* Automated bookkeeping

---

# Summary

The AI Expense Categorizer provides:

* Intelligent expense classification
* Efficient caching system
* Statistical anomaly detection
* Scalable architecture
* Production-ready design

---