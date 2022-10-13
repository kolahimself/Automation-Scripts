def geometry_check(treads, risers):
    """
    Checks that the geometry of the flight is proportioned to be comfortable, 
    and that it meets accessibiility standards 
    
    The checks are:
    
    (a) Treads should be at least 250mm, exclusive of nosing.
    (b)  Risers less than 100mm and more than 200mm high should not be used
    """
    
    if treads < 250:
        print('Tread length is lower than 250mm, adjust if possible.')
        alert = 1
        return alert
    
    if risers < 100 and risers > 200:
        print('Step risers are not bad for use, adjust if possible.')
        alert = 1
        return alert
      
    
    def flight_request(uneven_treads=False):
    """
    Requests for the necessary dimensions and attributes for a stair flight
    & sorts them into a dictionary.
    
    Should there be any case of unequal/nonuniform length of treads in the stair flight, 
    set `uneven_treads` to True
    """
    
    # Case for equal and unequal tread lengths along a stair flight
    if uneven_treads == True:
        # unequal tread lengths
        tread = float(input('Supply a typical tread/going length in mm: '))
        span = float(input('Supply the total horizontal length of the stair flight in mm: '))
    else:
        # equal tread lengths
        tread = float(input('Supply the length of the flight tread in mm: '))
        no = float(input('Supply the no of treads along this stair flight: '))
        span = no * tread
    
    # vertical face of a step
    riser = float(input('Supply the height of the step riser mm: '))
    
    # elevation
    elevation = float(input('Supply the elevation of the stair flight in mm: '))
    
    # waist 
    waist = float(input('Supply the waist thickness of the stair flight in mm: '))
    
    # finishes
    finishes = float(input('Supply extra dead load finishes on the stair flight in kN/m2: '))
    
    # imposed
    imposed_load = float(input('Supply the value of imposed load in kN/m2: '))
    
    # Run geometry check
    gc = geometry_check(tread, riser)
    if gc != 1:
        print('Stair Flight has passed Geometry Check!')
        
        # Flight attributes to be passed in a class instance
        attributes = {
            'tread': tread,
            'span': span,
            'riser': riser,
            'elevation': elevation,
            'waist': waist,
            'finishes': finishes,
            'imposed_load': imposed_load
        }
    
    else:
        print('Adjust stair dimensions with a sense of safety and ease. Ty')
    
    return attributes
  
  
  class Flight:
    """ A stair flight is an important component in stair cases.
    
    This class records previously defiend attrivutes from a dictionary and
    calculates the total dead, live and ultimate limit state loads according to EC2
    """
    
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
    
    def load(self):
        # Evaluate the total loading of the stair flight based on the supplied attributes
        # & design guidelines (EC2)
        # loads are returned in the format: (Total Dead load, Total Imposed Load, Total load at ULS)
        
        self_weight = mm_to_m(self.waist) * 25  # normal to the inclination in kN/m2
        stepped_area = 0.5 * mm_to_m(self.waist) * 25 # global vertical direciton
        
        # the angle of inclination of the flight area to the horizontal
        slope_factor = np.degrees(np.arctan(self.elevation/self.span)) 
        
        # UDL from waist of the stair flight in the global direction
        waist_udl = self_weight * np.cos(np.radians(slope_factor))
        
        # Total Dead Load
        gk = waist_udl + stepped_area + self.finishes
        # Total live/imposed load
        qk = self.imposed_load
        
        # load on the flight at ultimatye limit state
        n = (1.35 * gk) + (1.5 * qk)
        
        return gk, qk, n
      
   
  class Landing:
    """
    A stair landing is a slab designed orthogonically to the stair flight,
    
    This class records the span(length of main direction in mm),
    the thickness of the slab in mm,
    extra finishes in kN/m2 and imposed load on the slab in kN/m2 all in a list called slab_details
    """
    
    def __init__(self, slab_details):
        self.slab_details = slab_details
        
    def load(self):
        gk = (mm_to_m(self.slab_details[1]) * 25) + self.slab_details[2]
        qk = self.slab_details[3]
        
        # load at ultimate limit state
        n = (1.35 * gk) + (1.5 * qk)
        
        return gk, qk, n
   
  
