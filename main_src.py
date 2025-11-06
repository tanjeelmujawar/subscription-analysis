# --------------------------------------------
# Subscription Analysis Project
# Author: Tanjeel Mujawar
# Description:
#   This script cleans the data, explores it,
#   creates graphs, and calculates important insights.
# --------------------------------------------


# Importing required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Load the dataset
df = pd.read_csv(r"D:\Maven_dataset\Subscription Cohort Analysis Data.csv")

# Fix date formats for created_date and canceled_date
df['created_date'] = pd.to_datetime(df['created_date'], dayfirst=True, errors='coerce')
df['canceled_date'] = pd.to_datetime(df['canceled_date'], dayfirst=True, errors='coerce')

# Create a column to check if customer canceled or not
df['is_canceled'] = df['canceled_date'].notnull()

# Calculate customer lifetime
df['customer_lifetime'] = (df['canceled_date'] - df['created_date']).dt.days

# Print basic stats
print("Average Subscription Cost:", df['subscription_cost'].mean())
print("Median Subscription Cost:", df['subscription_cost'].median())
print("Most Common Interval:", df['subscription_interval'].mode()[0])
print("Total Revenue Collected: $", df['subscription_cost'].sum())
print("Total Customers:", df['customer_id'].nunique())


# Count of canceled vs active customers
cancel_counts = df['is_canceled'].value_counts()
print("\nCanceled vs Active Customers:")
print(cancel_counts)

# Count of canceled vs active customers
cancel_counts = df['is_canceled'].value_counts()
print("Canceled Subscriptions:", cancel_counts[True])
print("Active Subscriptions:", cancel_counts[False])


# Graph: Active vs Canceled Customers
cancel_counts.plot(kind='bar', color=['green','red'])
plt.title('Active vs Canceled Subscriptions')
plt.xlabel('Status (False = Active, True = Canceled)')
plt.ylabel('Number of Customers')
plt.show()

# Calculate the Cancel Rate
cancel_rate = (cancel_counts[True] / cancel_counts.sum()) * 100
print(f"Cancellation Rate: {cancel_rate:.2f}%")

# Total Revenue by Interval
interval_revenue = df.groupby('subscription_interval')['subscription_cost'].sum()
print(interval_revenue)

# Plot the line graph of monthly New Subscription
df['created_month'] = df['created_date'].dt.to_period('M')
monthly_new = df.groupby('created_month')['customer_id'].count()
monthly_new.plot(kind='line', marker='o')
plt.title('Monthly New Subscriptions')
plt.xlabel('Month')
plt.ylabel('Number of New Customers')
plt.show()

# PLot the graph of Customer Lifetime Distribution
sns.histplot(df['customer_lifetime'], bins=20, kde=True)
plt.title('Customer Lifetime Distribution')
plt.xlabel('Lifetime (days)')
plt.show()

# Calculate the Churn Rate.
total_customers = df['customer_id'].nunique()
canceled_customers = df[df['is_canceled'] == True]['customer_id'].nunique()
churn_rate = (canceled_customers / total_customers) * 100
print(f"Churn Rate: {churn_rate:.2f}%")

# Calculate the Average Lifespan of a customer.
average_lifetime = df['customer_lifetime'].mean()
median_lifetime = df['customer_lifetime'].median()
print(f"Average Lifetime: {average_lifetime:.0f} days")
print(f"Median Lifetime: {median_lifetime:.0f} days")

# Calculate the Total Revenue.
total_revenue = df['subscription_cost'].sum()
avg_revenue_per_customer = df['subscription_cost'].mean()
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Average Revenue per Customer: ${avg_revenue_per_customer:.2f}")