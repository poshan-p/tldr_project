import concurrent.futures, os, json
from configurations.tldr_fail_test import tldr_dectector
from utils.checkpoint import save_tldr_checkpoint
from utils.result import save_tldr_results


def tldr_process(ip_addresses, num_of_threads, chunk_size, countryname, version,  Processed_ip_addresses = []):
    """
    This function make use of parallel computing to speed up the process which calls 
    the tldr_detector function.

    #### :Parameters
        ip_address: string

        num_of_threads: integer
            Number of instances to create

        chunck_size: integer
            The number of IPs of each instance

        Processed_ip_address : list
            By default, the list is empty.
    """
    number_of_ip_addresses = len(ip_addresses)
    checkpoint = f"checkpoints/{countryname}/tldr_process_{version}_results.json"
    
    for i in range(0, number_of_ip_addresses, chunk_size):
        with concurrent.futures.ThreadPoolExecutor(num_of_threads) as executor:
            futures = {executor.submit(tldr_dectector, ip, timeout=30): ip for ip in ip_addresses[i:i+chunk_size]}
            for future in concurrent.futures.as_completed(futures):                
                try:
                    if future.result():
                        Processed_ip_addresses.append(future.result())
                    else:
                        Processed_ip_addresses.append(future.result())
                except Exception as e:
                    print(e)
                    Processed_ip_addresses.append(future.result())
                
                os.system('clear')
                print(f"Checkpoint at Checkpoints/{countryname}/tldr_process_{version}_results.json\nTotal IP address: \t{number_of_ip_addresses}\nIP Addresses Scanned: \t{len(Processed_ip_addresses)}\n{progress_bar(len(Processed_ip_addresses), number_of_ip_addresses, 100)}")
        
        # list_ip = [list(ip.values())[0] for ip in Processed_ip_addresses]
        # list_encoding = [list(binary.keys())[0] for binary in Processed_ip_addresses]
             
        save_tldr_checkpoint(Processed_ip_addresses, checkpoint)
    save_tldr_checkpoint(Processed_ip_addresses, checkpoint)

    save_tldr_results(len(Processed_ip_addresses), Processed_ip_addresses, f"results/{countryname}/tldr_process_{version}_results.json")
    

def resume_tldr_process(ip_address, num_of_threads, chunk_size, countryname, asndetails, version):
    checkpoint = f"checkpoints/{countryname}/tldr_process_{version}_results.json"
    
    if not os.path.exists(checkpoint):
        tldr_process(ip_address, num_of_threads,version=version, chunk_size=chunk_size, countryname=countryname)
    else:
        with open(checkpoint, "rb") as f:
            cp= json.load(f)
            cp_ip_addresses = cp["ip_addresses_encoding"]
            
            _remaining_ip = list(set((ip) for ip in ip_address) - (set(list(ip.values())[0] for ip in cp_ip_addresses)))
                        
            tldr_process(_remaining_ip, num_of_threads, chunk_size, countryname,version, cp_ip_addresses)
            _remaining_ip = None



def progress_bar(current, total, bar_length=100):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '#'
    padding = int(bar_length - len(arrow)) * ' '

    return (f'Progress: [{arrow}{padding}] {fraction * 100:.2f}% ') + ('\n' if current == total else '\r')


# # Given test data
# ip = ['8.8.8.8', '192.168.100.1', '164.234.65.57', '197.64.102.55']

# # example of output
# stuff = [{'1111': '8.8.8.8'}, {'0000': '192.168.100.1'}, {'0000': '164.234.65.57'}, {'0000': '197.64.102.55'}]

# # get the Ip address
# ip_address = [list(d.values())[0] for d in stuff]

# # Get the Binary encoding
# ip_address = [list(d.keys())[0] for d in stuff]
