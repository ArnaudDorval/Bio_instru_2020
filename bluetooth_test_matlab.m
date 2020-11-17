%"HC-06"--"98D332202FDA"--1--"Requires pairing"
%98D332202FDA

%bluetoothlist;
clear;
myDataSet = [0 0];
RawData = "rawData";

hc06 = bluetooth("HC-06", 1);
write(hc06, "init");
a = read(hc06, 2, "string");
disp(a);
for index = 1:10
   write(hc06, "b");
   a = read(hc06, 13, "string");
   strn = regexprep(a,'[l]','');
   n = str2num(strn);
   %a = read(hc06, n + 1, "string");
   %RawData = [RawData; a];
end
disp(RawData);

%faut je parse le data
for i = RawData
   formatted = uint16( str2double( regexp( a, '\;', 'split' ) ) )
   myDataSet = [myDataSet; formatted];
end
disp(myDataSet);
clear hc06;




