import gdspy
import numpy

gdspy.current_library = gdspy.GdsLibrary()

lib = gdspy.GdsLibrary()

lib_name ="spirals2.gds"


radius = 50

wg_width = 0.6

shift = 20

    
x1p = {"layer": 2, "datatype": 0}
x = {"layer": 5, "datatype": 0}


def spiral(turns, wg_width, length, height):

    path = gdspy.Path(wg_width, (0, 0))
    path.segment(radius, "+x", **x1p) 
    
    h = height
    l = length
    lenght_counter = 0
    
    for n in range(turns):
        
        path.segment(l, "+x", **x1p)
        path.turn(radius, "l", **x1p)
        
        l = l - shift
        
        path.segment(h, "+y", **x1p)
        path.turn(radius, "l", **x1p) 
        
        h = h - shift
        
        path.segment(l, "-x", **x1p)
        path.turn(radius, "l", **x1p) 
        
        l = l - shift
        
        path.segment(h, "-y", **x1p)
        path.turn(radius, "l", **x1p)
        
        h = h - shift
      
        lenght_counter += 2*(l + h) + 6*shift + 4*numpy.pi*radius/2
        # print(lenght_counter)
      
        
    path.segment((l-2*radius)/2, "+x", **x1p)
    path.turn(radius, "l", **x1p)
    path.segment(h, "+y", **x1p)
    path.turn(radius, "r", **x1p)
    path.segment((l-2*radius)/2, "+x", **x1p)
    path.turn(radius, "r", **x1p)

    lenght_counter += (l-2*radius) + h + 4*numpy.pi*radius/2

    
    h = h + shift/2
    l = l + shift/2
    
    path.segment(h, "-y", **x1p)
    path.turn(radius, "r", **x1p)
    
    h = h + shift*1.5
    
    path.segment(l, "-x", **x1p)
    path.turn(radius, "r", **x1p)
    
    l = l + shift*1.5
    
    
    path.segment(h, "+y", **x1p)
    path.turn(radius, "r", **x1p) 
    
    h = h + shift
    
    path.segment(l, "+x", **x1p) 
    l = l + shift
    
    lenght_counter += 2*(l + h) - 6*shift + 4*numpy.pi*radius/2
    
    
    for n in range(turns-1):
        
        path.turn(radius, "r", **x1p) 
        
        path.segment(h, "-y", **x1p)
        path.turn(radius, "r", **x1p)
        
        h = h + shift
        
        path.segment(l, "-x", **x1p)
        path.turn(radius, "r", **x1p)
        
        l = l + shift
        
        path.segment(h, "+y", **x1p)
        path.turn(radius, "r", **x1p) 
        
        h = h + shift
        
        path.segment(l, "+x", **x1p)      
        l = l + shift
        
        lenght_counter += 2*(l + h) - 6*shift + 4*numpy.pi*radius/2
         
    
    path.turn(radius, "r", **x1p) 
    
    path.segment(h-shift/2, "-y", **x1p)
    path.turn(radius, "l", **x1p)
    
    # path.segment(radius, "+x", **x1p)
    # print("Spiral ", turns, " turns, l=" , length, "h= ",  height, ", has L = ", round(lenght_counter*1e-3))
    print("turns=", turns,  "length=", round(l), "L = ", round(lenght_counter*1e-6,3))

    
    return path


height = 500

path = spiral(20, wg_width, 500, height)
spiral_cell = lib.new_cell('Spiral_' + str(1))
spiral_cell.add(path)
lib.add(spiral_cell)

path = spiral(25, wg_width, 1500, height)
spiral_cell = lib.new_cell('Spiral_' + str(2))
spiral_cell.add(path)
lib.add(spiral_cell)

path = spiral(25, wg_width, 3500, height) # 
spiral_cell = lib.new_cell('Spiral_' + str(3))
spiral_cell.add(path)
lib.add(spiral_cell)

path = spiral(12, wg_width, 2100, height) #
spiral_cell = lib.new_cell('Spiral_' + str(4))
spiral_cell.add(path)
lib.add(spiral_cell)



gdspy.LayoutViewer()

lib.write_gds(lib_name)