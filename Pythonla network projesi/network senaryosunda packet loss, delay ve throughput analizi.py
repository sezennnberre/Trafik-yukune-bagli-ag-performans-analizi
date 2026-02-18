# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 19:28:01 2026

@author: sezen
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# simülasyon parametreleri
simulation_time = 20 #saniye
time_step = 0.001 

packet_size = 1500 * 8 #bitler
#link_capacity = 50e6 # 50 Mbps sabit kapasite
buffer_size = 1000 #paketler

arrival_rates = [400, 500, 600] #3 istemci için saniyede paket sayısı
# biz discrete-time simülasyon yapacağız.
# her zaman adımında 1.yeni paket var mı?, 2.kuyruğa ekle, 3.link boşsa gönder, 4.buffer doluysa drop
def run_simulation(arrival_multiplier=1):
    base_snr = 20
    load = arrival_multiplier
    snr_linear = base_snr * np.exp(-load)

    bandwidth = 10e6
    link_capacity = bandwidth * np.log2(1 + snr_linear)
    
    queue = deque()
    dropped = 0
    delivered = 0
    delays = []
    
    current_time = 0
    link_busy_until = 0
    
    #trafik yükünü değiştir
    rates = [r * arrival_multiplier for r in arrival_rates]
    
    while current_time < simulation_time:
        
        #Paket üretici
        for rate in rates:
            arrivals = np.random.poisson(rate * time_step)   #poisson kullandım
            for _ in range(arrivals):
                if len(queue) < buffer_size:
                    queue.append(current_time)
                else:
                    dropped += 1
                    
                    
        #Aktarma
        if current_time >= link_busy_until and len(queue) > 0:
            arrival_time = queue.popleft()
            tx_time = packet_size / link_capacity
            link_busy_until = current_time + tx_time
            delay = link_busy_until - arrival_time
            delays.append(delay)
            delivered += 1
            
            
        current_time += time_step
        
    avg_delay = np.mean(delays) if delays else 0
    packet_loss = dropped / (dropped + delivered) if (dropped + delivered) > 0 else 0
    throughput = delivered * packet_size / current_time
    
    return avg_delay, packet_loss, throughput

loads = [0.5, 1, 1.5, 2]
delays = []
losses = []
throughputs = []

for load in loads:
    d, l, t = run_simulation(load)
    delays.append(d)
    losses.append(l)
    throughputs.append(t)

#Delay için    
plt.figure()
plt.plot(loads, delays)
plt.xlabel("Traffic Load Multiplier")
plt.ylabel("Average Delay (s)")
plt.title("Traffic Load vs Delay")
plt.show()

#Packet loss için
plt.figure()
plt.plot(loads, losses)
plt.xlabel("Traffic Load Multiplier")
plt.ylabel("Packet Loss Rate")
plt.title("Traffic Load vs Packet Loss")
plt.show()

#Throughput için 
plt.figure()
plt.plot(loads, throughputs)
plt.xlabel("Traffic Load Multiplier")
plt.ylabel("Throughput (bps)")
plt.title("Traffic load vs Throughput")
plt.show()











