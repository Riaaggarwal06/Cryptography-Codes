def hex_to_bin(hex_key):
    return bin(int(hex_key, 16))[2:].zfill(64)

def left_circular_shift(bits, shifts):
    return bits[shifts:] + bits[:shifts]

def pc1(key):
    pc1_table = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]
    return ''.join([key[i - 1] for i in pc1_table])

def pc2(key):
    pc2_table = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]
    return ''.join([key[i - 1] for i in pc2_table])

def generate_round_keys(initial_key, start, rounds):
    permuted_key = pc1(initial_key)
    left, right = permuted_key[:28], permuted_key[28:]
    shift_schedule = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    round_keys = []
    
    for i in range(start, start + rounds):
        left = left_circular_shift(left, shift_schedule[i])
        right = left_circular_shift(right, shift_schedule[i])
        combined_key = left + right
        round_key = pc2(combined_key)
        round_keys.append(round_key)
    
    return round_keys

def xor(a, b):
    return ''.join(['0' if a[i] == b[i] else '1' for i in range(len(a))])

def initial_permutation(block):
    ip_table = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]
    return ''.join([block[i - 1] for i in ip_table])

def des_one_round_encrypt(plaintext, key):
    permuted_plaintext = initial_permutation(plaintext)
    left, right = permuted_plaintext[:32], permuted_plaintext[32:]
    
    e_table = [
        32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
    ]
    
    expanded_right = ''.join([right[i - 1] for i in e_table])
    xored = xor(expanded_right, key)
    
    return xored

initial_key_hex = "231457799BBCDFF1"
initial_key_bin = hex_to_bin(initial_key_hex)
k1_k3 = generate_round_keys(initial_key_bin, 1, 3)

print("Keys (K1, K2, K3):")
for i, key in enumerate(k1_k3, 1):
    print(f"K{i}: {key}")

round8_key_hex = "A21036331ECB5873"
round8_key_bin = hex_to_bin(round8_key_hex)
round9_11 = generate_round_keys(round8_key_bin, 8, 3)

print("\nKeys (Round 9-11):")
for i, key in enumerate(round9_11, 9):
    print(f"Round {i}: {key}")

plaintext_hex = "0123456789ABCDEF"
plaintext_bin = hex_to_bin(plaintext_hex)
key_bin = hex_to_bin("1111222233334444")
ciphertext = des_one_round_encrypt(plaintext_bin, key_bin)

print("\nCiphertext after one round:")
print(ciphertext)
