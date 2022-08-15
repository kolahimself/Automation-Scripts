import numpy as np

def calculator(Ws, bearing_capacity):
    
    Pb = bearing_capacity * 1.35
    A_req = (1.1 * Ws)/Pb
    
    return A_req * 1000000

def footing_emulator(req):
    
    area = [640000, 1000000, 1440000, 1960000, 2560000, 3240000, 4000000]
    sizes = [800, 1000, 1200, 1400, 1600, 1800, 2000]
    
    reqs = list(filter(lambda x: x > req, area))
    final = min(reqs)
    index = area.index(final)
    l = sizes[index]
    
    print(f"Pad Base Dimension can be: {l}mm by {l}mm")
  
 def main():
    
    Ws = float(input('Input W at ultimate limit state (kN): '))
    bearing_capacity = float(('Input the soil bearing capacity: '))
    
    size = calculator(Ws, bearing_capacity)
    
    footing_emulator(size)

main()
