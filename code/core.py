import sys
import subprocess
import os
import argparse
import shutil

import csv
import itertools
import time
import copy

from code.cache import *
from multiprocessing import Pool

DEFINITION = "\nDEFINITION_PARAMETER "
POSITION = " 9.41 2.07"

def async_operation(id, input_hash, configuration, parameters):
    run_timenet(parameters, id)
    elaboration(configuration, input_hash, id)

def run_timenet(parameters,id):
    max_VNF = min( parameters.pop('maxVNF'), 6)
    max_NR = min( parameters.pop('maxNR'), 4)
 
    header_values_to_timenet=""
    for key in parameters:
        if isinstance(parameters[key],float) or isinstance(parameters[key],int):
            header_values_to_timenet = header_values_to_timenet + DEFINITION + key + " " + str(parameters[key]) + POSITION

    counter = 0
    values = set()
    for subset in itertools.combinations_with_replacement( [k for k in range(max_VNF, -1, -1)], int(max_NR)):
        values.add(subset)

    # Init log file
    log_file = open("logs//" + id + "_log", "a+")
    log_file.write(str(counter) + "|" + str(len(values)*2) + "\n")
    log_file.close()
    
    # Init output file
    output_file = open(id+".csv","w+")
    output_file.write("VNF1;VNF2;VNF3;VNF4;perf;parallelo\n")
    for perf in range(3,5):
        for value in values:
            VNF1=value[0]             
            VNF2=0 if len(value) < 2 else value[1]   
            VNF3=0 if len(value) < 3 else value[2]   
            VNF4=0 if len(value) < 4 else value[3]  
            counter += 1
            if VNF1+VNF2+VNF3+VNF4 > perf: 
                timenet_values = header_values_to_timenet + DEFINITION + "VNF1 "+ str(VNF1) + POSITION + DEFINITION + "VNF2 " + str(VNF2) + POSITION + DEFINITION + "VNF3 " + str(VNF3) + POSITION + DEFINITION + "VNF4 " + str(VNF4) + POSITION + "\n"     
                    
                input_file_to_timenet = open("homogeneous\\data_" + id,'w')
                input_file_to_timenet.write(timenet_values)
                input_file_to_timenet.close()
                
                try:
                    compose_timenet_file(id)
                                
                    subprocess.check_output("rm -rf " + id + ".dir")
                    subprocess.run('"C:\\Program Files (x86)\\TimeNET\\TimeNET\\EDSPN\\StatAnalysis\\scripts\\SOLVE.bat" '+ id + ' -E -s -i 10000 1e-10', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    result = read_result(id)                
                    output_file.write(";".join([str(VNF1), str(VNF2), str(VNF3), str(VNF4), str(perf), str(result)]) + "\n")
                except:
                    time.sleep(1)
                    compose_timenet_file(id)
                    
                    subprocess.check_output('"C:\\Program Files (x86)\\TimeNET\\TimeNET\\EDSPN\\StatAnalysis\\scripts\\SOLVE.bat"'+' '+ id + ' -E -s -i 10000 1e-10')
                    
                    result = read_result(id) 
                    output_file.write(";".join([str(VNF1), str(VNF2), str(VNF3), str(VNF4), str(perf), str(result)]) + "\n")

            log_file = open("logs//" + id + "_log", "a+")
            log_file.write(str(counter) + "|" + str(len(values)*2) + "\n")
            log_file.close()    
    
    output_file.close()
    shutil.rmtree(id+".dir")
    os.remove("homogeneous\\data_"+id)

    
def compose_timenet_file(id):
    filenames = ["homogeneous\\header", "homogeneous\\data_"+id, "homogeneous\\footer"]
    filename_timenet=id + ".TN"
    with open(filename_timenet, 'w+') as file_timenet:
        for fname in filenames:
            with open(fname) as infile:
                file_timenet.write(infile.read())
   
def read_result(id):
    result_file = open(id + ".dir\\" + id + ".RESULTS")
    result = float(result_file.readline().split("result = ")[1])
    result_file.close()
    return result

def elaboration(configuration, input_hash, id):
    for threshold in configuration['availability_target']:
        parallel_elab(configuration, input_hash, id, threshold)

def parallel_elab(configuration, input_hash, id, threshold):
    weights=configuration['weights']
    costs=configuration['costs']
    t = time.time()
    
    filename = id + ".csv"
    cscf = {}
    hss = {}
    out_filename = "results//" + id + "_" + str(threshold) + "_results.csv"
    
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            conf = ','.join(row[:4])
            if int(row[4]) == 3:
                if float(row[5].replace(',', '.')) >= threshold:
                    cscf[conf] = float(row[5].replace(',', '.'))
            elif int(row[4]) == 4:
                if float(row[5].replace(',', '.')) >= threshold:
                    hss[conf] = float(row[5].replace(',', '.'))


    minCost = float('inf')
    with open(out_filename, mode='w',newline='') as h_file:
        h_writer = csv.writer(h_file, delimiter=';')
        h_writer.writerow(['np1','np2','np3','np4','ns1','ns2','ns3','ns4','ni1','ni2','ni3','ni4','nh1','nh2','nh3','nh4','series','cost'])
        for h in hss:
            costH = cost_calculator(h, costs=costs) 
            parH = hss[h]
            if costH > minCost*weights[0] or parH < threshold:
                continue
            for i in cscf:
                costIH = cost_calculator(i, costs=costs) + costH
                parIH = cscf[i] * parH
                if costIH > minCost*weights[1] or parIH < threshold:
                    continue
                for p in cscf:
                    costPIH = cost_calculator(p, costs=costs)+costIH
                    parPIH = cscf[p] * parIH
                    if costPIH > minCost*weights[2] or parPIH < threshold:
                        continue
                    for s in cscf:
                        cost = cost_calculator(s, costs=costs) + costPIH
                        par = cscf[s] * parPIH
                        if cost > minCost*weights[3] or par < threshold:
                            continue
                        h_writer.writerow(to_write([p,s,i,h], par, cost))
                        if cost < minCost:
                            minCost = cost
    cache_file = open("CACHE", "a+")
    cache_file.write(str(input_hash) + ";" + id + "\n")
    cache_file.close()
    os.remove(filename)
    
def cost_calculator(configuration, costs=[0.5,0.5,0.5]):
    cost=0
    for i in range(0,7,2):
        if int(configuration[i]) != 0:
            cost = cost + costs[1] + costs[2] + costs[0]*int(configuration[i])
    return cost

def to_write(configuration,result,cost):
    to_write=[]
    for j in range(4):
        for k in range(0,len(configuration[j]),2):
            to_write.append(configuration[j][k])
    to_write.append(str(result))
    to_write.append(str(cost))
    return to_write