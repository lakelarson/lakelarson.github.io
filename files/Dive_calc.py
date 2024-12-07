import matplotlib.pyplot as plt


# ________________________________________________________ #
# ____________________ ASK FOR INPUTS ____________________ #

# The "while true" statements are used to stay in a loop until a number within the range is entered

# A standard air tank, when full, has a psi reading of 3000 psi. For this calculation, our diver 
#   will be using such a tank, but it may not be completetly full when they start their dive.
while True:
    psi_initial = input('____________________\nPlease enter the initial psi in your tank (max is 3000 psi): ')

    try: # Confirm that input is a float value
        psi_initial = round(float(psi_initial), 2)

        if psi_initial >0 and psi_initial <=3000: # Confirm value is within specified range
            break
        else:
            print(f'Please enter a value between 3000 and 0.\n')  
    except:
        print(f'Please enter a number (do not include units in your response).\n')

# Surface Air Consumption rate, or SAC, is a measurement of how much air a diver consumes at surface level. 
#   For most divers this rate should be around 30 psi/min.
while True:
    s_a_c = input('____________________\nPlease enter your surface air consumption rate (max is 60 psi/min): ')

    try: # Confirm that input is a float value
        s_a_c = round(float(s_a_c), 2)
        
        if s_a_c >0 and s_a_c <=60: # Confirm value is within specified range
            break
        else:
            print(f'Please enter a value between 60 and 0.\n')
    except:
        print(f'Please enter a number (do not include units in your response).\n')

# Pretty self-explanatory. What depth do you want to explore at?
while True:
    depth = input('____________________\nPlease enter the depth you would like to dive to (max is 200 ft): ') 

    try: # Confirm that input is a float value
        depth = round(float(depth), 2)
        
        if depth >0 and depth <=200: # Confirm value is within specified range
            break
        else:
            print(f'Please enter a value between 200 and 0.\n')        
    except:
        print(f'Please enter a number (do not include units in your response).\n')

# The US Navy recommends a max descent rate of 75 ft/min to avoid blackout, narcosis, and other pressure-related issues on the way down.
while True:
    descent_rate = input('____________________\nPlease enter how fast you will be descending (max is 75 ft/min): ')  

    try: # Confirm that input is a float value
        descent_rate = round(float(descent_rate), 2)
        
        if descent_rate >0 and descent_rate <=75: # Confirm value is within specified range
            break
        else:
            print(f'Please enter a value between 75 and 0.\n')             
    except:
        print(f'Please enter a number (do not include units in your response).\n')

#We want to save 1/3 of our tank for emergencies, so we will not include it in our calculations.
reserve_psi = round(psi_initial * (1/3), 2)
usable_psi = psi_initial - reserve_psi 


ascent_rate = 33 # About 33 ft/min is the optimal ascension rate, as outlined by the Professional Association of Diving Instructors

decompression_time = 0 # How long you need to decompress for. If you dive deep enough, time will be added (3 minutes is recommended)
decompression_depth = 16 # The depth at which you need to stop and decompress, if you dive deep enough (16 feet is recommended)

# Y VALUES
descent_air_values = []
exploration_air_values = []
initial_ascent_air_values = []
decompression_air_values = []
final_ascent_air_values = []
total_air_values = []

# X VALUES
descent_time_intervals = []
exploration_time_intervals = []
initial_ascent_time_intervals = []
decompression_time_intervals = []
final_ascent_time_intervals = []
total_time_intervals = []

# THE UNTOUCHABLES
descent_air = 0
exploration_air = 0
initial_ascent_air = 0
decompression_air = 0
final_ascent_air = 0


# ________________________________________________________________ #
# ____________________| FUNCTION DEFINITIONS |____________________ #

# These time iterators are used to create
def descent_time_iterator(depth, rate):
    time_elapsed = (depth / rate) * 60
    i = 1
    j = 1
    while j <= time_elapsed:
        descent_time_intervals.append(i)
        i += 1
        j += 1

    total_time_intervals.extend(descent_time_intervals)
    return time_elapsed

def exploration_time_iterator():
    time_elapsed = exploration_time * 60
    i = 1 + descent_time_intervals[-1]
    j = 1
    while j <= time_elapsed:
        exploration_time_intervals.append(i)
        i += 1
        j += 1

    total_time_intervals.extend(exploration_time_intervals)
    return time_elapsed

def initial_ascent_time_iterator(depth, rate):
    time_elapsed = (((depth-decompression_depth) / rate) * 60) # Time from initial ascent to decompression stop
    i = 1 + exploration_time_intervals[-1]
    j = 1
    while j <= time_elapsed:
        initial_ascent_time_intervals.append(i)
        i += 1
        j += 1

    total_time_intervals.extend(initial_ascent_time_intervals)
    return time_elapsed

def decompression_time_iterator():
    if depth >= 120:    
        time_elapsed = decompression_time * 60
        i = 1 + initial_ascent_time_intervals[-1]
        j = 1
        while j <= time_elapsed:
            decompression_time_intervals.append(i)
            i += 1
            j += 1
    else:
        time_elapsed = 0
    total_time_intervals.extend(decompression_time_intervals)
    #print(f"decompression_time_intervals: {decompression_time_intervals}")
    return time_elapsed

def final_ascent_time_iterator(rate):
    time_elapsed = (((decompression_depth) / rate) * 60) # Time from decompression to final ascent
    
    i = 1 + total_time_intervals[-1]
    j = 1
    while j < time_elapsed:
        final_ascent_time_intervals.append(i)
        i += 1
        j += 1

    total_time_intervals.extend(final_ascent_time_intervals)
    return time_elapsed


# RAC is Rate of Air Consumption
def r_a_c(s_a_c, depth):
    #This equation allows us to calculate a diver's Rate of Air Consumption at a given depth. The deeper you go, the faster you consume air.
    r_a_c = (s_a_c)*(depth/33 + 1) 

    return r_a_c

# Integrating RAC Equation will give us air consumed while descending
def air_consumed_on_descent(s_a_c, descent_rate, air_used_on_descent):
    """
    The calculation for a diver's Rate of Air Consumption at a depth is:
            (SAC psi/min)*((depth in ft)/(33ft) + 1)

    If we want to find the amount of air consumed from the surface to a depth, we can integrate this equation, which yields:
            (SAC psi/min)*((depth in ft squared)/(33ft*2) + depth in ft)
    We then need to divide our result by the descent rate in ft/min, to ensure we yield a result in units of psi.
    
    So, our final equation is 
            ((SAC psi/min)*((depth in ft squared)/(33ft*2) + depth in ft)) / (descent_rate in ft/min)
    """
  
 
    air_left = psi_initial

    descent_rate_seconds = descent_rate/60

    for i in descent_time_intervals:
        upper_bound = i * descent_rate_seconds
        lower_bound = (i-1) * descent_rate_seconds

        RAC_integral_slice = (s_a_c)*((upper_bound**2)/(66) + upper_bound) - (s_a_c)*((lower_bound**2)/(66) + lower_bound)
        air_used_on_descent += RAC_integral_slice/descent_rate

        descent_air_values.append(air_left - air_used_on_descent)
        total_air_values.append((air_left - air_used_on_descent))
    return air_used_on_descent
def descent_total(s_a_c, depth, descent_rate):
    #Integral of our RAC equation gives us a value in units of (psi * ft)/(min)
    total_integral = (s_a_c)*((depth*depth)/(66) + depth) 

    #Dividing units of (psi*ft)/(min) by units of (ft/min) yields untis of min.
    air_consumed = total_integral/descent_rate

    return air_consumed


def air_consumed_at_bottom(air_used_at_bottom):

    air_left = psi_initial - air_used_on_descent

    for i in exploration_time_intervals:
        integral_slice = r_a_c(s_a_c, depth)

        air_used_at_bottom += integral_slice * (1/60)

        exploration_air_values.append(air_left - air_used_at_bottom)
        total_air_values.append(air_left - air_used_at_bottom)

    return air_used_at_bottom

# Basically the same as the descent, but if you dive deep enough 
#   you need to stop to decompress on the way back up. This is why
#   there are three different functions for the ascent, rather than one.
def air_consumed_on_initial_ascent(s_a_c, ascent_rate, air_used_on_initial_ascent):

    air_left = psi_initial - air_used_on_descent - exploration_air_used

    ascent_rate_seconds = ascent_rate/60

    local_ascent = []
    j = len(initial_ascent_time_intervals)
    for i in initial_ascent_time_intervals:
        local_ascent.append (j)
        j -= 1


    for i in local_ascent:
        upper_bound = i * ascent_rate_seconds
        lower_bound = (i-1) * ascent_rate_seconds

        RAC_integral_slice = (s_a_c)*((upper_bound**2)/(66) + upper_bound) - (s_a_c)*((lower_bound**2)/(66) + lower_bound)
        air_used_on_initial_ascent += RAC_integral_slice/ascent_rate

        initial_ascent_air_values.append(air_left - air_used_on_initial_ascent)
        total_air_values.append((air_left - air_used_on_initial_ascent))
    
    return air_used_on_initial_ascent
def initial_ascent_total(s_a_c, depth, ascent_rate):
    #Integral of our RAC equation gives us a value in units of (psi * ft)/(min)
    total_integral = (s_a_c)*((decompression_depth*decompression_depth)/(66) + decompression_depth) - (s_a_c)*((depth*depth)/(66) + depth) 

    #Dividing units of (psi*ft)/(min) by units of (ft/min) yields untis of min.
    air_consumed = total_integral/ascent_rate

    return air_consumed

def air_consumed_on_decompression(air_used_on_decompression):

    if depth >= 120:
        air_left = psi_initial - air_used_on_descent - air_used_at_bottom - air_used_on_initial_ascent

        for i in decompression_time_intervals:
            integral_slice = r_a_c(s_a_c, depth)

            air_used_on_decompression += integral_slice / 60

            decompression_air_values.append(air_left - air_used_on_decompression)
            total_air_values.append(air_left - air_used_on_decompression)
    else: air_used_on_decompression = 0

    return air_used_on_decompression
def decompression_total():
    decomp_air_used = r_a_c(s_a_c, depth) * decompression_time
    return decomp_air_used

def air_consumed_on_final_ascent(s_a_c, ascent_rate, air_used_on_final_ascent):

    air_left = psi_initial - air_used_on_descent - air_used_at_bottom - air_used_on_initial_ascent - air_used_on_decompression

    ascent_rate_seconds = ascent_rate/60

    local_ascent = []
    j = len(final_ascent_time_intervals)
    for i in final_ascent_time_intervals:
        local_ascent.append (j)
        j -= 1



    for i in local_ascent:
        upper_bound = i * ascent_rate_seconds
        lower_bound = (i-1) * ascent_rate_seconds

        RAC_integral_slice = (s_a_c)*((upper_bound**2)/(66) + upper_bound) - (s_a_c)*((lower_bound**2)/(66) + lower_bound)
        air_used_on_final_ascent += RAC_integral_slice/ascent_rate

        final_ascent_air_values.append(air_left - air_used_on_final_ascent)
        total_air_values.append(air_left - air_used_on_final_ascent)

    return air_used_on_final_ascent
def final_ascent_total(s_a_c, depth, ascent_rate):
    #Integral of our RAC equation gives us a value in units of (psi * ft)/(min)
    total_integral = (s_a_c)*((depth*depth)/(66) + depth) 

    #Dividing units of (psi*ft)/(min) by units of (ft/min) yields untis of min.
    air_consumed = total_integral/ascent_rate

    return air_consumed

# Calculates exploration time given how much extra air is left in the tank
def time_at_bottom(air_consumed_on_descent, air_consumed_on_ascent, usable_psi, s_a_c, depth):
    psi_left = usable_psi - air_consumed_on_descent - air_consumed_on_ascent 

    rac_at_depth = r_a_c(s_a_c, depth) # Calculates how fast air will be consumed at constant depth of exploration

    time_at_bottom = round(psi_left / rac_at_depth, 2) #Here we are dividing units of psi by units of psi/min, which will yield unit of min.

    return time_at_bottom



# ________________________________________________________ #
# ____________________| BODY OF CODE |____________________ #



if depth >= 120:
    decompression_time = 3
else:
    decompression_time = 0


desc_test = descent_total(s_a_c, depth, descent_rate)
init_asc_test = initial_ascent_total(s_a_c, depth, ascent_rate)
decomp_test = decompression_total()
fin_asc_test = final_ascent_total(s_a_c, depth, ascent_rate)

total_air_on_ascent = init_asc_test + decomp_test + fin_asc_test
exploration_time = time_at_bottom(desc_test, total_air_on_ascent, usable_psi, s_a_c, depth)
exploration_air_used = r_a_c(s_a_c, depth)*exploration_time


descent_time_iterator(depth, descent_rate)
exploration_time_iterator()
if len(exploration_time_intervals) > 0:
    initial_ascent_time_iterator(depth, ascent_rate)
    decompression_time_iterator()
    final_ascent_time_iterator(ascent_rate)

air_used_on_descent = air_consumed_on_descent(s_a_c,descent_rate, descent_air)
air_used_at_bottom = air_consumed_at_bottom(exploration_air)
air_used_on_initial_ascent = air_consumed_on_initial_ascent(s_a_c, ascent_rate, initial_ascent_air)
air_used_on_decompression = air_consumed_on_decompression(decompression_air)
air_used_on_final_ascent = air_consumed_on_final_ascent(s_a_c, ascent_rate, final_ascent_air)

print('\n\n_____________________________________________________') # Makin things look pretty
print('____________________| YOUR DIVE |____________________\n')

# Ideal Case
if exploration_time >= 5:
    print(f'You will have {exploration_time} minutes to explore at a depth of {depth} feet, \nwhile still having {reserve_psi} psi of air in case of emergencies.')
    
    # Plotting the graph
    plt.figure(figsize=(8, 6))
    plt.ylim(bottom=0, top=3000)
    plt.plot(total_time_intervals, total_air_values, marker='o', markersize=1, linestyle='-')
    plt.plot(descent_time_intervals, descent_air_values, marker='o', markersize=1, linestyle='-', color='red')
    total_ascent_time_intervals = initial_ascent_time_intervals + decompression_time_intervals + final_ascent_time_intervals
    total_ascent_air_values = initial_ascent_air_values + decompression_air_values + final_ascent_air_values
    plt.plot(total_ascent_time_intervals, total_ascent_air_values, marker='o', markersize=1, linestyle='-', color='orange')

    plt.xlabel('Time (seconds)\n| Red: Descent | Blue: Exploration | Yellow: Ascent |')
    plt.ylabel('Remaining Air Pressure (psi)')
    plt.title('Air Consumption vs. Time')
    plt.grid(True)
    plt.show()
 
# It doesn't really make sense to dive all the way down if you can't explore, right?
# If you don't have a mostly full tank to begin with, maybe add some more air.
elif exploration_time >0 and psi_initial <= 2500: 
    print(f'You will only have {exploration_time} minutes to explore at a depth of {depth} feet. \nThis doesn\'t seem like a worthwhile dive. Maybe try exploring at a shallower depth, or add some more air to your tank.')

# If you have a relatively full tank, the dive may just not be feasible with a commerical tank.
elif exploration_time >0 and psi_initial > 2500:
    print(f'You will only have {exploration_time} minutes to explore at a depth of {depth} feet. \nThis doesn\'t seem like a feasible dive with a standard air tank. Maybe try exploring at a shallower depth.')

# What if your exploration time is negative?
else:
    print(f'You are tring to dive too deep! You won\'t be able to make it to the bottom and still have enough air to make it back up.')


print('_____________________________________________________') # Beautification
print('_____________________________________________________\n')    