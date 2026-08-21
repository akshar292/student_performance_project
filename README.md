# 🎓 StudentIQ - Student Performance Intelligence & Prediction Platform

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.61.1-red?logo=streamlit)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-blue?logo=mysql)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> An end-to-end Student Performance Analytics and Machine Learning Prediction Platform built with Python, MySQL, SQL, Scikit-Learn, Streamlit and Plotly.

---

## 🌐 Live Demo

🚀 **[Open StudentIQ Live Application](https://studentperformanceprojectgit-6cncbxbzdp58y8oba3y2f5.streamlit.app/)**

---

## 📌 Overview

StudentIQ is an end-to-end **Student Performance Analytics and Prediction Platform** designed to analyze student academic performance and generate Machine Learning based predictions.

The platform combines:

- SQL-based data analysis
- Data processing with Pandas
- Statistical and correlation analysis
- Interactive data visualization
- Machine Learning
- Student search and filtering
- Individual student prediction
- Batch CSV prediction
- Academic recommendations

The system uses the following academic factors:

- Attendance
- Study Hours
- Assignment Score
- Midterm Score
- Previous Score

Based on these features, StudentIQ provides:

- 📈 Final Score Prediction
- ✅ PASS / ❌ FAIL Prediction
- 📊 PASS / FAIL Probability
- 💡 Personalized Academic Recommendations
- 📊 Performance Analytics
- 🗄️ SQL-based Insights

---

# 🚀 Features

## 🏠 Dashboard

The Dashboard provides an overall view of student performance.

### Includes:

- Total Students
- Average Final Score
- PASS / FAIL Distribution
- Pass Percentage
- City-wise Performance
- Top Performing City
- Overall Performance Metrics

---

## 📊 Analytics

The Analytics section provides detailed insights into academic performance.

### Analysis includes:

- Attendance vs Final Score
- Study Hours vs Final Score
- Midterm Score vs Final Score
- Final Score Distribution
- Correlation Matrix
- Feature Correlation
- Random Forest Feature Importance
- Academic Performance Analysis

---

## 🤖 AI Prediction

The AI Prediction module uses Machine Learning models to predict student performance.

### Input Features:

- Attendance
- Study Hours
- Assignment Score
- Midterm Score
- Previous Score

### Outputs:

- Predicted Final Score
- PASS / FAIL Prediction
- PASS Probability
- FAIL Probability
- Personalized Academic Recommendations

---

## 🔍 Student Directory

The Student Directory allows users to search and analyze student records.

### Search options:

- Student ID
- Student Name
- City

Users can view individual student information and performance details.

---

## 🗄️ SQL Insights

The SQL Insights section provides database-level analytics.

### Available analysis:

- Total Students
- Average Final Score
- City-wise Performance
- Top 10 Students
- Low Performing Students
- PASS / FAIL Distribution
- City-wise Pass Rate
- Custom SQL Analysis

---

## 📁 Batch Prediction

Users can upload a CSV file containing multiple student records.

### Required CSV columns:

```text
attendance
study_hours
assignment_score
midterm_score
previous_score
