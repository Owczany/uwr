import math

# Udowodnie przez całkowanie przez części
# In = ∫ x^n / x + 2024 = ∫ x^(n-1) * (x + 2024 - 2024) / (x + 2024) = ∫ x^(n-1) * (1 - 2024 / (x + 2024)) = ∫ x^(n-1) - 2024 * x^(n-1) / (x + 2024) = 1 / n 

In = [math.log(2025/2024)] 

for i in range(1, 21):
    In.append(1/i - 2024 * In[i - 1])
    
for i in range(1, 21, 2):
    print(f'n = {i}')
    print(In[i])
    
for i in range(2, 21, 2):
    print(f'n = {i}')
    print(In[i])
    