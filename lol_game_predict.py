import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load the CSV file
df = pd.read_csv('games.csv')
# print("Loaded CSV columns:", df.columns)

# Load the champion data from JSON
with open('champion_info.json') as f:
    champ_data = json.load(f)

# Map champion IDs to names for both teams
for i in range(1, 6):
    df[f't1_champ{i}'] = df[f't1_champ{i}id'].apply(lambda x: champ_data['data'][str(x)]['name'])
    df[f't2_champ{i}'] = df[f't2_champ{i}id'].apply(lambda x: champ_data['data'][str(x)]['name'])

# Keep necessary columns
df = df[['t1_champ1', 't1_champ2', 't1_champ3', 't1_champ4', 't1_champ5', 
         't2_champ1', 't2_champ2', 't2_champ3', 't2_champ4', 't2_champ5', 
         'firstDragon', 'firstBlood', 'firstTower', 'firstBaron', 'winner']]

# Encode champion names
encodings1 = [pd.get_dummies(df[col], prefix=f't1_{col}') for col in ['t1_champ1', 't1_champ2', 't1_champ3', 't1_champ4', 't1_champ5']]
encodings2 = [pd.get_dummies(df[col], prefix=f't2_{col}') for col in ['t2_champ1', 't2_champ2', 't2_champ3', 't2_champ4', 't2_champ5']]

# Combine encoded data
combined_df1 = pd.concat(encodings1, axis=1)
combined_df2 = pd.concat(encodings2, axis=1)

# Join the encodings with the original data
df = df.join(combined_df1).join(combined_df2)

# Drop original champion columns
df = df.drop(['t1_champ1', 't1_champ2', 't1_champ3', 't1_champ4', 't1_champ5', 
              't2_champ1', 't2_champ2', 't2_champ3', 't2_champ4', 't2_champ5'], axis=1)

# Separate features and target
X, y = df.drop('winner', axis=1), df['winner']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
clf = RandomForestClassifier(n_jobs=-1, random_state=42)
clf.fit(X_train, y_train)

# Evaluate the model
print("Model Accuracy:", clf.score(X_test, y_test))

# Feature importance
importances = dict(zip(X.columns, clf.feature_importances_))
sorted_importances = sorted(importances.items(), key=lambda x: x[1], reverse=True)
# print("Feature Importances:", sorted_importances[:10])

# Calculate champion win rates
champ_name = input('Enter a champion name: ')

# Test Team 1
wins1 = len(df[(df.filter(like='t1_').filter(like=champ_name) == 1).any(axis=1) & (df['winner'] == 1)])
picks1 = len(df[(df.filter(like='t1_').filter(like=champ_name) == 1).any(axis=1)])
print(f"Team 1: Wins={wins1}, Picks={picks1}")

# Test Team 2
wins2 = len(df[(df.filter(like='t2_').filter(like=champ_name) == 1).any(axis=1) & (df['winner'] == 2)])
picks2 = len(df[(df.filter(like='t2_').filter(like=champ_name) == 1).any(axis=1)])
print(f"Team 2: Wins={wins2}, Picks={picks2}")

win_rate = (wins1 + wins2) / (picks1 + picks2) if (picks1 + picks2) > 0 else 0
# print(f"Win Rate for Tristana: {win_rate_tristana}")
print(f"Win Rate for {champ_name}: {win_rate}")
