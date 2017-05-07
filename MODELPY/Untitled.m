%% COMPLETE LINNEAR TRANSFER FUNCTION

%%%%%%%%%% MECHANICAL SYSTEM %%%%%%%%%%
% Transfer function from acceleration to amplitude of vibration.
% System is governed by equation: mz'' + dz' + kz = -my''
% m: mass of magnet, d: damping coefficient (assuming constant)
% k: damping coefficient (Sssuming constant which might be a bad
%   approximation. Otherwise the system is not linnear)
% z: amplitude of spring (z = x-y where x is the position of the mass
%   with respect to the frame of the harvester)
% y: position of harvester in space

m = 1; %NOT KNOWN ATM
d = 1; %NOT KNOWN ATM
k = 1; %NOT KNOWN ATM

numerator_mech = [0 0 -m];
denominator_mech = [m d k];

G_mech = @(s) -m*s.^2./(m*s.^2 + d*s + k);

%%%%%%%%%% ELECTRIC SYSTEM %%%%%%%%%%

%CIRCUIT
%   ---L_coil---R_coil---
%   |                   |
%   NBl*z'               R_load
%   |                   |
%   ---------------------

% Governing equation: L_coil*i' +(R_coil+R_load)*i = -NBl*z'

N = 1; % Number of turns in coil
B = 1; % Total magnetic field perpendicular to coils
R_load = 1; % Load resistance
R_coil = 1; % Coil resistance
L_coil = 1 + 1i; % Induction in coil
l = 1; % Radius of coil

G_electric = @(s) -N*B*l*R_load*s./(L_coil*s + R_coil + R_load);

%%%%%%%%%%% TOTAL SYSTEM %%%%%%%%%%
G = @(s) G_mech(s)*G_electric(s);





