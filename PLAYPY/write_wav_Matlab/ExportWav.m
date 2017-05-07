%% Import x y and z acceleration
x = vx;
x = x - mean(x);
timescale = 0.000001;
t_s = (0:length(t)-1)*((t(end)-t(1))/(length(t)-1))'*timescale;
t_s = t_s';
plot(t_s,x)
hold on
disp(t_s(end)-t_s(1))
disp((t(end)-t(1))*timescale)
grid on
%%
a = vx;
v = cumtrapz(a,t_s);
x = cumtrapz(v,t_s);
%plot(t_s,a,'.')
hold on
plot(t_s,v,'.')
plot(t_s,x,'.')
%% Create sound file with 41000 Hz sample frequency (Default speaker frequency)
a_m = vx; % Measured acceleration spectrum
t_m = t_s(end)-t_s(1); % Measured time spectrum
delta_t_m = (t_s(2)c-t_s(1))/1; 
fs_m = 1/delta_t_m % Measured sample frequency
n_m = length(t_s);
a_fft_m = fft(a_m);

fs_w = 41000;
n = round(t_m*41000) - n_m

a_fft_w = padarray(a_fft_m, n, 'post');
a_w = ifft(a_fft_w);
t_w = (0:length(a_w)-1)*t_m/length(a_w);

delta_t_w = (t_w(2)-t_w(1))/2;
fs_w_prime = 1/delta_t_w

t_w = t_w';

q = rms(a_m)/rms(a_w);
a_w = a_w*q;
plot(t_s,a_m,'o');
hold on
plot(t_w, a_w,'.')
%%
writeaudio(t_w ,a_w, 'acc_44100')