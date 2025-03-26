# Getting input data
num = input()

# Main function
def solution(num):
    n = len(num)
    
    # Checking for 0 or 8
    for i in range(n):
        if int(num[i]) % 8 == 0:
            print("YES")
            print(num[i])
            return
        
        # Checking for 2-digit number that can be divided by 8
        for j in range(i+1, n):
            if int(num[i] + num[j]) % 8 == 0:
                print("YES")
                print(num[i] + num[j])
                return
            
            # Checking for 3-digit number that can be divided by 8
            for k in range(j+1, n):
                if int(num[i] + num[j] + num[k]) % 8 == 0:
                    print("YES")
                    print(num[i] + num[j] + num[k])
                    return
    
    print("NO")

solution(num)
