## 📈 Week 2 — Predictive & Diagnostic Analysis

Week 2 moved the project from descriptive analysis into predictive modelling.

The focus was to investigate whether socioeconomic and health-related indicators could help explain differences in under-5 mortality across countries.

### Day 8 — Data Integration

Integrated additional World Bank indicators with the Week 1 mortality dataset:

- GDP per capita
- Health expenditure (% of GDP)
- DPT3 immunization coverage
- Basic sanitation
- Female literacy

Female literacy was excluded from the main analytical dataset because of substantial missing values.

### Day 9 — Predictor Exploration

Examined relationships between the predictors and under-5 mortality using:

- Correlation analysis
- Correlation heatmap
- Variance Inflation Factor (VIF)

VIF values ranged from approximately 1.06 to 1.57, indicating no serious multicollinearity among the four retained predictors.

### Day 10 — Baseline Model

Built an initial multiple linear regression model using:

- GDP per capita
- Health expenditure
- DPT3 immunization
- Basic sanitation

The initial model explained 51.8% of the variation in under-5 mortality.

Diagnostic analysis identified the Central African Republic as an extreme observation that strongly influenced the model.

A second model excluding this observation produced an R² of 73.2%.

### Model Refinement

Compared:

- OLS
- Ridge Regression
- Lasso Regression

using an 80/20 train-test split with `random_state=42`.

For the model excluding the Central African Republic:

| Model | R² | RMSE | MAE |
|---|---:|---:|---:|
| OLS | 0.819 | 9.721 | 6.905 |
| Ridge | 0.819 | 9.719 | 6.936 |
| Lasso | 0.818 | 9.758 | 7.372 |

### Residual Analysis

Residuals were used to compare actual mortality with model-predicted mortality.

Countries with negative residuals performed better than the model predicted, while positive residuals indicated worse-than-predicted outcomes.

Top over-performers included:

- Papua New Guinea
- Solomon Islands
- Vanuatu
- São Tomé and Príncipe
- Nicaragua

Top under-performers included:

- Nigeria
- Equatorial Guinea
- Niger
- Turkmenistan
- Sierra Leone

This analysis provided a different perspective from simply ranking countries by mortality: it examined how countries performed relative to what the model expected given their socioeconomic characteristics.

### Female Literacy — Supplementary Analysis

Although female literacy was excluded from the main model because of missing data, a supplementary analysis was conducted using the 42 countries with available observations.

The five-predictor model produced:

- R² = 85.4%
- Adjusted R² = 83.3%
- Female literacy p-value = 0.004

Because this analysis uses only 42 countries compared with 167 in the main model, its results should be interpreted separately rather than treated as a direct improvement to the main model.