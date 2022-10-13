def flexure_designer(moment: float, bar_size: list, fck: float, fy: float, struct_object, cover=25):
    """Performs flexural design of landing or slab, prints errors if supplied members fail,
       returns rebar results if adequate.
       
    Parameters:
        moment: (float) Design moment as determined by sturctural analysis in kNm
        bar_size: (list) Preferred bar sizes for the main and distribution bars e.g [12, 10]
        fck: (float) Desired concrete grade in MPa
        fy: (float) Desired high yield steel grade in MPa
        cover: (float) Concrete cover in mm, default is 25mm
        struct_object: Defined structural object from class Flight & Landing
        
    Returns: area_provided, area_required
    area_provided: Area of Main Bars Provided in mm2/m from table
    area_required: Calculated area of main bars from structural design
    """
    
    # determine effective depth, d
    # for stair flights
    if type(struct_object) is Flight:
        d = struct_object.waist - cover - bar_size[0]/2 - 10
    else:
        d = struct_object.slab_details[1] - cover - bar_size[0]/2 - 10
    
    # determine k, (from EC2 -> k = M_ed/fck.b.d^2)
    k = (moment * 1000000)/(fck * 1000 * np.square(d))
    
    if k < 0.167:
        pass
    else:
        
        # For double reinforced sections
        print('Compression reinforcement is required')
        m_rd = 0.167 * fck * 1000 * np.square(d)
        
        # Area of compression reinforcements
        d2 = cover - bar_size[0] - 10
        area_comp = (moment - m_rd) * 1000000/(0.87 * fy * (d-d2))
        
        # Area of tension reinforcements
        z = d * (0.5 + np.sqrt(0.25 - (0.882 * 0.167)))
        area_tension = (m_rd * 1000000/(0.87 * fy * z)) + area_comp
        
        # determine area of bar spacing for compresison bars
        comp_area, comp_spacing = area_spacing(area_required=area_tension, bar_size=bar_size[0])
        print(f'Provide Y{bar_size[0]} @ {comp_spacing}mm C/C bottom ({comp_area}mm2)')
        
        # Distribution bars
        dist_min = (0.0013 * 1000 * (d-d2))
        dist1, dist2 = area_spacing(bar_size[1], dist_min)
        print(f'Provide Y{bar_size[1]} @ {dist2}mm C/C distribution bars')
        
        return comp_area, area_tension
        
    # determine lever arm z
    z = d * (0.5 + np.sqrt(0.25 - (0.882 * k)))
    
    # determine area of steel for bottom bars
    area_s1 = (moment * 1000000)/(0.87 * fy * z)
    
    # Determine area of bar spacing for bottom reinforcements
    area_provided, bar_spacing = area_spacing(area_required=area_s1, bar_size=bar_size[0])
    
    # Distribution reinforcements
    fctm = 0.3 * np.power(fck, (2/3))
    a_smin = 0.26 * (fctm/fy) * 1000 * d
    dist_prov, dist_spacing = area_spacing(area_required=a_smin, bar_size=bar_size[1])
    
    if a_smin > (0.0013 * 1000 * d):
        
        # Print Design Results (Reinforcement bar selections and proportions)
        print(f'Provide Y{bar_size[0]} @ {bar_spacing}mm C/C bottom ({area_provided}mm2)')
        print(f'Provide Y{bar_size[1]} @ {dist_spacing}mm C/C distribution bars')
        return area_provided, area_s1
    
    else:
        print('The provided distribution reinforcement is inadequate')
     
    
    def deflection_check(span_eff, area_required, area_provided, fck, fyk, struct_obj, comp_area=None):
    """Performs Deflection Check on the stair flight or landing.
    
    Parameters:
        span_eff: Effective span of the stair flight in mm
        area_required: Area of steel required as supplied by flexure designer
        area_provided:  Area of steel provided as supllied by flexure designer
        fck: Concrete grade in MPa
        fyk: Steel grade in MPa
        struct_obj: Defined structural object from class Flight or Landing
        comp_area: Defaults to `None`, set to desired value if compression reinforcements are required
    """
    
    # determine effective depth, d
    # for stair flights
    if type(struct_obj) is Flight:
        d = struct_obj.waist - 25 - 12/2 - 10
    else:
        d = struct_obj.slab_details[1] - 25 - 12/2 - 10
    
    # for simply supported beams and slab according to EC2
    K = 1.0
    
    # tension reinforcement ratio to resist moment due to design load
    rho = area_provided/ (1000 * d)
    
    # reference reinforcement ratio 
    rho_not = 0.001 * np.sqrt(fck)
    
    # compresion reinforcement ratio
    if comp_area == None:
        rho_prime = 0
        pass 
    else:
        rho_prime = comp_area/ (1000 * d)
        
    # The limiting basic span/ effective depth ratio 
    # tension rebar ratio check
    if rho <= rho_not:
        sd_ratio = (11 
                    + (1.5 * np.sqrt(fck) * (rho_not/rho))
                    + ((1/12) * np.sqrt(fck)
                       * np.power((rho_not/rho) - 1, 3/2))
                   ) * K
        
    else: 
        sd_ratio = (11 
                    + (1.5 * np.sqrt(fck) * (rho_not/(rho - rho_prime)))
                    + (3.2 * np.sqrt(fck)
                       * np.power((rho_not/rho), 1/2))
                   ) * K
    
    # modification factor
    sigma = (310 * fyk * area_required) / (500 * area_provided)
    mod_factor = 310/sigma
    
    # allowable span to depth ratio
    allowable_sd = mod_factor * sd_ratio
    
    # actual deflection L/d
    actual_deflection = span_eff/d
    
    # Deflection Check
    if actual_deflection < allowable_sd:
        print('This Stair Structure has passed for deflection ✅')
        
    else:
        print(f'The structure has failed due to deflection, {np.round(actual_deflection, 3)} < {np.round(allowable_sd, 3)}')
     
    
    def shear_check(v_ed, area_required, fck, struct_obj, ac, fcd, ned=0):
    """Performs a shear check on the stair structure,
    
    Parameters: 
        v_ed: Ultimate shear force in kN
        area_required: Area of steel required as supplied by flexure designer
        fck: Concrete grade in MPa
        struct_obj: Defined structural object from class Flight or Landing
        ac: Cross sectional area of the concrete
        fcd: design compressive strength of the concrete
        ned: Net axial force at the section, check for this in the analysis. If absent, it defaults to 0
        
    """
    # determine effective depth, d
    # for stair flights
    if type(struct_obj) is Flight:
        d = struct_obj.waist - 25 - 12/2 - 10
    else:
        d = struct_obj.slab_details[1] - 25 - 12/2 - 10
    
    c_rdc = 0.18/1.5
    k = 1 + np.sqrt(200/d)
    
    # check for k
    if k > 2:
        k = 2
    else:
        pass
    
    # detemrine V_minimum
    v_min = 0.035 * np.power(k, 3/2) * np.power(fck, 1/2)
    k1 = 0.15
    
    rho = area_required/(1000 * d)
    sigma = ned/ac
    if sigma > (0.2 * fcd):
        print('Axial forces and compressive strengths do not pass design checks')
    else:
        pass
    
    # the concrete resistance shear stress without shear reinforcement
    v_rdc = (c_rdc * k 
             * np.power((100 * rho * fck), 1/3)
             + (k1 * sigma)) * 1000 * d
    
    # check for shear reinforcements
    if v_rdc > (v_ed + (k1 * sigma)):
        print('Shear Reinforcements are not required, shear is OK✅')
    else:
        print('Shear Reinforcements are needed')
