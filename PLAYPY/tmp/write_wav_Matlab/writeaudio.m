function writeaudio(time, signal, outputLoc)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
fs=1/(time(2)-time(1));
fs=round(fs);
n = length(time);
signal_fft= fft(signal);
f = fs*(0:n-1)/n;
plot(f(1:n/2),abs(signal_fft(1:n/2)))
audiowrite([outputLoc '.wav'],signal,fs)
end

