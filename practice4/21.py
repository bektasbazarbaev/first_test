import importlib
import sys

def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    q = int(input_data[0])
    for i in range(1, q + 1):
        path, attr = input_data[i].split()
        
        try:
            module = importlib.import_module(path)
            if hasattr(module, attr):
                obj = getattr(module, attr)
                if callable(obj):
                    print("CALLABLE")
                else:
                    print("VALUE")
            else:
                print("ATTRIBUTE_NOT_FOUND")
        except ImportError:
            print("MODULE_NOT_FOUND")

if __name__ == "__main__":
    solve()