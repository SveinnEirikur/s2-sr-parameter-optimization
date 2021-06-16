function RGB=sentinel2RGB(Y,thresholdRGB)
% Y - a sentinel image with B2,B3 and B4
% thresholdRGB =1, then the tail
%    and head of RGB values are removed.
%   This increases contrast 


[ydim,xdim,zdim]=size(Y);
Y=reshape(Y,ydim*xdim,zdim)';
Y=Y./max(Y(:));

% T matrix from "Natural color representation of Sentinell-2 data " paper
T=[0.180 0.358 0.412
   0.072 0.715 0.213
   0.950 0.119 0.019];


XYZ=T*Y;

% Convert to RGB
M=[ 3.2404542 -1.5371385 -0.4985314;
   -0.9692660  1.8760108  0.0415560;
    0.0556434 -0.2040259  1.0572252];
sRGB=M*XYZ;


% Correct gamma 
gamma_map = (sRGB >  0.0031308);
sRGB(gamma_map) = 1.055 * power(sRGB(gamma_map), (1. / 2.4)) - 0.055;
sRGB(~gamma_map) = 12.92*sRGB(~gamma_map);
sRGB(sRGB>1)=1;
sRGB(sRGB<0)=0;

if (thresholdRGB>0)
thres=0.01;
for idx=1:3
    y=sRGB(idx,:);
    [a,b]=hist(y,100);
    a=cumsum(a)/sum(a);
    th=b(1);
    i=find(a<thres);
    if ~isempty(i)
    th=b(i(end));
    end
    y=max(0,y-th);

    
    [a,b]=hist(y,100);
    a=cumsum(a)/sum(a);    
    i=find(a>1-thres);
    th=b(i(1));
    y(y>th)=th;
    y=y./th;
    sRGB(idx,:)=y;
end
end

RGB(:,:,1)=reshape(sRGB(1,:),ydim,xdim);
RGB(:,:,2)=reshape(sRGB(2,:),ydim,xdim);
RGB(:,:,3)=reshape(sRGB(3,:),ydim,xdim);


end

















