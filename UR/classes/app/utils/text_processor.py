
import re

def fix_pos(line,id):
    position = re.findall(r'\[(\S.*)\]', line)
    # print(line)
    # print(position)
    pos  = position[0].split(',')
    posfix = []
    posfix.append(id)
    for j in pos:
        posfix.append(float(j))
    return(posfix)

def process(file):

    with open(file) as f:
        lines = f.read()

    list_of_lines = [
        line.strip()                 # remove trailing and leading whitespace
        for line in lines.split("\n") # split up the text into lines
        if line                      # filter out the empty lines
    ]

    all_pos = []
    section = 0

    for line in list_of_lines:
    # Main program:
        if re.search(r'(#)\s(Global)\s(parameters):',line):
            section = 0
        if re.search(r'(#)\s(Main)\s(program):',line):
            section = 1
        
        if section == 0:
            if re.search(r'(global)\s(speed_ms)\s*=\d*',line):
                data = []
                speed = re.findall(r'\s*(\d.*)', line)
                data.append(30)
                data.append(float(speed[0]))
                all_pos.append(data)
            
            if re.search(r'(global)\s(speed_rads)\s*=\d*',line):
                data = []
                speed = re.findall(r'\s*(\d.*)', line)
                data.append(31)
                data.append(float(speed[0]))
                all_pos.append(data)
            
            if re.search(r'(global)\s(accel_mss)\s*=\d*',line):
                data = []
                speed = re.findall(r'\s*(\d.*)', line)
                data.append(32)
                data.append(float(speed[0]))
                all_pos.append(data)
            
            if re.search(r'(global)\s(accel_radss)\s*=\d*',line):
                data = []
                speed = re.findall(r'\s*(\d.*)', line)
                data.append(33)
                data.append(float(speed[0]))
                all_pos.append(data)
            
            if re.search(r'(global)\s(blend_radius_m)\s*=\d*',line):
                data = []
                speed = re.findall(r'\s*(\d.*)', line)
                data.append(34)
                data.append(float(speed[0]))
                all_pos.append(data)

        if section == 1:

            # if re.search(r'(movep)\(',line):
            #     posfix = fix_pos(line,6)
            #     all_pos.append(posfix)
            
            if re.search(r'(tool_on\(\))',line):
                data = []
                data.append(1)
                all_pos.append(data)

            if re.search(r'(tool_off\(\))',line):
                data = []
                data.append(2)
                all_pos.append(data)
            
            if re.search(r'(movel)\(\[',line):
                posfix = fix_pos(line,3)
                all_pos.append(posfix)
            
            if re.search(r'(movel)\(p\[',line):
                posfix = fix_pos(line,4)
                all_pos.append(posfix)

            if re.search(r'(movej)\(\[',line):
                posfix = fix_pos(line,5)
                all_pos.append(posfix)
            
            if re.search(r'(movej)\(p\[',line):
                posfix = fix_pos(line,6)
                all_pos.append(posfix)
            
            if re.search(r'(visor_detect\(\))',line):
                data = []
                data.append(10)
                all_pos.append(data)
            
            if re.search(r'(visor_code\(\))',line):
                data = []
                data.append(11)
                all_pos.append(data)
            
            if re.search(r'(camera_inspection\(\))',line):
                data = []
                data.append(12)
                all_pos.append(data)                
            
            if re.search(r'(move_axis_0\(\))',line):
                data = []
                data.append(20)
                all_pos.append(data)
            if re.search(r'(move_axis_1\(\))',line):
                data = []
                data.append(21)
                all_pos.append(data)
            if re.search(r'(move_axis_2\(\))',line):
                data = []
                data.append(22)
                all_pos.append(data)
            if re.search(r'(move_axis_3\(\))',line):
                data = []
                data.append(23)
                all_pos.append(data)
                

            if re.search(r'(speed_ms\s*=\d*)',line):
                data = []
                speed = re.findall(r'\s*(\d.*)', line)
                data.append(30)
                data.append(float(speed[0]))
                all_pos.append(data)

            if re.search(r'(speed_rads\s*=\d*)',line):
                data = []
                speed = re.findall(r'\s*(\d.*)', line)
                data.append(31)
                data.append(float(speed[0]))
                all_pos.append(data)
            
            if re.search(r'(accel_mss\s*=\d*)',line):
                data = []
                speed = re.findall(r'\s*(\d.*)', line)
                data.append(32)
                data.append(float(speed[0]))
                all_pos.append(data)
            
            if re.search(r'(accel_radss\s*=\d*)',line):
                data = []
                speed = re.findall(r'\s*(\d.*)', line)
                data.append(33)
                data.append(float(speed[0]))
                all_pos.append(data)
            
            if re.search(r'(blend_radius_m\s*=\d*)',line):
                data = []
                speed = re.findall(r'\s*(\d.*)', line)
                data.append(34)
                data.append(float(speed[0]))
                all_pos.append(data)
            


    
    
    # 1 = active tool
    # 2 = deactive tool
    # 3 = move L (joint type)
    # 4 = move L (cartesian type)
    # 5 = move J (joint type)
    # 6 = move J (cartesian type)

    # 10 = visor detect
    # 11 = visor code

    # 20 = move axis 0
    # 21 = move axis 1
    # 22 = move axis 2
    # 23 = move axis 3

    # 30 = speed_ms
    # 31 = speed_rads
    # 32 = accel_mss
    # 33 = accel_radss
    # 34 = blend_radius_m
    
    speed_ms = 0  
    speed_rads = 0  
    accel_mss = 0  
    accel_radss = 0  
    blend_radius_m = 0

    targets = []    
    tool = 0

    for i in all_pos: 
        # print(i)

        if i[0] == 30:
            speed_ms = i[1]
        if i[0] == 31:
            speed_rads = i[1]

        if i[0] == 32:
            accel_mss = i[1]
        if i[0] == 33:
            accel_radss = i[1]

        if i[0] == 34:
            blend_radius_m = i[1]
        
        # 1 = active too
        if i[0] == 1:
            targets.append([[0,0,0,0,0,0],0,0,0,0,i[0]]) 
        # 2 = deactive tool
        if i[0] == 2:
            targets.append([[0,0,0,0,0,0],0,0,0,0,i[0]]) 
        
        # Move L (joint mode)
        if i[0] == 3:
            targets.append([i[1:],accel_radss,speed_rads,0,blend_radius_m,i[0]]) 
        # Move L (cartesian mode)
        if i[0] == 4:
            targets.append([i[1:],accel_mss,speed_ms,0,blend_radius_m,i[0]]) 
        
        # Move J (joint mode)
        if i[0] == 5:
            targets.append([i[1:],accel_radss,speed_rads,0,blend_radius_m,i[0]]) 
        # Move J (cartesian mode)
        if i[0] == 6:
            targets.append([i[1:],accel_mss,speed_ms,0,blend_radius_m,i[0]])
        
        # 10 = visor detect
        if i[0] == 10:
            targets.append([[0,0,0,0,0,0],0,0,0,0,i[0]])
        # 11 = visor code
        if i[0] == 11:
            targets.append([[0,0,0,0,0,0],0,0,0,0,i[0]])
        # 12 = camera inspection
        if i[0] == 12:
            targets.append([[0,0,0,0,0,0],0,0,0,0,i[0]])

        # 20 = move axis 0
        if i[0] == 20:
            targets.append([[0,0,0,0,0,0],0,0,0,0,i[0]])
        # 21 = move axis 1
        if i[0] == 21:
            targets.append([[0,0,0,0,0,0],0,0,0,0,i[0]])
        # 22 = move axis 2
        if i[0] == 22:
            targets.append([[0,0,0,0,0,0],0,0,0,0,i[0]])
        # 23 = move axis 3
        if i[0] == 23:
            targets.append([[0,0,0,0,0,0],0,0,0,0,i[0]])
        # 24 = move axis 4
        if i[0] == 24:
            targets.append([[0,0,0,0,0,0],0,0,0,0,i[0]])
    
    # for i in targets:
    #     print (i)

    # print (len(targets))
    return targets


# process('urp/routine_8.txt')

# 1 (tool_on)
# 2 (tool_off)
# [[2.43791, -0.836938, -1.898501, -1.976621, 1.570586, 0.10807], 6.2832, 13.963, 0, 0.0, 4]
# [[-0.154066, 0.370617, 0.268, -2.905868, -1.192671, 0.000279], 0.1, 3.0, 0, 0.0, 3]

