
t = linspace(0,60,100000);
y = sin(50*2*pi*t);
audiowrite('50Hz.wav',y,floor(1/(t(2)-t(1))))