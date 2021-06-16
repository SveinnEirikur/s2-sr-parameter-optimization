function [Z, alltime] = ATPRKwrap(Yim, varargin)
%%%%This is the code for ATPRK produced by Dr Qunming Wang; Email: wqm11111@126.com
%%%%Copyright belong to Qunming Wang
%%%%When using the code, please cite the fowllowing papers
%%%%Q. Wang, W. Shi, Z. Li, P. M. Atkinson. Fusion of Sentinel-2 images. Remote Sensing of Environment, 2016, 187: 241�C252.
%%%%Q. Wang, W. Shi, P. M. Atkinson, Y. Zhao. Downscaling MODIS images with area-to-point regression kriging. Remote Sensing of Environment, 2015, 166: 191�C204.

%%%%%The synthesized scheme in ATPRK amounts to the use of all 10m bands
% reshape cell array if necessary
L=length(Yim);
Yim=reshape(Yim,L,1);
[nr,nc] = size(Yim{2});
for i=1:L, Yim{i}=double(Yim{i}); end

s=2;

d = [6 1 1 1 2 2 2 1 2 6 2 2]';
ind = find(d==2);
for i=1:numel(ind)
    I_MS(:,:,i)=Yim{ind(i)};
end
ind = find(d==6);
for i=1:numel(ind)
    I_60(:,:,i)=Yim{ind(i)};
end

ind = find(d==1);
for i=1:numel(ind)
    I_PAN(:,:,i)=Yim{ind(i)};
end

w=1;
sigma=s/2;
PSFh=PSF_template(s,w,sigma);%%%Gaussian PSF
%PSFh=zeros((2*w+1)*s,(2*w+1)*s);PSFh(w*s+1:w*s+s,w*s+1:w*s+s)=1/s^2;%%%Ideal square wave PSF

Sill_min=1;
Range_min=0.5;
L_sill=20;
L_range=20;
rate=0.1;
H=20;

for i=1:2:(length(varargin)-1)
        switch varargin{i}
            case 'Sill_min'
                Sill_min=varargin{i+1};
            case 'r'
                r=varargin{i+1};
            case 'Range_min'
                Range_min=varargin{i+1};
            case 'L_sill'
                L_sill=varargin{i+1};
            case 'L_range'
                L_range=varargin{i+1};
            case 'rate'
                rate = varargin{i+1};
            case 'H'
                H = varargin{i+1};
        end
    end
    
tic
Z = nan(nr,nc,L);
Z20 = nan(nr,nc,6);
Z60 = nan(nr,nc,2);

for i=1:6
    [~,~,Z0]=ATPRK_MSsharpen(I_MS(:,:,i),I_PAN,Sill_min,Range_min,L_sill,L_range,rate,H,w,PSFh);
    Z20(:,:,i)=Z0;
end

s=6;
w=1;
sigma=s/2;
PSFh=PSF_template(s,w,sigma);%%%Gaussian PSF
%PSFh=zeros((2*w+1)*s,(2*w+1)*s);PSFh(w*s+1:w*s+s,w*s+1:w*s+s)=1/s^2;%%%Ideal square wave PSF

for i=1:2
    [~,~,Z0]=ATPRK_MSsharpen(I_60(:,:,i),I_PAN,Sill_min,Range_min,L_sill,L_range,rate,H,w,PSFh);
    Z60(:,:,i)=Z0;
end

ind = find(d==1);
for i=1:numel(ind)
    Z(:,:,ind(i))=Yim{ind(i)};
end
ind = find(d==2);
for i=1:numel(ind)
    Z(:,:,ind(i))=Z20(:,:,i);
end

ind = find(d==6);
for i=1:numel(ind)
    Z(:,:,ind(i))=Z60(:,:,i);
end
alltime=toc;
