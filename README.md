# Global-Warming-Turbulence-Analysis-Python

## Relationship Between Global Warming and Atmospheric Turbulence

## Project Overview

This project investigates the relationship between global warming and atmospheric turbulence. Using historical datasets for CO2 emissions, global surface temperature anomalies, and turbulence events, we explore whether increases in greenhouse gas concentrations contribute to increased atmospheric instability.

The analysis includes:
- Data cleaning and standardization
- Exploratory data analysis (EDA)
- Correlation analysis
- Regression modeling
- Visualizations with trendlines

---

## Datasets

Three datasets are used:

1. **CO2 Emissions** ('CO2_Emission.csv')  
   - Contains annual CO2 emissions per country.  
   - Key columns: 'country', 'year', 'co2'  

2. **Global Surface Temperature Anomalies** ('Global_Surface_Temperature_Anomolies.csv')  
   - Contains monthly and annual temperature anomalies.  
   - Key column: 'J-D' (renamed to 'temp_anomaly')  

3. **Global Atmospheric Turbulence Data** ('global_warming_turbulence_data.csv')  
   - Contains yearly turbulence metrics.  
   - Key column: 'reported_turbulence_events' (renamed to 'turbulence_index')  

**Note:** All CSV files should be in the 'datasets/' folder.

---

## Project Structure
global-warming-turbulence/
│
├── Relationship Between Global Warming and Air Turbulence.py # Main Python script
├── datasets/
│ ├── CO2_Emission.csv
│ ├── Global_Surface_Temperature_Anomolies.csv
│ └── global_warming_turbulence_data.csv
├── README.md

---

## Installation and Requirements

This project uses Python 3.x and requires the following libraries:
- bash: pip install pandas numpy matplotlib scipy scikit-learn

## How to Run
- Make sure all CSV files are in the 'datasets/' folder.
- Update file paths in the script if necessary.
- Run the Python script: python "Relationship Between Global Warming and Air Turbulence.py"

## Code Workflow

### 1. Import Libraries
```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
```

### 2. Load Data
```
co2 = pd.read_csv('datasets/CO2_Emission.csv')
temp = pd.read_csv('datasets/Global_Surface_Temperature_Anomolies.csv')
turb = pd.read_csv('datasets/global_warming_turbulence_data.csv')
```

### 3. Clean and Standardize Columns
```
co2.columns = co2.columns.str.lower().str.strip()
temp.columns = temp.columns.str.lower().str.strip()
turb.columns = turb.columns.str.lower().str.strip()

temp = temp.rename(columns={'j-d': 'temp_anomaly'})
turb = turb.rename(columns={'reported_turbulence_events': 'turbulence_index'})
```

### 4. Aggregate CO2 Data
```
co2_global = co2.groupby('year')['co2'].mean().reset_index()
```

### 5. Merge Datasets
```
df = co2_global.merge(temp[['year', 'temp_anomaly']], on='year') \
               .merge(turb[['year', 'turbulence_index']], on='year')
```
               
### 6. Handle Missing Values
```
df = df.dropna()
```

### 7. Exploratory Analysis
```
plt.figure()
plt.plot(df['year'], df['co2'])
plt.title("CO2 Over Time")
plt.xlabel("Year")
plt.ylabel("CO2 Levels")
plt.show()

plt.figure()
plt.plot(df['year'], df['temp_anomaly'])
plt.title("Temperature Anomalies Over Time")
plt.xlabel("Year")
plt.ylabel("Temperature Anomaly")
plt.show()

plt.figure()
plt.plot(df['year'], df['turbulence_index'])
plt.title("Atmospheric Turbulence Over Time")
plt.xlabel("Year")
plt.ylabel("Turbulence Index")
plt.show()
```

### 8. Correlation Analysis
```
corr_matrix = df[['co2', 'temp_anomaly', 'turbulence_index']].corr()
print("\nCorrelation Matrix:\n", corr_matrix)

corr_temp_turb, p_val1 = pearsonr(df['temp_anomaly'], df['turbulence_index'])
corr_co2_turb, p_val2 = pearsonr(df['co2'], df['turbulence_index'])

print(f"\nTemp. vs Turbulence: r={corr_temp_turb:.3f}, p={p_val1:.5f}")
print(f"CO2 vs Turbulence: r={corr_co2_turb:.3f}, p={p_val2:.5f}")
```

### 9. Regression Analysis
```
X = df[['co2', 'temp_anomaly']]
y = df['turbulence_index']

model = LinearRegression()
model.fit(X, y)

print("\nRegression Coefficients:")
print(f"CO2 Coefficient: {model.coef_[0]}")
print(f"Temperature Coefficient: {model.coef_[1]}")
print(f"Intercept: {model.intercept_}")
```

### 10. Predictions vs Actual
```
y_pred = model.predict(X)

plt.figure()
plt.scatter(y, y_pred)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.xlabel("Actual Turbulence")
plt.ylabel("Predicted Turbulence")
plt.title("Actual vs Predicted Turbulence")
plt.show()
```

### 11. Trend Relationship Plots

#### Temperature vs Turbulence
```
plt.figure()
plt.scatter(df['temp_anomaly'], df['turbulence_index'])
m, b = np.polyfit(df['temp_anomaly'], df['turbulence_index'], 1)
plt.plot(df['temp_anomaly'], m*df['temp_anomaly'] + b, color='red')
plt.xlabel("Temperature Anomaly")
plt.ylabel("Turbulence")
plt.title("Temp. vs Turbulence")
plt.show()
```

#### CO2 vs Turbulence
```
plt.figure()
plt.scatter(df['co2'], df['turbulence_index'])
m, b = np.polyfit(df['co2'], df['turbulence_index'], 1)
plt.plot(df['co2'], m*df['co2'] + b, color='red')
plt.xlabel("CO2 Levels")
plt.ylabel("Turbulence")
plt.title("CO2 vs Turbulence")
plt.show()
```

## Key Findings

### Strong positive correlations:
Temperature vs Turbulence: r= ~0.77
CO2 vs Turbulence: r= ~0.78

### Regression Results:
Temperature has a larger effect on turbulence than CO2
CO2 contributes indirectly via global warming
Statistical significance: p < 0.001 for all relationships

Interpretation:
Rising greenhouse gases increase global temperatures which strongly influence atmospheric turbulence. This supports the hypothesis that global warming
contributes to increased atmospheric instability.

## Notes and Recommendations
- NaN values in early historical years are expected due to incomplete records.
- Only complete rows are used for analysis.
- Analysis shows association, not causation.
- Trendlines in scatterplots visually support regression findings.

## Author
Marco A. Lapcevic

---
