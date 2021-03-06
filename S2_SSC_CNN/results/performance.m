%% 
clear all
close all
clc
%%%%%%%%%%%Coastal%%%%%%%%%%
addpath('/home/han/PycharmProjects/Pansharpening Project/data')
addpath('/home/han/PycharmProjects/Pansharpening Project/help_functions')
addpath('ATPRK')
%% Load coastal cell
% load coastalA_cell_RR.mat 
% xref=Xm_im;
% load skipnetpanshapen_c.mat
% xskip=double(xpr); %predicted img skip net
% load resnetpanshapen_c.mat
% xres=double(xpr); %predicted img resnet
%% Load reykjavik data
load reykjavik_cell.mat % cell for ATPRK
xref=Xm_im;
load skipnetpanshapen_r.mat
xskip=double(xpr); %predicted img skip net
load resnetpanshapen_r.mat
xres=double(xpr); %predicted img resnet

%% ATPRK
for i=1:12
    Yim{i}=double(Yim{i});
end
Z=ATPRKwrap(Yim);
%% Reconstructed images (Fig. 4 in the paper)
band=["5","6","7","8a","11","12"];
ha = tight_subplot(2,4,.01,0.06,0.06);
axes(ha(1)); imagesc(xref(:,:,1));colormap gray; axis image;axis off;
title('Reference','FontSize',6)
axes(ha(2)); imagesc(Z(:,:,1));colormap gray; axis image;axis off;
title('ATPRK','FontSize',6)
axes(ha(3)); imagesc(xres(:,:,1));colormap gray; axis image;axis off;
title('ResNet','FontSize',6)
axes(ha(4)); imagesc(xskip(:,:,1));colormap gray; axis image;axis off;
title('SSC-CNN','FontSize',6)
axes(ha(5)); imagesc(xref(:,:,2));colormap gray; axis image;axis off;
axes(ha(6)); imagesc(Z(:,:,2));colormap gray; axis image;axis off;
axes(ha(7)); imagesc(xres(:,:,2));colormap gray; axis image;axis off;
axes(ha(8)); imagesc(xskip(:,:,2));colormap gray; axis image;axis off;
% % 
% axes(ha(1));ylabel('Reference','FontSize',6,'FontWeight','bold');
% axes(ha(3));ylabel('SkipNet','FontSize',6,'FontWeight','bold');
% axes(ha(5));ylabel('ResNet','FontSize',6,'FontWeight','bold');
% axes(ha(7));ylabel('ATPRK','FontSize',6,'FontWeight','bold');
%% Residual images (Fig. 3 in the paper)
band=["5","6","7","8a","11","12"];
ha = tight_subplot(3,2,[.005 .005],0.06,0.06);
rZ=abs(Z-xref);
rres=abs(xres-xref);
rskip=abs(xskip-xref);
bottom=min(log(rZ(:)+1));
top=max(log(rZ(:)+1));
for i=1:2
    axes(ha(i)); imagesc(log(1+rZ(:,:,i)),[bottom top]);axis image;axis off;colorbar;
    title(strcat("Band ",band(i)),'FontSize',8)
    axes(ha(i+2)); imagesc(log(1+rres(:,:,i)),[bottom top]);axis image;axis off;colorbar;
    axes(ha(i+2*2)); imagesc(log(1+rskip(:,:,i)),[bottom top]);axis image;axis off;colorbar;
end
%% calculate SSIM, SAM, PSNR
[r,c,d]=size(xref);
SSIM_skip=zeros(d, 1);
SSIM_res=zeros(d, 1);
SSIM_at=zeros(d, 1);
for i=1:d
    SSIM_skip(i,1)=ssim_index(xref(:,:,i),xskip(:,:,i));
    SSIM_res(i,1)=ssim_index(xref(:,:,i),xres(:,:,i));
    SSIM_at(i,1)=ssim_index(xref(:,:,i),Z(:,:,i));
end
[sam_skip,~]=SAM(xref,xskip);
[sam_res,~]=SAM(xref,xres);
[sam_at,~]=SAM(xref,Z);

[SREvec_skip,aSRE_skip]=sre(xref,xskip);
[SREvec_res,aSRE_res]=sre(xref,xres);
[SREvec_at,aSRE_at]=sre(xref,Z);

disp([sam_skip,sam_res,sam_at]);
disp([SREvec_skip',SREvec_res',SREvec_at']);
disp([aSRE_skip,aSRE_res,aSRE_at]);
disp([SSIM_skip, SSIM_res,SSIM_at]);
disp([mean(SSIM_skip),mean(SSIM_res),mean(SSIM_at)]);