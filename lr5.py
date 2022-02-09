import psutil
from win32.win32api import GlobalMemoryStatus
import matplotlib.pyplot as plt
import pymem
from loguru import logger


conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                    5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                    13: 'D', 14: 'E', 15: 'F'}

def decimalToHexadecimal(decimal):
    hexadecimal = ''
    while(decimal > 0):
        remainder = decimal % 16
        hexadecimal = conversion_table[remainder] + hexadecimal
        decimal = decimal // 16
    return hexadecimal


def first():
    data = GlobalMemoryStatus()
    print(data)
    graph = [
        data['MemoryLoad'] / 100,
        data['AvailPhys'] / data['TotalPhys'],
        data['AvailPageFile'] / data['TotalPageFile'],
        data['AvailVirtual'] / data['TotalVirtual']
    ]
    index = ['MemoryLoad', 'Phys', 'PageFile', 'Virtual']

    plt.bar(index, graph)
    plt.show()


def second():
    data = psutil.pids()
    processes = []
    for i in data:
        try:
            p = psutil.Process(i)
            pdict = {}
            pdict['name'] = p.name()
            pdict['pid'] = i
            pdict['rss'] = p.memory_info()[0]  # размер страниц памяти выделенных процессу
            pm = pymem.Pymem(str(p.name()))
            info = pymem.memory.virtual_query(pm.process_handle, pm.base_address)
            pdict['Base Address'] = decimalToHexadecimal(pm.base_address)
            pdict['End Address'] = decimalToHexadecimal(pm.base_address + p.memory_info()[0])
            pdict['Allocation Base'] = info.AllocationBase
            pdict['Allocation Protect'] = info.AllocationProtect
            pdict['Region Size'] = info.RegionSize
            pdict['Protect'] = info.Protect
            processes.append(pdict)
        except Exception as e:
            pass
    logger.warning('ProcessMap')
    for i in processes:
        print(i)


second()
