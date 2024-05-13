function runMySimulation
    fig = uifigure('Name', 'Simulation Controls');
    startBtn = uibutton(fig,'push', 'Text', 'Start Simulation', 'Position',[100, 100, 100, 22], 'ButtonPushedFcn', @(btn,event) startSimulation());
end

function startSimulation()
    disp('Simulation started');
    % Insert code here to initialize and run your simulation
end
