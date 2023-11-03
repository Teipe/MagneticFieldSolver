import pandas
import numpy as np
import matplotlib.pyplot as plt
import cmath


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

### Get timebase
time = 399.2e-9
samples = 998
xAxis = np.linspace(0, time, num=998)

# df = pandas.read_csv(f'C:\\ProsjektOppgave\\emfi-studies\\_results_ZCentral\\20231027-133851\\raw_dumps\\150V\\width_80\\150_66.0,154.9,10_0.csv')
df = pandas.read_csv(f'C:\\ProsjektOppgave\\emfi-studies\\_results_ZCentral\\20231027-143843\\raw_dumps\\150V\\width_80\\150_66.0,154.9,10_0.csv')    
# df = pandas.read_csv(f'C:\\ProsjektOppgave\\emfi-studies\\_results_SetupCurrent\\20231025-131042\\raw_dumps\\400V\\width_80\\400_10,200,30_0.csv')
chA = df['Channel A'] #you can also use df['column_name']
chC = df['Channel C'] #you can also use df['column_name']
square = [0]*449 + [5]*300 + [0]*249
# chC = df['Channel C'] #you can also use df['column_name']

from numpy.fft import fft, ifft, fftfreq
# chA = moving_average(chA, 10)
Xid = fft(square)
XrealA = fft(chA)
XrealC = fft(chC)
N = len(square)
# N = len(square)
# n = np.arange(N)
# sr = time/samples
# T = N/sr
# freq = n/T 
freq = fftfreq(N, d=time/samples)

print(XrealA)

N = 5
radius = 4e-3/2
A = np.pi*radius**2
mu0  = 1.257e-6  #m kg s**-2 A**-2
mu = mu0*3000
l = 6e-3
ZL = mu*N**2*A/l
radius = 1e-3/2
A = np.pi*radius**2
ZL2 = mu*N**2*A/l
print(f'L2 = {ZL2*1e6} [nH]')
print(f'L = {ZL*1e6} [nH]')
print(f'L/L2 = {ZL/ZL2}')
print(f'L2/L = {ZL2/ZL}')
R = 1

squareApprox = 0
currentApprox = 0
for i, amplitude in enumerate(XrealA):
    sinusoidV = 1/(len(xAxis)*1/2)*(abs(amplitude)*np.cos(freq[i]*2*np.pi*xAxis+cmath.phase(amplitude)))
    sinusoidI = (1/(len(xAxis)*1/2)*(abs(amplitude)*np.cos(freq[i]*2*np.pi*xAxis+cmath.phase(amplitude))))/(R+ZL2*freq[i])
    squareApprox += sinusoidV
    currentApprox += sinusoidI


plt.figure()
plt.subplot(121)
plt.plot(chC)
plt.subplot(122)
plt.plot(squareApprox)
plt.show()

# plt.figure(figsize = (12, 6))
# plt.subplot(321)

# plt.stem(freq/1e9, np.abs(Xid), 'b', \
#          markerfmt=" ", basefmt="-b")
# # plt.yscale('log')
# plt.xlabel('Freq (Hz)')
# plt.ylabel('FFT Amplitude |X(freq)|')
# # plt.xlim(0, 10)

# plt.subplot(322)
# plt.plot(xAxis*1e9, ifft(Xid), 'r')
# plt.xlabel('Time (ns)')
# plt.ylabel('Amplitude')
# plt.tight_layout()

# plt.subplot(323)
# plt.stem(freq/1e9, np.abs(XrealA), 'b', \
#          markerfmt=" ", basefmt="-b")
# # plt.yscale('log')
# plt.xlabel('Freq (GHz)')
# plt.ylabel('FFT Amplitude |X(freq)|')
# # plt.xlim(0, 10)

# plt.subplot(324)
# plt.plot(xAxis*1e9, ifft(XrealA), 'r')
# plt.xlabel('Time (ns)')
# plt.ylabel('Amplitude')
# plt.tight_layout()

# plt.subplot(325)
# plt.stem(freq/1e9, np.abs(XrealC), 'b', \
#          markerfmt=" ", basefmt="-b")
# # plt.yscale('log')
# plt.xlabel('Freq (GHz)')
# plt.ylabel('FFT Amplitude |X(freq)|')
# # plt.xlim(0, 10)

# plt.subplot(326)
# plt.plot(xAxis*1e9, ifft(XrealC), 'r')
# plt.xlabel('Time (ns)')
# plt.ylabel('Amplitude')
# plt.tight_layout()
# plt.show()