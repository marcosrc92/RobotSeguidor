s = serial('COM1','BaudRate',9600)

s.ReadAsyncMode = 'continuous'
 
s.BytesAvailableFcnCount = 733;
s.BytesAvailableFcnMode = 'byte';

s.Tag = 'sick';
s.DataTerminalReady='off';

s.InputBufferSize=733;
  
fopen(s)

msg_reset={'02' '00' '01' '00' '10' '34' '12'}; % reset

h=hex2dec(msg_reset);
fwrite(s,h,'uint8','async');

msg_on=['02' '80' '17' '00' '90'... 
    '4C' '4D' '53' '32' '30' '30' '3B' '33' '30' '31' '30' '36' '33' '3B' '56' '30' '32' '2E' '31' '30' '20' '10'...
    '63' '5E'];% Power-on

% h=hex2dec(msg_on);
% fwrite(s,h,'uint8','async');

a=[];
    
    while (~strcmp(a(:)',msg_on))
        % Vaciar el puerto 
        % OJO!!! Los datos se perderan
        if(s.BytesAvailable>0)
            pause(0.1)
            disp(['>>> AVISO: Se descartaran ' int2str(s.BytesAvailable) ' datos']);
            ack=fread(s, s.BytesAvailable,'uint8');
            a=dec2hex(ack)';
        end
    end
    disp('Sick reseteado')



while (1)

msg_data={'02' '00' '02' '00' '30' '01' '31' '18'}; %comando para obligarle a mandar datos
msg_hex=hex2dec(msg_data); %conversion a hexadecimal
fwrite(s,msg_hex,'uint8','async');

  while(s.BytesAvailable<733)
        pause(0.01)
    end

[ack1,cnt,ms]=fread(s,733,'uint8');
newData=ack1(7:end-3); %quita la cabecera

len=length(newData);
    
dis=[];
for i=1:2:len
	dis=[dis newData(i)+newData(i+1)*256];
end

ang=0:pi/361:pi;
    
X=cos(ang).*dis;
Y=sin(ang).*dis;

plot(X,Y)
axis([-8000 8000 0 8000])    
grid on
grid minor

end