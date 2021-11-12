import time
import subprocess

def main():
    address = input("Enter a domain: ")
    running = True
    iteration = 0

    while(running):
        average_TTL_for_hop, ips = run_tracert_command(address)

        print("***************************************")

        time.sleep(10)
        iteration += 1


def run_tracert_command(address):
    ips = []
    average_TTL_for_hop = []

    response = subprocess.Popen("tracert -d %s" % address, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

    while True:
        data = response.stdout.readline()

        if data.strip() == "":
            pass
        else:
            split_data = data.strip().split()
            print(split_data)
            if "over" not in split_data and len(split_data) >= 6:
                average_TTL, ip = parse_data(list(split_data))
            
                print(average_TTL, ip)

                #average_TTL_for_hop.append(average_TTL)
                #ips.append(ip)
        if not data: break

    response.wait()
    return average_TTL_for_hop, ip

def parse_data(data):
    hops = []
    average_TTL = 0
    counter = 0

    unwanted = {"ms"}

    clean_data = [element for element in data if element not in unwanted]

    if(str(data[4]).find("Request") == - 1):
        ip = str(clean_data[-1])
    else:
        ip = "*"

    hops.append(str(clean_data[1]))
    hops.append(str(clean_data[2]))
    hops.append(str(clean_data[3]))

    for string in hops:
        if "<" in string:
             string = string.replace("<", "")
        if string.find("*") == -1:
            average_TTL += int(string)
            counter += 1

    if counter == 0:
        average_TTL = 999
    else:
        average_TTL = average_TTL / counter

    return average_TTL, ip

if __name__ == '__main__':
    main()