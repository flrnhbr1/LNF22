clear

Path = '/Users/florianhuber/Documents/MATLAB/LNF/logs/fig_8.csv';

% Get Waypoint from csv sheet
Table = readtable(Path);
time = table2array(Table(:, 2));
x_drone = table2array(Table(:, 3));
y_drone = table2array(Table(:, 4));
z_drone = table2array(Table(:, 5));

length = size(x_drone, 1);


figure
plot(x_drone, 'red')
grid
hold on
plot(y_drone,'green')
plot(z_drone,'blue')
title 'Drone position in x-y-z'
xlabel 'time [s]'
ylabel 'position [m]'
legend 'x' 'y' 'z'
hold off

figure
plot3(x_drone, z_drone, y_drone, 'LineWidth',2)
grid
title 'Trajectory'
legend 'Drone'

