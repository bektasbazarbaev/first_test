a = int(input())
arr = list(map(int, input().split()))

freq = {} 

for num in arr:
    if num in freq:       
        freq[num] += 1    
    else:                
        freq[num] = 1     

max_count = max(freq.values()) 
candidates = []

for num, count in freq.items():  
    if count == max_count:      
        candidates.append(num)  

result = min(candidates)       
print(result)
