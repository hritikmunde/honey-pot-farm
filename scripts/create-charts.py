#!/usr/bin/env python3
import matplotlib.pyplot as plt
from collections import Counter

# Top passwords across all honeypots
passwords = {
    '123456': 70,
    '123': 15,
    'password': 11,
    'abc123': 8,
    'admin': 7,
    'root': 6,
    '123456789': 5,
    'postgres': 4,
    '1qazXSW@': 4,
    'pass': 5
}

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(passwords.keys(), passwords.values(), color='steelblue')
plt.xlabel('Password', fontsize=12)
plt.ylabel('Attempts', fontsize=12)
plt.title('Top 10 Passwords Attempted Across All Honeypots', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_passwords.png', dpi=300)
print("✓ Created top_passwords.png")

# Attack distribution
honeypots = ['Edge Router', 'Domain Controller', 'Web Server']
attempts = [386, 149, 16]

plt.figure(figsize=(8, 8))
plt.pie(attempts, labels=honeypots, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Login Attempts by Honeypot Type', fontsize=14)
plt.savefig('attack_distribution.png', dpi=300)
print("✓ Created attack_distribution.png")

print("\n✅ Charts created for your report!")