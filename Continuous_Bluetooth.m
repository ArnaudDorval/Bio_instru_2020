

clear;
myDataSet = [0 0];
RawData = "rawData";

hc06 = bluetooth("HC-06", 1);

configureCallback(hc06, "string", 10, @collectData);

disp(hc06.UserData);

function collectData(src, evt)
    % Read received data and store it in the UserData property on the bluetooth object
    src.UserData = [src.UserData; read(src,src.BytesAvailableFcnCount)];
end
