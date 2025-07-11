# PSX Trading Debate AI Agent — V1 Dataflows

This repository is part of an ongoing project aimed at building a comprehensive AI agent capable of understanding and debating trading choices, specifically focused on the Pakistan Stock Exchange (PSX).

## Version 1 — Dataflows

The primary objective of this version is to establish the foundational data ingestion pipelines that will power the AI agent. These dataflows will focus on collecting relevant trading data and financial information necessary for subsequent analysis and model development.

---

### Components

#### 1. **Sarmaya.pk Scraper**

* A simple scraper will be implemented to extract data from [Sarmaya.pk](https://sarmaya.pk/).
* The scraper will systematically collect data relevant to PSX trading, such as company information, stock data, and any other publicly available datasets on the platform.

#### 2. **Optional Financial News Scraper**

* An optional scraper will be designed to gather financial news from various online news sources.
* This data will help provide context and sentiment insights that may influence trading decisions.

#### 3. **Orchestration with Airflow**

* Apache Airflow will be used to orchestrate and schedule the scraping jobs.
* Airflow will manage the execution sequence, handle failures, and ensure that data is collected reliably and regularly.

#### 4. **Future Optimizations**

* After establishing functional data pipelines, optimization efforts will focus on improving code readability and maintainability.
* This will include better modularization, documentation, and adherence to clean coding practices.

---

### Project Scope (V1 Summary)

* Build and deploy initial scrapers.
* Integrate scrapers into an Airflow DAG.
* Ensure that the system reliably collects data from Sarmaya.pk and optionally from financial news sources.
* Lay the groundwork for later enhancements, with a focus on code quality.

--- 

## Version 2 - Data Cleaning and Context Database

The primary objective here is to create a vector DB and relational DB after cleaning the data to produce a more cohesive structure. This version aims to evaluate the Feasibility of teh two as well. i.e. evaluate if Vector DB outperforms a relational DB and vice-versa.

--- 

### Components

#### 1. **Relational Database in MySQL**
* *Details to be added based on implementation plan*

#### 2. **Vector Database compatible with Groq**
* *Details to be added based on implementation plan*

---

### Project Scope (V2 Summary)
* *Summary to be added soon*

---

***Note:*** *Future versions will build upon V1 & V2 to create a complete structured AI agent capable of analysing comapnies and suggesting investment options based on investment goals.*