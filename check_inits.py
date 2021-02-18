def g1(x,coefficient=1):
    return (x ^ 0b0001111,coefficient)

def g2(x,coefficient=1):
    return (x ^ 0b0110011,coefficient)

def g3(x,coefficient=1):
    return (x ^ 0b1010101,coefficient)

def g4(x,coefficient=1):
    s = (x&0b0000001) ^ ((x&0b0000010) >> 1) ^ ((x&0b0000100) >> 2) ^ ((x&0b0001000) >> 3)
    return (x,coefficient*(-1)**s)

def g5(x,coefficient=1):
    s = ((x&0b0100000)>>5) ^ ((x&0b0010000)>>4) ^ ((x&0b0000010)>>1) ^ (x&0b0000001)
    return (x,coefficient*(-1)**s)

def g6(x,coefficient=1):
    s = ((x&0b1000000)>>6) ^ ((x&0b0010000)>>4) ^ ((x&0b0000100)>>2) ^ (x&0b0000001)
    return (x,coefficient*(-1)**s)

def I(x,coefficient):
    return (x,coefficient)

def f(measurement, x):
    fn = [g1,g2,g3,g4,g5,g6]
    output_dict = {x:1}

    # print(output_dict,'\n')

    for i in range(-1,-7,-1):
        keys = list(output_dict.keys())
        for state in keys:
            (s,c) = fn[i](state,output_dict[state])
            if s in output_dict.keys():
                output_dict[s] += (-1)**(int(measurement[i]))*c
            else:
                output_dict[s] = (-1)**(int(measurement[i]))*c
        keys = list(output_dict.keys())
        for state in keys:
            if output_dict[state] == 0:
                output_dict.pop(state)

        # print('i=',i+7,' measured bit=', measurement[i], '\n',output_dict,'\n')
    
    return output_dict

# x = 0b0001010
#   0b1010101
# print(g4(x),g5(x),g6(x))

sv_dict = {}

for x in range(8):
    print(bin(x)[2:].zfill(3))
    sv = f(bin(x)[2:].zfill(3)+'000',0b1111111)
    print(sv,'\n\n')
    sv_dict[bin(x)[2:].zfill(3)] = sv
    
def apply_z(sv, pos):
    new_sv = {}
    for ket in sv.keys():
        sign = 0
        for i in range(7):
            sign += (ket & pos) >> i
        sign = sign % 2
        new_sv[ket] = sv[ket]*(-1)**sign
    return new_sv

for syndrome in sv_dict.keys():
    print('syndrome: ', syndrome)
    pos = 0b0000000
    if syndrome[0] == '1':
        pos = pos | 0b0001000
    if syndrome[1] == '1':
        pos = pos | 0b0100000
    if syndrome[2] == '1':
        pos = pos | 0b1000000
    print(apply_z(sv_dict[syndrome], pos))


