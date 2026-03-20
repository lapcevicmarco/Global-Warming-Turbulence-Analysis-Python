# =========================
# 1. Import Libraries
# =========================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression

# ========================= 
# 2. Load Data
# =========================
co2 = pd.read_csv('CO2_Emission.csv')
temp = pd.read_csv('Global_Surface_Temperature_Anomolies.csv')
turb = pd.read_csv('global_warming_turbulence_data.csv')

# =========================
# CLEAN + STANDARDIZE COLUMNS
# =========================
co2.columns = co2.columns.str.lower().str.strip()
temp.columns = temp.columns.str.lower().str.strip()
turb.columns = turb.columns.str.lower().str.strip()

# Fix incorrect column names
temp = temp.rename(columns={'j-d': 'temp_anomaly'})
turb = turb.rename(columns={
    'reported_turbulence_events': 'turbulence_index'
})

# =========================
# 3. Inspect Data
# =========================
print(co2.nunique())
print(temp.nunique())
print(turb.nunique())

# =========================
# 4. Standardize Column Names
# =========================
co2.columns = co2.columns.str.strip().str.lower()
temp.columns = temp.columns.str.strip().str.lower()
turb.columns = turb.columns.str.strip().str.lower()

# =========================
# 5. Merge Datasets
# =========================

# =========================
# FIX CO2 DATA (AGGREGATE)
# =========================
co2_global = co2.groupby('year')['co2'].mean().reset_index()

# =========================
# MERGE DATA CORRECTLY
# =========================
df = co2_global.merge(temp[['year', 'temp_anomaly']], on='year') \
               .merge(turb[['year', 'turbulence_index']], on='year')

print(df.nunique())

# =========================
# 6. Handle Missing Values
# =========================
df = df.dropna()

# =========================
# 7. Exploratory Analysis
# =========================
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

# =========================
# 8. Correlation Analysis
# =========================
corr_matrix = df[['co2', 'temp_anomaly', 'turbulence_index']].corr()
print("\nCorrelation Matrix:\n", corr_matrix)

# Individual correlations
corr_temp_turb, p_val1 = pearsonr(df['temp_anomaly'], df['turbulence_index'])
corr_co2_turb, p_val2 = pearsonr(df['co2'], df['turbulence_index'])

print(f"\nTemp. vs Turbulence: r={corr_temp_turb:.3f}, p={p_val1:.5f}")
print(f"CO2 vs Turbulence: r={corr_co2_turb:.3f}, p={p_val2:.5f}")

# =========================
# 9. Regression Analysis
# =========================
X = df[['co2', 'temp_anomaly']]
y = df['turbulence_index']

model = LinearRegression()
model.fit(X, y)

print("\nRegression Coefficients:")
print(f"CO2 Coefficient: {model.coef_[0]}")
print(f"Temperature Coefficient: {model.coef_[1]}")
print(f"Intercept: {model.intercept_}")

# =========================
# 10. Predictions vs Actual
# =========================
y_pred = model.predict(X)

plt.figure()
plt.scatter(y, y_pred)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')  # dashed red line
plt.xlabel("Actual Turbulence")
plt.ylabel("Predicted Turbulence")
plt.title("Actual vs Predicted Turbulence")
plt.show()

# =========================
# 11. Trend Relationship Plots
# =========================
plt.figure()
plt.scatter(df['temp_anomaly'], df['turbulence_index'])
# Fit linear trend
m, b = np.polyfit(df['temp_anomaly'], df['turbulence_index'], 1)
plt.plot(df['temp_anomaly'], m*df['temp_anomaly'] + b, color='red')
plt.xlabel("Temperature Anomaly")
plt.ylabel("Turbulence")
plt.title("Temp. vs Turbulence")
plt.show()

plt.figure()
plt.scatter(df['co2'], df['turbulence_index'])
# Fit linear trend
m, b = np.polyfit(df['co2'], df['turbulence_index'], 1)
plt.plot(df['co2'], m*df['co2'] + b, color='red')
plt.xlabel("CO2 Levels")
plt.ylabel("Turbulence")
plt.title("CO2 vs Turbulence")
plt.show()