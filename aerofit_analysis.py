import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

# Set the style for better visualizations
plt.style.use('seaborn')
sns.set_palette("husl")

# Read the data
df = pd.read_csv('aerofit_treadmill_data.csv')

# 1. Basic Data Analysis
print("\n=== Basic Data Overview ===")
print(df.info())
print("\nSummary Statistics:")
print(df.describe())

# 2. Customer Demographics by Product
print("\n=== Customer Demographics by Product ===")

# Average metrics by product
demographics = df.groupby('Product').agg({
    'Age': 'mean',
    'Education': 'mean',
    'Income': 'mean',
    'Usage': 'mean',
    'Fitness': 'mean',
    'Miles': 'mean'
}).round(2)

print("\nAverage Customer Metrics by Product:")
print(demographics)

# 3. Visualizations

# Create a figure with subplots
plt.figure(figsize=(15, 10))

# Age Distribution by Product
plt.subplot(2, 2, 1)
sns.boxplot(x='Product', y='Age', data=df)
plt.title('Age Distribution by Product')

# Income Distribution by Product
plt.subplot(2, 2, 2)
sns.boxplot(x='Product', y='Income', data=df)
plt.title('Income Distribution by Product')

# Fitness Level by Product
plt.subplot(2, 2, 3)
sns.boxplot(x='Product', y='Fitness', data=df)
plt.title('Fitness Level by Product')

# Usage by Product
plt.subplot(2, 2, 4)
sns.boxplot(x='Product', y='Usage', data=df)
plt.title('Weekly Usage by Product')

plt.tight_layout()
plt.savefig('product_distributions.png')
plt.close()

# Gender Distribution
plt.figure(figsize=(10, 6))
gender_product = pd.crosstab(df['Product'], df['Gender'], normalize='index') * 100
gender_product.plot(kind='bar', stacked=True)
plt.title('Gender Distribution by Product (%)')
plt.ylabel('Percentage')
plt.tight_layout()
plt.savefig('gender_distribution.png')
plt.close()

# 4. Contingency Tables and Chi-Square Tests
print("\n=== Contingency Tables and Statistical Tests ===")

# Product vs Gender
gender_table = pd.crosstab(df['Product'], df['Gender'])
print("\nProduct vs Gender Contingency Table:")
print(gender_table)
chi2, p_value = stats.chi2_contingency(gender_table)[:2]
print(f"Chi-square p-value: {p_value:.4f}")

# Product vs MaritalStatus
marital_table = pd.crosstab(df['Product'], df['MaritalStatus'])
print("\nProduct vs Marital Status Contingency Table:")
print(marital_table)
chi2, p_value = stats.chi2_contingency(marital_table)[:2]
print(f"Chi-square p-value: {p_value:.4f}")

# 5. Correlation Analysis
print("\n=== Correlation Analysis ===")
numeric_cols = ['Age', 'Education', 'Usage', 'Fitness', 'Income', 'Miles']
correlation = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix of Numeric Variables')
plt.tight_layout()
plt.savefig('correlation_matrix.png')
plt.close()

# 6. Product Profiles
print("\n=== Product Profiles ===")
for product in df['Product'].unique():
    product_data = df[df['Product'] == product]
    print(f"\nProfile for {product}:")
    print(f"Average Age: {product_data['Age'].mean():.1f} years")
    print(f"Average Income: ${product_data['Income'].mean():,.2f}")
    print(f"Average Fitness Level: {product_data['Fitness'].mean():.1f}")
    print(f"Average Weekly Usage: {product_data['Usage'].mean():.1f} times")
    print(f"Average Weekly Miles: {product_data['Miles'].mean():.1f}")
    print(f"Gender Split: {(product_data['Gender'].value_counts(normalize=True) * 100).round(1).to_dict()}")
