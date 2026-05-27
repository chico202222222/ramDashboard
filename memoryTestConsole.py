import subprocess

# here, I use the subprocess library to get the cmd.exe to return me the amount of total and free RAM memo
# i have in my system. i use the "result_free" and "result_total" variables to convert them to int values, and then,
# finally to float values in gigabytes.
def calculate_memory():
    # getting the free memory in KB
    result_free = subprocess.check_output(["wmic", "OS", "get", "FreePhysicalMemory"], text=True)
    free_kb = int(''.join(filter(str.isdigit, result_free)))
    gbFreeMemory: float = free_kb / (1024 * 1024)

    # getting the total memory in KB
    result_total = subprocess.check_output(["wmic", "OS", "get", "TotalVisibleMemorySize"], text=True)
    total_kb = int(''.join(filter(str.isdigit, result_total)))
    gbTotalMemory: float = total_kb / (1024 * 1024)

    print(f'Total Memory: {gbTotalMemory:.2f} GB')
    print(f'Free Memory: {gbFreeMemory:.2f} GB')

    # returning both values so they can be assigned to variables outside the function
    return gbFreeMemory, gbTotalMemory

def memoryUsage():
    free_ram, total_ram = calculate_memory()
    used_ram = total_ram - free_ram
    used_percentage = (used_ram / total_ram) * 100
    free_percentage = (free_ram / total_ram) * 100
    #percentage lol
    print(f'Used Memory: {used_ram:.2f} GB ({used_percentage:.1f}%)')
    print(f'Free Memory: {free_ram:.2f} GB ({free_percentage:.1f}%)')
memoryUsage()
