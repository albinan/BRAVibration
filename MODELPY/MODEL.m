figure
subplot(2,1,1)
loglog(Frequency02,RMS_V02./RMS_g02)
legend('a = 0.2g')
hold on
loglog(Frequency04,RMS_V04./RMS_g04)
legend('a = 0.4g')
loglog(Frequency06,RMS_V06./RMS_g06)
legend('a = 0.6g')
loglog(Frequency08,RMS_V08./RMS_g08)
legend('a = 0.6g')
grid on

freq = (Frequency02 + Frequency04 + Frequency06 + Frequency08)/4;
G_abs = (RMS_V02./RMS_g02 + RMS_V04./RMS_g04 + RMS_V06./RMS_g06 + RMS_V08./RMS_g08)/4;
Phase = (Phase_V02 + Phase_V04 + Phase_V06 + Phase_V08)/4;
plot(freq,G_abs, 'o','Color', 'black' )



% Phase flips between -
subplot(2,1,2)
plot(Frequency02,Phase_V02)
legend('a = 0.2g')
hold on
plot(Frequency04,Phase_V04)
legend('a = 0.4g')
plot(Frequency06,Phase_V06)
plot(Frequency08,Phase_V08)
plot(freq, Phase, 'o','Color','black')
ylim([-180 180])
%%
figure
loglog(freq,G_abs)
grid on
