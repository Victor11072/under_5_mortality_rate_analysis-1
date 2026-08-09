# Deep Research on Under-5 Mortality Rates Across Countries of the World
A data-driven exploration of global under-5 mortality, examining trends, income-group differences, regional disparities, stalled progress, and geographic patterns across countries.

## 📌 Project Overview

Under-5 mortality remains an important indicator of child health and development. This project explores how the rate of deaths among children under five has changed across countries and how these outcomes differ by **income group, region, population size, and geography**.

Rather than looking at a single measure, the project gradually approaches the problem from different perspectives — from cleaning and understanding the data, to statistical comparison, disparity analysis, and geographic visualization.

This project is part of my 30-Day Learning & Building Challenge, where I am applying my Data Science skills to a real-world problem while strengthening my ability to build projects that are **reproducible, organized, and well documented.**

The analysis goes beyond simply looking at averages. It examines global trends, income-group differences, regional disparities, countries with stalled progress, and geographic patterns using data visualization.

This project is being developed as part of my **30-Day Learning & Building Challenge**, where I am applying my Data Science skills to a real-world problem while strengthening my approach to reproducible and well-documented analysis.

## 🎯 Research Questions

The project seeks to answer questions such as:

- How has under-5 mortality changed globally since 2000?
- How different are under-5 mortality rates across income groups?
- Does population size explain differences in under-5 mortality?
- Which regions experience the highest burden of child mortality?
- Which countries have experienced the greatest improvements?
- Which countries have experienced stalled progress?
- Where are the largest geographic disparities?


## 📅 Week 1 — Data Foundation
Week 1 focused on building the foundation for the project — from obtaining and cleaning the data to exploring trends, comparing groups, identifying disparities, mapping geographic patterns, and strengthening the tools needed to maintain the project.

### Day 1 — Ingest & Clean

The first day focused on obtaining and preparing the datasets required for the analysis.

Key tasks included:

- Importing datasets directly into Python using URLs/APIs where possible.
- Cleaning and validating the data.
- Using country codes to distinguish countries from aggregate regions.
- Adding World Bank income-group information.
- Preparing the datasets for further analysis.

**Outcome:**  
A clean foundation was created for analysing under-5 mortality across countries and over time.


### Day 2 — Descriptive Statistics & Trends

The second day focused on understanding the overall pattern of under-5 mortality.

Key tasks included:

- Combining under-5 mortality data with population data.
- Restricting the analysis to the period from 2000 onward.
- Examining changes in mortality over time.
- Calculating a population-weighted global under-5 mortality rate.

**Outcome:**  
The analysis provided a clearer picture of global mortality trends while accounting for differences in population size.


### Day 3 — Group Comparison

The third day examined differences in under-5 mortality across World Bank income groups.

Key tasks included:

- Comparing mortality rates across High, Upper-middle, Lower-middle and Low-income groups.
- Testing whether the differences between groups were statistically significant.
- Examining whether population size could explain the observed differences.

**Outcome:**  
Under-5 mortality differed substantially across income groups, while population size alone provided little explanation for the differences.


### Day 4 — Disparity Analysis

The fourth day moved beyond averages to investigate disparities in progress.

The analysis focused on:

- Countries with stalled progress since 2000.
- Differences in mortality across regions.
- Differences across income groups.
- Countries and regions showing stronger improvements.

**Outcome:**  
The analysis showed that progress in reducing under-5 mortality has not been equally distributed across countries and regions.


### Day 5 — Geographic Mapping

The fifth day focused on visualizing under-5 mortality geographically using a choropleth map.

The map was used to identify where higher and lower mortality rates are concentrated across the world.

**Outcome:**  
The geographic visualization made regional patterns and disparities easier to identify than viewing the values as a table alone.


### Day 6 — Git & GitHub

Day 6 focused on strengthening the Git and GitHub skills needed to properly document and maintain the project.

I completed:

- Introduction to Git
- Intermediate Git
- Introduction to GitHub Concepts

As the project became more structured, I realized that building a meaningful data project is not only about analysis.

It also requires the ability to **track changes, organize files, document the work, and make the analysis reproducible.**

**Outcome:**  
I strengthened my Git and GitHub knowledge and prepared the project for a more organized and maintainable workflow.


### Day 7 — Polish & Reflect

The final day of Week 1 is focused on transforming the work completed throughout the week into a structured, documented and reproducible GitHub project.

Key tasks include:

- Organizing the project repository.
- Finalizing the README documentation.
- Organizing notebooks, datasets and outputs.
- Documenting data sources and tools used.
- Adding visualizations and key findings.
- Reviewing the analysis for consistency and clarity.
- Preparing the project for publication and sharing.

**Outcome:**
A complete and organized GitHub repository that documents the Week 1 journey from data collection and cleaning to analysis, visualization and reflection.


## 📊 Key Findings
- The analysis conducted during Week 1 revealed several important patterns:
- Under-5 mortality has generally declined over time, but the pace of progress differs considerably across countries.
- Mortality rates vary substantially across World Bank income groups.
- Population size alone does not explain the differences in under-5 mortality.
- Sub-Saharan Africa has the highest regional burden of under-5 mortality.
- Some countries have experienced very limited improvement since 2000.
- Geographic visualization reveals clear concentrations of higher and lower mortality rates.


## 📈 Visualizations
*The project includes visualizations developed throughout the analysis, including:*

**Global Trends**

- Visualizing how under-5 mortality has changed since 2000.

**Income-Group Comparison**

- Comparing mortality across World Bank income classifications.

**Regional Comparison**

- Examining differences in mortality across global regions.

**Disparity Analysis**

- Identifying countries with stalled progress and countries showing stronger improvements.

**Geographic Mapping**

- A choropleth map showing under-5 mortality rates across countries.

## 🗂️ Data Sources
*The project uses publicly available data from:*

- **Our World in Data** — Under-5 Mortality
- **World Bank API** — Population and country metadata
- **World Bank** — Income-group classifications
- **GeoPandas Natural Earth boundary data** — Geographic mapping
- **Pycountry** — Country/ISO code validation

## 🛠️ Tools & Technologies
*The project is primarily developed using:*

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- GeoPandas
- SciPy
- Statsmodels
- Jupyter Notebook
- Git
- GitHub

## 📁 Project Structure
under-5-mortality-analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_ingest_clean.ipynb
│   ├── 02_descriptive_stats_trends.ipynb
│   ├── 03_group_comparison.ipynb
│   ├── 04_disparity_analysis.ipynb
│   ├── 05_geographic_mapping.ipynb
│   └── 06_git_github_workflow.ipynb
│
├── scripts/
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── README.md
└── requirements.txt

## 🔄 How to Reproduce
The goal of this project is to make the analysis as reproducible as possible.

Where available, datasets are accessed directly through URLs or APIs rather than relying solely on manually downloaded files.

To reproduce the analysis:

1. Clone this repository.
2. Install the required Python packages.
3. Open the notebooks in the notebooks/ directory.
4. Run the notebooks in sequence.
5. Generated figures and tables will be saved in the outputs/ directory.

## 🚀 Future Improvements
*Future stages of the project may include:*

- Extending the analysis to additional health indicators.
- Improving automated data collection.
- Automating the data-cleaning and analysis pipeline.
- Adding more interactive visualizations.
- Developing a dashboard for exploring country-level patterns.
- Automating updates as new data becomes available.

## 👤 Author
**Victor Olumide**
Associate Data Scientist

**30-Day Learning & Building Challenge**

*Building in public. Learning by solving real problems with data.*