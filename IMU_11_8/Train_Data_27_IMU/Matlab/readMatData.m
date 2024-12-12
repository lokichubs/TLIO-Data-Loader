% Column 1 (Equipment):1 is WTLeft_foot(ed:6b:47:60:be:bc)(ed:6b:47:60:be:bc)   2 is WTRight_foot(c2:22:89:2b:7b:c3)(c2:22:89:2b:7b:c3)   3 is WTDRS(dc:64:37:61:c5:65)(dc:64:37:61:c5:65)   
% Column 2:Chip Time   The interval (in seconds) between each piece of data and the start time, with the start time as the starting point
% Column 3:Acceleration X(g)
% Column 4:Acceleration Y(g)
% Column 5:Acceleration Z(g)
% Column 6:Angular velocity X(°/s)
% Column 7:Angular velocity Y(°/s)
% Column 8:Angular velocity Z(°/s)
% Column 9:Angle X(°)
% Column 10:Angle Y(°)
% Column 11:Angle Z(°)
% Column 12:Magnetic field X(ʯt)
% Column 13:Magnetic field Y(ʯt)
% Column 14:Magnetic field Z(ʯt)
% Column 15:Temperature(℃)
% Column 16:Quaternions 0
% Column 17:Quaternions 1
% Column 18:Quaternions 2
% Column 19:Quaternions 3
% 函数调用：a=readMatData;
function d = readMatData(file)

    if nargin<1
        disp('默认数据')
        file='data.mat';
    else
        disp(file);
    end

    disp('加载mat文件')
    load('data.mat')
    S=whos;
    len = length(S)-1;
    dend = eval(S(len).name);
    d1 = eval(S(1).name);
    len_m = length(d1);
    len_n = length(d1(1,:));

    d=zeros(len_m*(len-1)+length(dend),len_n);
    %h=waitbar(0,'数据合并中……');
    for i=1:len-1
        dTemp = eval(S(i).name);
        d(len_m*(i-1)+1:len_m*i,:)=[dTemp];
        m=len-1;
        %p=fix(i/(m)*len_m)/100; %这样做是可以让进度条的%位数为2位
        %str=['正在合并，目前进度为 ',num2str(p),' %，完成 ',num2str(i),'/',num2str(m)];%进度条上显示的内容
        %waitbar(i/m,h,str);
    end
    d(len_m*(len-1)+1:len_m*(len-1)+length(dend),:)=dend;

end