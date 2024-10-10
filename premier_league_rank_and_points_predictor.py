# -*- coding: utf-8 -*-
"""premier-league-rank-and-points-predictor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16P6fMZGtLDUgZg4AxUY9v5OHPJPFKby6
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
import numpy as np

file_path = '/kaggle/input/premier-league-season-2024/PremierLeagueSeason2024.csv'
df = pd.read_csv(file_path)

# Inspect dataset
df.info()
df.describe()
df.isnull().sum()

df.head()

plt.figure(figsize=(10,6))
sns.heatmap(df.drop(columns=['team']).corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.show()

# Bar plot for top 5 teams by points
df.sort_values('points', ascending=False).head(5).plot(x='team', y='points', kind='barh')
plt.title("Top 5 Teams by Points")
plt.show()

plt.figure(figsize=(14, 8))

# Plot Wins for each team
sns.barplot(x='team', y='wins', data=df, palette='Blues_d')
plt.title('Wins per Team', fontsize=16)
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.xlabel('Team', fontsize=12)
plt.ylabel('Wins', fontsize=12)
plt.grid(True)
plt.show()

# Plot Losses for each team
plt.figure(figsize=(14, 8))
sns.barplot(x='team', y='losses', data=df, palette='Reds_d')
plt.title('Losses per Team', fontsize=16)
plt.xticks(rotation=90)
plt.xlabel('Team', fontsize=12)
plt.ylabel('Losses', fontsize=12)
plt.grid(True)
plt.show()

# Plot Draws for each team
plt.figure(figsize=(14, 8))
sns.barplot(x='team', y='draws', data=df, palette='Greens_d')
plt.title('Draws per Team', fontsize=16)
plt.xticks(rotation=90)
plt.xlabel('Team', fontsize=12)
plt.ylabel('Draws', fontsize=12)
plt.grid(True)
plt.show()

# Plot Goals Scored for each team
plt.figure(figsize=(14, 8))
sns.barplot(x='team', y='goals_scored', data=df, palette='Purples_d')
plt.title('Goals Scored per Team', fontsize=16)
plt.xticks(rotation=90)
plt.xlabel('Team', fontsize=12)
plt.ylabel('Goals Scored', fontsize=12)
plt.grid(True)
plt.show()

# Plot Goals Conceded for each team
plt.figure(figsize=(14, 8))
sns.barplot(x='team', y='goals_conceded', data=df, palette='Oranges_d')
plt.title('Goals Conceded per Team', fontsize=16)
plt.xticks(rotation=90)
plt.xlabel('Team', fontsize=12)
plt.ylabel('Goals Conceded', fontsize=12)
plt.grid(True)
plt.show()

# Plot Points for each team
plt.figure(figsize=(14, 8))
sns.barplot(x='team', y='points', data=df, palette='coolwarm')
plt.title('Points per Team', fontsize=16)
plt.xticks(rotation=90)
plt.xlabel('Team', fontsize=12)
plt.ylabel('Points', fontsize=12)
plt.grid(True)
plt.show()

# Feature Engineering: Add win_rate, draw_rate, loss_rate
df['win_rate'] = df['wins'] / (df['wins'] + df['draws'] + df['losses'])
df['draw_rate'] = df['draws'] / (df['wins'] + df['draws'] + df['losses'])
df['loss_rate'] = df['losses'] / (df['wins'] + df['draws'] + df['losses'])

# Plot Win Rate for each team
plt.figure(figsize=(14, 8))
sns.barplot(x='team', y='win_rate', data=df, palette='Blues_d')
plt.title('Win Rate per Team', fontsize=16)
plt.xticks(rotation=90)
plt.xlabel('Team', fontsize=12)
plt.ylabel('Win Rate', fontsize=12)
plt.grid(True)
plt.show()

# Plot Draw Rate for each team
plt.figure(figsize=(14, 8))
sns.barplot(x='team', y='draw_rate', data=df, palette='Greens_d')
plt.title('Draw Rate per Team', fontsize=16)
plt.xticks(rotation=90)
plt.xlabel('Team', fontsize=12)
plt.ylabel('Draw Rate', fontsize=12)
plt.grid(True)
plt.show()

# Plot Loss Rate for each team
plt.figure(figsize=(14, 8))
sns.barplot(x='team', y='loss_rate', data=df, palette='Reds_d')
plt.title('Loss Rate per Team', fontsize=16)
plt.xticks(rotation=90)
plt.xlabel('Team', fontsize=12)
plt.ylabel('Loss Rate', fontsize=12)
plt.grid(True)
plt.show()

"""# **1. Using Linear Regression**"""

X = df[['goals_scored', 'goals_conceded', 'wins', 'draws', 'losses', 'points', 'goal_difference']]
y_rank = df['rank']
y_points = df['points']

X_train, X_test, y_rank_train, y_rank_test = train_test_split(X, y_rank, test_size=0.2, random_state=42)
_, _, y_points_train, y_points_test = train_test_split(X, y_points, test_size=0.2, random_state=42)

linear_model_rank = LinearRegression()
linear_model_rank.fit(X_train, y_rank_train)

y_rank_pred_linear = linear_model_rank.predict(X_test)
mae_rank_linear = mean_absolute_error(y_rank_test, y_rank_pred_linear)
r2_rank_linear = r2_score(y_rank_test, y_rank_pred_linear)
cv_scores_rank = cross_val_score(linear_model_rank, X, y_rank, cv=5, scoring='neg_mean_absolute_error')

print(f"Linear Regression - Rank Mean Absolute Error: {mae_rank_linear}")
print(f"Linear Regression - Rank R²: {r2_rank_linear}")
print(f"Cross-Validated MAE for Rank Prediction: {-np.mean(cv_scores_rank)}")

linear_model_points = LinearRegression()
linear_model_points.fit(X_train, y_points_train)

y_points_pred_linear = linear_model_points.predict(X_test)
mae_points_linear = mean_absolute_error(y_points_test, y_points_pred_linear)
r2_points_linear = r2_score(y_points_test, y_points_pred_linear)
cv_scores_points = cross_val_score(linear_model_points, X, y_points, cv=5, scoring='neg_mean_absolute_error')

print(f"Linear Regression - Points Mean Absolute Error: {mae_points_linear}")
print(f"Linear Regression - Points R²: {r2_points_linear}")
print(f"Cross-Validated MAE for Rank Prediction: {-np.mean(cv_scores_points)}")

y_rank_pred_all = linear_model_rank.predict(X)
y_points_pred_all = linear_model_points.predict(X)

residuals_rank = df['rank'] - y_rank_pred_all
residuals_points = df['points'] - y_points_pred_all
residuals_rank_df = pd.DataFrame({'team': df['team'], 'rank_residuals': residuals_rank})
residuals_points_df = pd.DataFrame({'team': df['team'], 'points_residuals': residuals_points})
residuals_combined_df = pd.merge(residuals_rank_df, residuals_points_df, on='team')

print("Residuals for Rank:")
print(residuals_combined_df[['team', 'rank_residuals']].sort_values('rank_residuals', key=abs, ascending=False))

print("\nResiduals for Points:")
print(residuals_combined_df[['team', 'points_residuals']].sort_values('points_residuals', key=abs, ascending=False))

y_rank_pred_all = linear_model_rank.predict(X)
y_points_pred_all = linear_model_points.predict(X)

y_test_inverted = max(y_rank) + 1 - df['rank']
y_pred_inverted = max(y_rank) + 1 - y_rank_pred_all

plt.figure(figsize=(10, 6))
plt.scatter(y_test_inverted, y_pred_inverted, color='blue', label='Predicted Rank')
plt.plot([min(y_test_inverted), max(y_test_inverted)], [min(y_test_inverted), max(y_test_inverted)], color='red', lw=2, label='Perfect Prediction')
plt.title('Actual vs Predicted Rank for All Teams')
plt.xlabel('Actual Rank')
plt.ylabel('Predicted Rank (Inverted)')
plt.legend()
plt.grid(True)

for i, team in enumerate(df['team']):
    plt.text(y_test_inverted.iloc[i], y_pred_inverted[i], team, fontsize=8, ha='right')

plt.show()

residuals_rank = df['rank'] - y_rank_pred_all
plt.figure(figsize=(10, 6))
plt.scatter(y_rank_pred_all, residuals_rank, color='blue')
plt.axhline(y=0, color='red', linestyle='--')
plt.title('Residuals Plot for Rank Prediction')
plt.xlabel('Predicted Rank')
plt.ylabel('Residuals')
plt.grid(True)

for i, team in enumerate(df['team']):
    plt.text(y_rank_pred_all[i], residuals_rank[i], team, fontsize=8, ha='right')

plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['points'], y_points_pred_all, color='green', label='Predicted Points')
plt.plot([min(df['points']), max(df['points'])], [min(df['points']), max(df['points'])], color='red', lw=2, label='Perfect Prediction')
plt.title('Actual vs Predicted Points for All Teams')
plt.xlabel('Actual Points')
plt.ylabel('Predicted Points')
plt.legend()
plt.grid(True)

for i, team in enumerate(df['team']):
    plt.text(df['points'].iloc[i], y_points_pred_all[i], team, fontsize=8, ha='right')

plt.show()

residuals_points = df['points'] - y_points_pred_all
plt.figure(figsize=(10, 6))
plt.scatter(y_points_pred_all, residuals_points, color='green')
plt.axhline(y=0, color='red', linestyle='--')
plt.title('Residuals Plot for Points Prediction')
plt.xlabel('Predicted Points')
plt.ylabel('Residuals')
plt.grid(True)

for i, team in enumerate(df['team']):
    plt.text(y_points_pred_all[i], residuals_points[i], team, fontsize=8, ha='right')

plt.show()

plt.figure(figsize=(10, 6))
plt.hist(residuals_rank, bins=10, color='blue', edgecolor='black')
plt.title('Error Distribution for Rank Prediction')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(residuals_points, bins=10, color='green', edgecolor='black')
plt.title('Error Distribution for Points Prediction')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

"""# 2. **Using Random Forest:**"""

rf_model_rank = RandomForestRegressor(random_state=42)
rf_model_rank.fit(X_train, y_rank_train)

y_rank_pred_rf = rf_model_rank.predict(X_test)
mae_rank_rf = mean_absolute_error(y_rank_test, y_rank_pred_rf)
r2_rank_rf = r2_score(y_rank_test, y_rank_pred_rf)
cv_scores_rank = cross_val_score(rf_model_rank, X, y_rank, cv=5, scoring='neg_mean_absolute_error')

print(f"Random Forest - Rank Mean Absolute Error: {mae_rank_rf}")
print(f"Random Forest - Rank R²: {r2_rank_rf}")
print(f"Cross-Validated MAE for Rank Prediction: {-np.mean(cv_scores_rank)}")

rf_model_points = RandomForestRegressor(random_state=42)
rf_model_points.fit(X_train, y_points_train)

y_points_pred_rf = rf_model_points.predict(X_test)
mae_points_rf = mean_absolute_error(y_points_test, y_points_pred_rf)
r2_points_rf = r2_score(y_points_test, y_points_pred_rf)
cv_scores_points = cross_val_score(rf_model_points, X, y_points, cv=5, scoring='neg_mean_absolute_error')

print(f"Random Forest - Points Mean Absolute Error: {mae_points_rf}")
print(f"Random Forest - Points R²: {r2_points_rf}")
print(f"Cross-Validated MAE for Points Prediction: {-np.mean(cv_scores_points)}")

y_rank_pred_all = rf_model_rank.predict(X)
y_points_pred_all = rf_model_points.predict(X)

residuals_rank = df['rank'] - y_rank_pred_all
residuals_points = df['points'] - y_points_pred_all
residuals_rank_df = pd.DataFrame({'team': df['team'], 'rank_residuals': residuals_rank})
residuals_points_df = pd.DataFrame({'team': df['team'], 'points_residuals': residuals_points})
residuals_combined_df = pd.merge(residuals_rank_df, residuals_points_df, on='team')

print("Residuals for Rank:")
print(residuals_combined_df[['team', 'rank_residuals']].sort_values('rank_residuals', key=abs, ascending=False))

print("\nResiduals for Points:")
print(residuals_combined_df[['team', 'points_residuals']].sort_values('points_residuals', key=abs, ascending=False))

y_rank_pred_all_rf = rf_model_rank.predict(X)
y_points_pred_all_rf = rf_model_points.predict(X)
y_test_inverted = max(y_rank) + 1 - df['rank']
y_pred_inverted = max(y_rank) + 1 - y_rank_pred_all

plt.figure(figsize=(10, 6))
plt.scatter(y_test_inverted, y_pred_inverted, color='blue', label='Predicted Rank')  # Use inverted ranks for plotting
plt.plot([min(y_test_inverted), max(y_test_inverted)], [min(y_test_inverted), max(y_test_inverted)], color='red', lw=2, label='Perfect Prediction')
plt.title('Actual vs Predicted Rank for All Teams')
plt.xlabel('Actual Rank')
plt.ylabel('Predicted Rank (Inverted)')
plt.legend()
plt.grid(True)

for i, team in enumerate(df['team']):
    plt.text(y_test_inverted.iloc[i], y_pred_inverted[i], team, fontsize=8, ha='right')

plt.show()

residuals_rank_rf = df['rank'] - y_rank_pred_all_rf
plt.figure(figsize=(10, 6))
plt.scatter(y_rank_pred_all_rf, residuals_rank_rf, color='blue')
plt.axhline(y=0, color='red', linestyle='--')
plt.title('Residuals Plot for Rank Prediction (Random Forest)')
plt.xlabel('Predicted Rank')
plt.ylabel('Residuals')
plt.grid(True)

for i, team in enumerate(df['team']):
    plt.text(y_rank_pred_all_rf[i], residuals_rank_rf[i], team, fontsize=8, ha='right')

plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['points'], y_points_pred_all_rf, color='green', label='Predicted Points')
plt.plot([min(df['points']), max(df['points'])], [min(df['points']), max(df['points'])], color='red', lw=2, label='Perfect Prediction')
plt.title('Actual vs Predicted Points for All Teams (Random Forest)')
plt.xlabel('Actual Points')
plt.ylabel('Predicted Points')
plt.legend()
plt.grid(True)

for i, team in enumerate(df['team']):
    plt.text(df['points'].iloc[i], y_points_pred_all_rf[i], team, fontsize=8, ha='right')

plt.show()

residuals_points_rf = df['points'] - y_points_pred_all_rf
plt.figure(figsize=(10, 6))
plt.scatter(y_points_pred_all_rf, residuals_points_rf, color='green')
plt.axhline(y=0, color='red', linestyle='--')
plt.title('Residuals Plot for Points Prediction (Random Forest)')
plt.xlabel('Predicted Points')
plt.ylabel('Residuals')
plt.grid(True)

for i, team in enumerate(df['team']):
    plt.text(y_points_pred_all_rf[i], residuals_points_rf[i], team, fontsize=8, ha='right')

plt.show()

plt.figure(figsize=(10, 6))
plt.hist(residuals_rank_rf, bins=10, color='blue', edgecolor='black')
plt.title('Error Distribution for Rank Prediction (Random Forest)')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(residuals_points_rf, bins=10, color='green', edgecolor='black')
plt.title('Error Distribution for Points Prediction (Random Forest)')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

"""# **Rank and Points Predictions**"""

y_rank_pred_linear_all = linear_model_rank.predict(X)
y_points_pred_linear_all = np.round(linear_model_points.predict(X))

predictions_df_linear = pd.DataFrame({
    'team': df['team'],
    'actual_rank': df['rank'],
    'predicted_rank_linear': y_rank_pred_linear_all,
    'predicted_points_linear': y_points_pred_linear_all,
})

print('Predictions Using Linear Regression:\n\n', predictions_df_linear)

y_rank_pred_rf_all = rf_model_rank.predict(X)
y_points_pred_rf_all = np.round(rf_model_points.predict(X))

predictions_df_rf = pd.DataFrame({
    'team': df['team'],
    'actual_rank': df['rank'],
    'predicted_rank_rf': y_rank_pred_rf_all,
    'predicted_points_rf': y_points_pred_rf_all,
})

print('Predictions Using Random Forest Regression:\n\n', predictions_df_rf)

residuals_linear = y_rank_pred_linear_all - df['rank']
residuals_rf = y_rank_pred_rf_all - df['rank']

residuals_df_linear = pd.DataFrame({'team': df['team'], 'residuals': residuals_linear})
residuals_df_rf = pd.DataFrame({'team': df['team'], 'residuals': residuals_rf})

top_5_linear = residuals_df_linear.loc[residuals_df_linear['residuals'].abs().nlargest(5).index]
top_5_rf = residuals_df_rf.loc[residuals_df_rf['residuals'].abs().nlargest(5).index]

plt.figure(figsize=(12, 6))
plt.barh(top_5_linear['team'], top_5_linear['residuals'], color='skyblue')
plt.axvline(0, color='red', linestyle='--')
plt.title('Top 5 Teams with Highest Residuals (Linear Regression)')
plt.xlabel('Residuals')
plt.ylabel('Teams')
plt.grid(axis='x')
plt.show()

plt.figure(figsize=(12, 6))
plt.barh(top_5_rf['team'], top_5_rf['residuals'], color='lightgreen')
plt.axvline(0, color='red', linestyle='--')
plt.title('Top 5 Teams with Highest Residuals (Random Forest)')
plt.xlabel('Residuals')
plt.ylabel('Teams')
plt.grid(axis='x')
plt.show()