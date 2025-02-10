# S-Box (hex values as strings)
sbox = [
    ['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
    ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
    ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
    ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
    ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
    ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
    ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
    ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
    ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
    ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
    ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
    ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
    ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
    ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
    ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
    ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']
]

# Rcon table for key expansion (hex)
rcon = ['01', '02', '04', '08', '10', '20', '40', '80', '1b', '36']

def hex_to_int(hex_str):
    return int(hex_str, 16)

def int_to_hex(number):
    return format(number, '02x')

def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            row = hex_to_int(state[i][j][0])
            col = hex_to_int(state[i][j][1])
            state[i][j] = sbox[row][col]
    return state

def shift_rows(state):
    new_state = [row[:] for row in state]
    new_state[1] = [state[1][1], state[1][2], state[1][3], state[1][0]]
    new_state[2] = [state[2][2], state[2][3], state[2][0], state[2][1]]
    new_state[3] = [state[3][3], state[3][0], state[3][1], state[3][2]]
    return new_state

def add_round_key(state, round_key):
    return [[int_to_hex(hex_to_int(state[i][j]) ^ hex_to_int(round_key[i][j])) for j in range(4)] for i in range(4)]

def key_expansion(key):
    words = [key[i:i+4] for i in range(0, len(key), 4)]
    for i in range(4, 44):
        temp = words[i-1]
        if i % 4 == 0:
            temp = [temp[1], temp[2], temp[3], temp[0]]
            temp = [sbox[hex_to_int(hex_str[0])][hex_to_int(hex_str[1])] for hex_str in temp]
            temp[0] = int_to_hex(hex_to_int(temp[0]) ^ hex_to_int(rcon[i // 4 - 1]))
        words.append([int_to_hex(hex_to_int(words[i-4][j]) ^ hex_to_int(temp[j])) for j in range(4)])
    return words

def aes_problem_1():
    print("\n--- AES Problem 1 ---")
    plaintext = ['00', '00', '01', '00', '02', '03', '03', '04', '04', '06', '06', '08', '08', '07', '0a', '09']
    key = ['01', '01', '01', '01', '02', '02', '02', '02', '03', '03', '03', '03', '04', '04', '04', '04']

    state = [[plaintext[i + 4 * j] for j in range(4)] for i in range(4)]
    round_key = [[key[i + 4 * j] for j in range(4)] for i in range(4)]

    state = add_round_key(state, round_key)
    state = sub_bytes(state)
    state = shift_rows(state)

    print("\nState after transformations:")
    for row in state:
        print(row)

def aes_problem_2():
    print("\n--- AES Problem 2 ---")
    plaintext = ['02', '10', '11', '21', 'a2', '32', '44', '53', '61', '07', 'b6', 'e7', 'd8', 'f9', '0c', 'db']
    key = ['00', '00', '10', '01', '20', '02', '30', '03', '40', '04', '50', '05', '60', '06', '70', '07']

    state = [[plaintext[i + 4 * j] for j in range(4)] for i in range(4)]
    round_key = [[key[i + 4 * j] for j in range(4)] for i in range(4)]

    state = add_round_key(state, round_key)
    state = sub_bytes(state)
    state = shift_rows(state)

    print("\nState after transformations:")
    for row in state:
        print(row)

def aes_key_expansion_problem():
    print("\n--- AES Key Expansion Problem ---")
    key = ['0a', '7c', '12', '20', '51', '42', '41', '15', '65', '63', 'b2', '48', '72', '45', '31', '63']
    words = key_expansion(key)

    print("\nExpanded Key:")
    for i in range(4, 8):
        print(f"W{i}: {words[i]}")

# Run Problems
aes_problem_1()
aes_problem_2()
aes_key_expansion_problem()
