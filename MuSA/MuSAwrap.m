function [Xhat_MuSA, time] = MuSAwrap(Yim, varargin)

% include actual code 
    mfilepath=fileparts(which(mfilename));
    addpath(fullfile(mfilepath,'./Utilities'));
    addpath(fullfile(mfilepath,'./bm3d'));

% parameters
    mu = 0.6 ;
    nb = 12;
    niters   = 130; 
    iters_pp = 30; 
    tau =  0.005;
    p = 5;
    mtf = [ .32 .26 .28 .24 .38 .34 .34 .26 .23 .33  .26 .22 ];

    for i=1:2:(length(varargin)-1)
        switch varargin{i}
            case 'tau'
                tau=varargin{i+1};
            case 'mu'
                mu=varargin{i+1};
            case 'mtf'
                mtf=varargin{i+1};
            case 'niters'
                niters=varargin{i+1};
            case 'iters_pp'
                iters_pp=varargin{i+1};
            case 'nb'
                nb=varargin{i+1};
            case 'p'
                p=varargin{i+1};
        end
    end
    
% subsampling factors (in pixels)
    d = [6 1 1 1 2 2 2 1 2 6 2 2]';
% convolution  operators (Gaussian convolution filters)
    sdf = d.*sqrt(-2*log(mtf)/pi^2)'; 
    sdf(d==1) = 0;
% remove border for computing the subspace
    limsub = 9;
% kernel filter support
    dx = 12;
    dy = 12;

% reshape cell array if necessary
    L=length(Yim);
    Yim=reshape(Yim,L,1);
    for i=1:L, Yim{i}=double(Yim{i}); end

[ Yim2, av ] = normaliseData(Yim);          
[ nl,nc ] = size(Yim{2});
n = nl*nc;

FBM = createConvKernel(sdf,d,nl,nc,nb,dx,dy); % Define blurring operators
FBM2 = createConvKernelSubspace(sdf,nl,nc,nb,dx,dy); % The same for computing the subspace

t0= clock;

%=================================================================
% Calculate Subspace E
%=================================================================

Y1im = zeros(nl,nc,nb); % Generate LR MS image for Subspace

     for i = 1:nb
         Y1im(:,:,i) = imresize(Yim2{i},d(i)); % Upsample image via interpolation
     end

Y1 = conv2mat(Y1im,nl,nc,nb);
Y2 = ConvCM( Y1,FBM2,nl,nc,nb );% Y2 interpolated images blurred to the same ammount (for subspace)
Y2im = conv2im( Y2,nl,nc,nb);
Y2n = conv2mat( Y2im(limsub+1:end-limsub,limsub+1:end-limsub,:));

[ E2,~ ] = svd(Y2n*Y2n'/n); % Y2n is the image for subspace with the removed border
E = E2(:,1:p);

%=================================================================
% Subsampling (inserT zeros)
%=================================================================
              
[~, Y] = createSubsampling(Yim2,d,nl,nc,nb);
Yim = conv2im(Y,nl,nc,nb);
p = size(E,2);
n = nl*nc;
FBMC = conj(FBM);
BTY =  ConvCM(Y,FBMC,nl);

IF = 0*FBM;

% build the invserse filter in frequece with subsampling
     for i=1:nb
         Fim = abs(FBM(:,:,i)).^2;
         Fpatches = im2col(Fim,[nl/d(i),nc/d(i)],'distinct');
         [~,p2] = size(Fpatches);
         Fpatches = 1./(sum(Fpatches,2)/mu + d(i)^2);   % inv(d^2*I +(1/lambda)*D'*abs(S).^2D)  (image forma)
         aux = col2im(repmat(Fpatches,1,p2),[nl/d(i),nc/d(i)], [nl,nc],'distinct');   % D*ans*D' (image format)
         Fim =  Fim.*aux;
         IF(:,:,i) = Fim;  
     end
     
%=================================================================
% Solver
%=================================================================
Z = zeros(p,n);
V1 = zeros(nb,n);
D1 = V1;
V2 = zeros(p,n);
D2 = V2;
sigmaRGB = zeros(niters,3);
                % ADMM
                for i = 1:niters
                    %  min (1/2)||(U kron I))*z - v1 -d1 ||^2 +  (1/2)||z - v2 -d2 ||^2
                    %   z

                    Z = (1/2)*(E'*(V1+D1) + (V2+D2)) ;

                    %  min(1/2)|| M*B*v1 - y||^2 + (mu/2)||(U kron I))*z - v1 -d1 ||^2
                    %   v

                    % matrix format
                    NU1 = E*Z-D1;
                    AUX = BTY+mu*NU1;
                    V1 = AUX/mu - ConvCM(AUX,IF,nl,nc,nb)/mu^2;

                    % solve V2 with Plus and Play prior
                    % min tau/2 phi(V2)  + (mu/2)||Z - V2 -D2 ||^2
                    NU2 =  Z-D2;
                    V2 = NU2;
                    % plug and play bm3d
                    
                        if i > iters_pp
                             V2im = reshape(NU2',nl,nc,p);
                             for k=1:1:p
                                %colour green
                                auxim1 = V2im(:,:,k);
                                % set transform to [0 1]
                                max_im1 = max(auxim1(:));
                                min_im1 = min(auxim1(:));
                                scale1 = max_im1 - min_im1;
                                auxim1 = (auxim1 - min_im1)/scale1;

                                Yim_clean = synthetize_pan(auxim1,Yim(:,:,[2 3 4 8]));
                                max_im = max(Yim_clean(:));
                                min_im = min(Yim_clean(:));
                                scale = max_im - min_im;
                                Yim_clean = (Yim_clean - min_im)/scale;

                                yRGB(:,:,1) = Yim_clean;
                                yRGB(:,:,2) = auxim1;
                                yRGB(:,:,3) = auxim1;

                                sigmaRGB(i,:) = [1e-4 1/scale1 1/scale1]*sqrt(tau/mu); % [0,1] instead of [0,255]

                                yRGB_est = CBM3D(yRGB, sigmaRGB(i,:)); % Doesn't return PSNR
                                auxim1 = yRGB_est(:,:,2);
                                auxim1 = auxim1*scale1 + min_im1;
                                V2im(:,:,k) = auxim1;

                            end
                            V2 = reshape(V2im,nl*nc,p)';
                        end

                        % fprintf('iter = %d, ||EZ-V1|| = %2.2f, ||X-V2|| = %2.2f, \n',i, ...
                        %                      norm(NU1+D1-V1, 'fro'), norm(NU2+D2-V2, 'fro'))

                        % update Lagrange multipliers
                        D1 = -NU1 + V1;
                        D2 = -NU2 + V2;

                end
                
Xhat = E*Z;
Xhat_im = conv2im(Xhat,nl,nc,nb);

time=etime(clock,t0)

Xhat_MuSA = unnormaliseData(Xhat_im,av);

