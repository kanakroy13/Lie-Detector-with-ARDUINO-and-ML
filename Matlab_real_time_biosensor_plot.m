clc;
clear;
close all;

% Set up serial communication (Change 'COMX' to match your Arduino port)
arduino = serialport('COM3', 9600); % Example: 'COM3' on Windows or '/dev/ttyUSB0' on Linux

% Set buffer size to avoid delays
configureTerminator(arduino, "LF"); % Ensures line-by-line reading
flush(arduino); % Clear any old data

% Initialize figure and plots
figure;
hold on;
grid on;
xlabel('Time (s)');
ylabel('Values');
title('Real-Time Heart Rate , Temperature Monitoring , GSR and piezo READINGS');

% Create animated lines for instant updates
h1 = animatedline('Color', 'r', 'LineWidth', 1.5); % BPM
h2 = animatedline('Color', 'b', 'LineWidth', 1.5); % Avg BPM
h3 = animatedline('Color', 'g', 'LineWidth', 1.5); % Rapid Changes
h4 = animatedline('Color', 'k', 'LineWidth', 1.5); % Temperature
h5 = animatedline('Color', 'y', 'LineWidth', 1.5); % gsr 
h6 = animatedline('Color', 'c', 'LineWidth', 1.5); % piezoelectric
legend('BPM', 'Avg BPM', 'Rapid Changes', 'Temperature (°C)','GSR','piezoelectric');
ylim([0 120]); % Adjust based on expected values

% Variables to track time range
time_min = Inf;
time_max = -Inf;

% Infinite loop for real-time plotting
while true
    dataLine = readline(arduino); % Read one line from Arduino
    data = str2double(split(dataLine, ',')); % Convert CSV to numeric array

    if length(data) == 7 && all(~isnan(data)) % Ensure valid numeric data
        % Extract data values
        time = data(1);
        bpm = data(2);
        avgBpm = data(3);
        rapidChanges = data(4);
        temperature = data(5);
        GSR = data(6);
        piezoelectric = data(7);

        % Update time range
        time_min = min(time_min, time);
        time_max = max(time_max, time);

        % Update plots instantly
        addpoints(h1, time, bpm);
        addpoints(h2, time, avgBpm);
        addpoints(h3, time, rapidChanges);
        addpoints(h4, time, temperature);
        addpoints(h5, time, GSR);
        addpoints(h6, time, piezoelectric);
        % Ensure xlim remains valid and increasing
        if time_max > time_min
            xlim([max(0, time_max - 30), time_max]); % Show last 30s of data
        end

        drawnow limitrate; % Fast, optimized real-time update
    end
end
