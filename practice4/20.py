import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    
    m = int(data[0])
    g, n = 0, 0
    
    for i in range(1, 2 * m, 2):
        scope = data[i]
        val = int(data[i+1])
        
        if scope == "global":
            g += val
        elif scope == "nonlocal":
            n += val
            
    print(g, n)

if __name__ == "__main__":
    solve()