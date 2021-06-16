function [Xhat_im,time]=SSSSwrap(Yim_cell,varargin)

mtf= [.32 .26 .28 .24 .38 .34 .34 .26 .23 .33 .26 .22];
lam = 0.1;
mu = 0.1;
ksize = 13;
for i=1:2:(length(varargin)-1)
    switch varargin{i}
        case 'lam'
            lam=varargin{i+1};
        case 'mu'
            mu=varargin{i+1};
        case 'mtf'
            mtf=varargin{i+1};
        case 'mtf'
            mtf=varargin{i+1};
        case 'ksize'
            ksize=varargin{i+1};
    end
end

%% upsampling matrix
rv= [6 1 1 1 2 2 2 1 2 6 2 2]';
[C,D] = size(Yim_cell{2});
nb = length(Yim_cell);
Yim = zeros(C,D,nb);
for i=1:12
    topleft= zeros(rv(i),rv(i)); topleft(1,1)= 1;
    Yim(:,:,i)= kron(Yim_cell{i},topleft);
end

%% blurring matrix
dx= ksize; dy= ksize; % kernel filter support
limsub= 6; % due to BCCB convolution, one needs remove border (dx-1)/2
sdf= rv.*sqrt(-2*log(mtf)/pi^2)';
sdf(rv==1)= 0; % (dx,dy,sdf) define the blurring kenel 'fspecial('gaussian',[dx,dy],sdf(i))' of band i


%% algorithm
nr=120; nc=120;
if C>108
    nr=84;
end
if D>108
    nc=84; 
end
if C==198 && D==198
    nr=78;nc=78;
end

t0= clock;
for c = 1 : nr-2*limsub : C
	c2 = min(c + nr - 1, C);
	for d = 1 : nc-2*limsub : D
		d2 = min(d + nc - 1, D);
		[temp,~] = SSSS(Yim(c:c2, d:d2, :),rv,dx,dy,sdf,lam,mu);
        if c==1 && d==1
            Xhat_im(c:c2,d:d2,:)= temp(1:end,1:end,:);
        elseif c==1
            Xhat_im(c:c2,d+limsub:d2,:)= temp(1:end,1+limsub:end,:);
        elseif d==1
            Xhat_im(c+limsub:c2,d:d2,:)= temp(1+limsub:end,1:end,:);
        else
            Xhat_im(c+limsub:c2,d+limsub:d2,:)= temp(1+limsub:end,1+limsub:end,:);
        end
    end
end
time=etime(clock,t0)
