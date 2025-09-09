### Zablos Secret Sharer V3 One Time Pad ###

import os
import sys
import json
from secrets import randbelow
from string import ascii_uppercase
from string import ascii_lowercase

FALLBACK_CODE = 67
SPACE_PLACEHOLDER = "§"

decimal = [x for x in range(0, 100)]  
sign = [str(x) for x in range(0, 10)] + [x for x in ascii_uppercase] + [x for x in ascii_lowercase] + [
    ".", ",", "!", "?", "_", "§", "ß", "$", "&", "%", '"', "(", ")", "-", "{", "}", "[", "]", "*", "/", "+", "Ä",
    "Ü", "=", "²", "<", ">", ";", ":", "~", "#", "@", "Ö", "°", "^", "ö", "ä", "ü"]
mastercode = dict(zip(sign, decimal))
masterdecode = dict(zip(decimal, sign))

codes_global = {}  


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def save_codes_to_json(codes):
    filename = input("Enter filename to save codes (codes.json): ").strip()
    if not filename.endswith(".json"):
        filename += ".json"
    try:
        with open(filename, "w") as f:
            json.dump(codes, f, indent=4)
        print(f"Codes saved to {filename}\n")
    except Exception as e:
        print(f"Error saving file: {e}\n")


def load_codes_from_json():
    filename = input("Enter filename to load codes from (codes.json): ").strip()
    try:
        with open(filename, "r") as f:
            loaded_codes = json.load(f)
        print(f"Codes loaded from {filename}\n")
        return loaded_codes
    except Exception as e:
        print(f"Error loading file: {e}\n")
        return None


def validate_code_input(code):
    if " " in code:
        raise ValueError("Code must not contain spaces. Use a valid symbol instead.")


def print_mastercode():
    print()
    print(masterdecode)
    print()
    print(mastercode)


def translate_into_mastercode():
    global codes_global

    shares = check_int()
    message = list(input("Message: "))
    messageMaster = []
    UccMaster = []
    c1str = ''
    ucc_input = input(f'C1: ')
    ucc = list(ucc_input)

    for x in ucc:
        if x == ' ':
            x = SPACE_PLACEHOLDER
            c1str += x
        else:
            c1str += x

    clear()
    print(f'C1: {c1str}')

    for x in message:
        if x == " ":
            x = SPACE_PLACEHOLDER
        messageMaster.append(mastercode.get(x, FALLBACK_CODE))
    for x in ucc:
        if x == " ":
            x = SPACE_PLACEHOLDER
        UccMaster.append(mastercode.get(x, FALLBACK_CODE))

    if len(messageMaster) < len(UccMaster):
        missing = len(UccMaster) - len(messageMaster)
        for _ in range(missing):
            messageMaster.append(FALLBACK_CODE)
    elif len(messageMaster) > len(UccMaster):
        print("Code is too short!")
        return

    codes_global = {}
    codes_global['C1'] = [x for x in c1str]

    if shares == 2:
        UccNeg = []
        for x in UccMaster:
            UccNeg.append(x * -1)
        c2 = [sum(i) for i in zip(messageMaster, UccNeg)]
        code2_list = [masterdecode[x % 100] for x in c2]
        codes_global['C2'] = code2_list
        code2_str = ''.join(code2_list)
        print(f'C2: {code2_str}')
    else:
        pseudo_random_numbers(messageMaster, UccMaster, shares)


def pseudo_random_numbers(messageMaster, UccMaster, shares):
    global codes_global
    random_codes = {}
    count = len(UccMaster)
    for x in range(2, shares):
        key = f'C{x}'
        value = []
        for _ in range(count):
            value.append(randbelow(100))
        random_codes[key] = value
    last_code(messageMaster, random_codes, UccMaster, shares)


def last_code(messageMaster, random_codes, UccMaster, shares):
    global codes_global
    count = len(UccMaster)

    for i in range(2, shares):
        key = f'C{i}'
        templist = random_codes[key]
        codes_global[key] = [masterdecode[y] for y in templist]
        messageOut = ''.join(codes_global[key])
        print(f'{key}: {messageOut}')

    mdtemp = list(zip(*random_codes.values()))
    copylist = []
    for l in mdtemp:
        copylist.append(sum(l))

    finalSum = list(sum(i) for i in (zip(copylist, UccMaster)))
    copylist.clear()
    copylist = [x % 100 for x in finalSum]
    last_code_list = [((m - c) % 100) for m, c in zip(messageMaster, copylist)]

    last_code_chars = [masterdecode[x] for x in last_code_list]

    codes_global[f'C{shares}'] = last_code_chars
    messageOut = ''.join(last_code_chars)
    print(f'C{shares}: {messageOut}')


def decode_message():
    shares = check_int()
    codes = {}
    copylist = []
    x = 1

    for _ in range(shares):
        key = f'C{x}'
        value = list(input(f'{key}: '))
        try:
            validate_code_input(value)
        except ValueError as e:
            print(f"[Error] {e}")
            return
        codes[key] = value
        x += 1

    if shares <= 1:
        print("error!")
        return

    messageOut = ""
    md = list(zip(*codes.values()))

    for l in md:
        temp = 0
        for value in l:
            temp += mastercode[value] % 100
        if temp >= 100:
            temp = temp % 100
        copylist.append(temp)

    for x in copylist:
        messageOut += masterdecode[x]
    print()
    print('Message: ', messageOut.replace(SPACE_PLACEHOLDER, " "))
    print()


def check_int():
    s = input("enter shares count 2 -> 99: ")
    if s.isdigit() and 2 <= int(s) <= 99:
        return int(s)
    return 2


def generate_otp():
    global codes_global
    while True:
        try:
            count = int(input("Code length: "))
            if count <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for code length.")
    
    while True:
        try:
            range_low = int(input('Code start#: '))
            range_high = int(input('Code last#: '))
            if range_low > range_high:
                print("Start number must be less than or equal to last number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter valid integers for start and last code numbers.")

    random_codes = {}

    for x in range(range_low, range_high + 1):
        key = f'C{x}'
        value = [randbelow(100) for _ in range(count)]
        random_codes[key] = value

    codes_global = {}
    for key, values in random_codes.items():
        codes_global[key] = [masterdecode[y] for y in values]
        messageOut = ''.join(codes_global[key])
        print(f'{key}: {messageOut}')


def menu():
    global codes_global
    print()
    menu_choice = input("(S)plit, (C)ombine, (M)astercode, (O)TP, (W)ipe, Sa(V)e, (L)oad, (Q)uit? ").lower()
    if menu_choice == "s":
        try:
            translate_into_mastercode()
        except ValueError as e:
            print(f"[Error] {e}")
    elif menu_choice == "c":
        decode_message()
    elif menu_choice == "m":
        print_mastercode()
    elif menu_choice == " " or menu_choice == "w":
        clear()
    elif menu_choice == "o":
        generate_otp()
    elif menu_choice == "v":
        if codes_global:
            save_codes_to_json(codes_global)
        else:
            print("No codes generated or loaded yet to save.\n")
    elif menu_choice == "l":
        loaded = load_codes_from_json()
        if loaded:
            codes_global = loaded
            print("[Loaded Codes]:")
            for key, val in codes_global.items():
                print(f"{key}: {''.join(val)}")
            print()
    elif menu_choice == "q":
        print("Goodbye!")
        sys.exit()
    else:
        print("Invalid option, please try again.")


def main():
    while True:
        menu()


if __name__ == "__main__":
    main()
