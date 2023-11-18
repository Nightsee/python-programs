import re
import os
import platform
import shutil

terminal_width = shutil.get_terminal_size().columns

def clear_terminal():
    #clears the terminal window
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def is_valid_ipv4(ip):
    pattern = re.compile(r'^(\d{1,3}.){3}\d{1,3}(\/\d{1,2})?$')
    return bool(pattern.match(ip))

byte_sequence = [128,64,32,16,8,4,2,1]
stop_prog = False
ip_address_info = {
    "classless": False,
    "class" : "",
    "subnet mask" : "",
    "network ip address" : ""
}

def centered_printing(text):
    padding = max(0, (terminal_width - len(text)) // 2)
    centered_text = " " * padding + text + " " * padding
    print(centered_text)

def result_printer(data, ipAddress):
    print(f"""
    {ipAddress} :
\t class: {data["class"]}
\t subnet mask: {data["subnet mask"]}
\t network ip address: {data["network ip address"]}
    """)

centered_printing("welcome to ip cracker ^__^")
print('\n')
print("you can enter the ip adresse in two formates : \t x.x.x.x/y or x.x.x.x")
print("to exit type : exit.")

while not stop_prog:
    ip_address = input("--> enter ip address : ")
    if ip_address == "exit":
        clear_terminal()
        exit()
    check = is_valid_ipv4(ip_address)
    if not check :
        print("the address you entered is not a valid ip address.")
        exit()

    if "/" in ip_address:
        # check if classless or not
        ip_address_info["classless"] = True
        ip_address_info["class"] = "this ip is classless"

    if not ip_address_info["classless"] :
        # case 1: the address is classed
        ip_bytes = ip_address.split(".")
        count = 1
        for byte in ip_bytes:
            int_byte = int(byte)
            if count == 1:
                if int_byte < 127:
                    ip_address_info['class'] = "A"
                    ip_address_info['subnet mask'] = "255.0.0.0"
                    ip_address_info['network ip address'] = f"{ip_bytes[0]}.0.0.0"
                elif int_byte < 192 and int_byte > 127:
                    ip_address_info['class'] = "B"
                    ip_address_info['subnet mask'] = "255.255.0.0"
                    ip_address_info['network ip address'] = f"{ip_bytes[0]}.{ip_bytes[1]}.0.0"
                else:
                    ip_address_info['class'] = "C"
                    ip_address_info['subnet mask'] = "255.255.255.0"
                    ip_address_info['network ip address'] = f"{ip_bytes[0]}.{ip_bytes[1]}.{ip_bytes[2]}.0"
                break
    else :
        # case 2 : the address is not classed
        prefix_size = int(ip_address.split('/')[1])
        ip_bytes = ip_address.split('/')[0].split('.')
        count = 0 # count is the number of bytes to 1 from left to right
        while prefix_size >= 8:
            count += 1
            prefix_size -= 8
        if prefix_size == 0:
            if count == 1:
                ip_address_info["subnet mask"] = "255.0.0.0"
                ip_address_info['network ip address'] = f"{ip_bytes[0]}.0.0.0"
            if count == 2:
                ip_address_info["subnet mask"] = "255.255.0.0"
                ip_address_info['network ip address'] = f"{ip_bytes[0]}.{ip_bytes[1]}.0.0"
            if count == 3:
                ip_address_info["subnet mask"] = "255.255.255.0"
                ip_address_info['network ip address'] = f"{ip_bytes[0]}.{ip_bytes[1]}.{ip_bytes[2]}.0"
        else :
            digital_representation = 0
            while prefix_size > 0:
                prefix_size -= 1
                digital_representation += byte_sequence[prefix_size]
            if count == 0:
                ip_address_info["subnet mask"] = f"{digital_representation}.0.0.0"
                anding = digital_representation & int(ip_bytes[0])
                ip_address_info['network ip address'] = f"{anding}.0.0.0"
            if count == 1:
                ip_address_info["subnet mask"] = f"255.{digital_representation}.0.0"
                anding = digital_representation & int(ip_bytes[1])
                ip_address_info['network ip address'] = f"{ip_bytes[0]}.{anding}.0.0"
            if count == 2:
                ip_address_info["subnet mask"] = f"255.255.{digital_representation}.0"
                anding = digital_representation & int(ip_bytes[2])
                ip_address_info['network ip address'] = f"{ip_bytes[0]}.{ip_bytes[1]}.{anding}.0"
            if count == 3:
                ip_address_info["subnet mask"] = f"255.255.255.{digital_representation}"
                anding = digital_representation & int(ip_bytes[3])
                ip_address_info['network ip address'] = f"{ip_bytes[0]}.{ip_bytes[1]}.{ip_bytes[2]}.{anding}"
    result_printer(ip_address_info, ip_address)
