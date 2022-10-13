def mm_to_m(val, flip=False):
    """Converts input value from millimeters to meters
        
    Set flip to 'True' if you intend to convert from meters to millimeters
    """
    if flip is False:
        return val/1000
    else: 
        return val * 1000
   
  
  
  def area_spacing(bar_size, area_required):
    """Determines the bar spacing (area provided) from area of steel required

    Bar size: The required bar size
    Area Required: The area required derived from design calculations
    """
    # Standard bar sizes
    bars = [8, 10, 12, 16, 20, 25, 32, 40]
    
    # Areas for bar spacing as used in Eurocodes
    areas = np.array([
        [503, 402, 335, 287, 252, 223, 201, 182, 168],
        [785, 628, 523, 449, 393, 349, 314, 285, 262],
        [1130, 905, 754, 646, 566, 502, 452, 411, 377],
        [2010, 1610, 1340, 1150, 1010, 893, 804, 731, 670],
        [3140, 2510, 2090, 1800, 1570, 1396, 1260, 1142, 1050],
        [4910, 3930, 3270, 2810, 2450, 2181, 1960, 1784, 1640],
        [np.nan , 6430, 5360, 4600, 4020, 3574, 3220, 2924, 2680],
        [np.nan, np.nan, 8380, 7180, 6280, 5585, 5030, 4569, 4190]
    ])
    
    
    # Bar centre-to-centre spacing
    spacing = [100, 125, 150, 175, 200, 225, 250, 275, 300]
    
    if bar_size in bars:
        idx = bars.index(bar_size)
        pass
    else:
        print('Area spacing cannot be determined due to the bar size supplied.')
    
    # Determine area provided
    area_provided = np.min(areas[idx][np.where(areas[idx] >= area_required)])
    
    # Determine spacing
    i = list(areas[idx]).index(area_provided)
    bar_spacing = spacing[i]
    
    return area_provided, bar_spacing
