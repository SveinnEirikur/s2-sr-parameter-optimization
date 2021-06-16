function output = sreval(Yim, Xhat_ims, Xm_im)
  output = struct('SAMm',[],'SAMm_2m',[],'SRE',[], ...
    'ERGAS_20m', [], 'ERGAS_60m', [], 'SSIM', [], 'aSSIM', [], ...
    'RMSE', []);
  L=length(Yim); % Fjöldi banda
  m = length(Xhat_ims);
  [nl,nc] = size(Yim{2}); % Spatial upplausn á B2
  n = nl*nc; % Fjöldi pixla í B2
  limsub = 2;
  [~, av] = normaliseData(Yim); % Meðaltal myndar
  d = [6 1 1 1 2 2 2 1 2 6 2 2]'; % Subsampling factor in pixels
  for mIDX = 1:m
      Xhat_im = Xhat_ims{mIDX};
      [output.SAMm(mIDX), output.SAMm_2m(mIDX), output.SRE{mIDX}, ...
          output.RMSE(mIDX), output.SSIM{mIDX}, output.aSSIM(mIDX), ...
          output.ERGAS_20m(mIDX), output.ERGAS_60m(mIDX)] ...
          = evaluate_performance(Xm_im,normaliseData(Xhat_im),nl,nc,L,limsub,d,av);
  end
end

function [SAMm, SAMm_2m, SRE, RMSE, SSIM_index, aSSIM, ERGAS_20m, ERGAS_60m] = evaluate_performance(Xm_im,Xhat_im,nl,nc,L,limsub,d,av)
    Xhat_im = Xhat_im(limsub+1:end-limsub,limsub+1:end-limsub,:);
    Xhat_im = unnormaliseData(Xhat_im,av);
    Xhat=reshape(Xhat_im,[(nl-4)*(nc-4),L]);
    % Xm_im is the ground truth image
    Xm_im = Xm_im(limsub+1:end-limsub,limsub+1:end-limsub,:); 
    if ( size(Xm_im,3) == 6 ) % Reduced Resolution
        ind = find( d==2 );
        SAMm=SAM(Xm_im,Xhat_im(:,:,ind));
        SAMm_2m=SAMm;
        X = conv2mat(Xm_im); 
        Xhat = conv2mat(Xhat_im);
        % SRE - signal to reconstrution error
        for i=1:6
            SRE(i,1) = 10*log10(sum(X(i,:).^2)/ sum((Xhat(ind(i),:)-X(i,:)).^2));
            SSIM_index(i,1) = ssim(Xm_im(:,:,i),Xhat_im(:,:,ind(i)));
        end
        aSSIM=mean(SSIM_index);
        ERGAS_20m = ERGAS(Xm_im,Xhat_im(:,:,ind),2);
        ERGAS_60m = nan;
        RMSE = norm(X - Xhat(ind,:),'fro') / size(X,2);
    else    
        ind=find(d==2 | d==6);
        SAMm=SAM(Xm_im(:,:,ind),Xhat_im(:,:,ind));
        ind2=find(d==2);
        SAMm_2m=SAM(Xm_im(:,:,ind2),Xhat_im(:,:,ind2));
        ind6=find(d==6);
        X = conv2mat(Xm_im); 
        Xhat = conv2mat(Xhat_im);
        % SRE - signal to reconstrution error
        for i=1:L
            SRE(i,1) = 10*log10(sum(X(i,:).^2)/ sum((Xhat(i,:)-X(i,:)).^2));
            SSIM_index(i,1) = ssim(Xm_im(:,:,i),Xhat_im(:,:,i));
        end
        aSSIM=mean(SSIM_index(ind));
        ERGAS_20m = ERGAS(Xm_im(:,:,ind),Xhat_im(:,:,ind),2);
        ERGAS_60m = ERGAS(Xm_im(:,:,ind2),Xhat_im(:,:,ind2),6);
        RMSE = norm(X(ind,:) - Xhat(ind,:),'fro') / size(X,2);
    end
end

function [Yim, av] = normaliseData(Yim)
    % Normalize each cell to unit power
    if iscell(Yim)
        % mean squared power = 1
        nb = length(Yim);
        for i=1:nb
            av(i,1) = mean2(Yim{i}.^2);
            Yim{i,1} = sqrt(Yim{i}.^2/av(i,1));
        end   
    else
        nb = size(Yim,3);
        for i=1:nb
            av(i,1) = mean2(Yim(:,:,i).^2);
            Yim(:,:,i) = sqrt(Yim(:,:,i).^2/av(i,1));
        end
    end
end

function [Yim] = unnormaliseData(Yim, av)
    if iscell(Yim)
        % mean squared power = 1
        nb = length(Yim);    
        for i=1:nb
            Yim{i,1} = sqrt(Yim{i}.^2*av(i,1));
        end
    else
        nb = size(Yim,3);
        for i=1:nb
            Yim(:,:,i) = sqrt(Yim(:,:,i).^2*av(i,1));
        end
    end
end

function X = conv2mat(X,nl,nc,L)
    if ndims(X) == 3
        [nl,nc,L] = size(X);
        X = reshape(X,nl*nc,L)';
    elseif ndims(squeeze(X)) == 2
        L = 1;
        [nl,nc] = size(X);
        X = reshape(X,nl*nc,L)';
    end
end

%%% Performance Measures

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Description: 
%           Spectral Angle Mapper (SAM).
% 
% Interface:
%           [SAM_index,SAM_map] = SAM(I1,I2)
%
% Inputs:
%           I1:         First multispectral image;
%           I2:         Second multispectral image.
% 
% Outputs:
%           SAM_index:  SAM index;
%           SAM_map:    Image of SAM values.
% 
% References:
%           [Yuhas92]   R. H. Yuhas, A. F. H. Goetz, and J. W. Boardman, "Discrimination among semi-arid landscape endmembers using the Spectral Angle Mapper (SAM) algorithm," 
%                       in Proceeding Summaries 3rd Annual JPL Airborne Geoscience Workshop, 1992, pp. 147�149.
%           [Vivone14]  G. Vivone, L. Alparone, J. Chanussot, M. Dalla Mura, A. Garzelli, G. Licciardi, R. Restaino, and L. Wald, �A Critical Comparison Among Pansharpening Algorithms�, 
%                       IEEE Transaction on Geoscience and Remote Sensing, 2014. (Accepted)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [SAM_index,SAM_map] = SAM(I1,I2)

    [M,N,~] = size(I2);
    prod_scal = dot(I1,I2,3); 
    norm_orig = dot(I1,I1,3);
    norm_fusa = dot(I2,I2,3);
    prod_norm = sqrt(norm_orig.*norm_fusa);
    prod_map = prod_norm;
    prod_map(prod_map==0)=eps;
    SAM_map = acos(prod_scal./prod_map);
    prod_scal = reshape(prod_scal,M*N,1);
    prod_norm = reshape(prod_norm, M*N,1);
    z=find(prod_norm==0);
    prod_scal(z)=[];prod_norm(z)=[];
    angolo = sum(sum(acos(prod_scal./prod_norm)))/(size(prod_norm,1));
    SAM_index = real(angolo)*180/pi;
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Description: 
%           Erreur Relative Globale Adimensionnelle de Synth�se (ERGAS).
% 
% Interface:
%           ERGAS_index = ERGAS(I1,I2,ratio)
%
% Inputs:
%           I1:             First multispectral image;
%           I2:             Second multispectral image;
%           ratio:          Scale ratio between MS and PAN. Pre-condition: Integer value.
% 
% Outputs:
%           ERGAS_index:    ERGAS index.
% References:
%           [Ranchin00]     T. Ranchin and L. Wald, �Fusion of high spatial and spectral resolution images: the ARSIS concept and its implementation,�
%                           Photogrammetric Engineering and Remote Sensing, vol. 66, no. 1, pp. 49�61, January 2000.
%           [Vivone14]      G. Vivone, L. Alparone, J. Chanussot, M. Dalla Mura, A. Garzelli, G. Licciardi, R. Restaino, and L. Wald, �A Critical Comparison Among Pansharpening Algorithms�, 
%                           IEEE Transaction on Geoscience and Remote Sensing, 2014. (Accepted)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function ERGAS_index = ERGAS(I1,I2,ratio)

    I1 = double(I1);
    I2 = double(I2);

    Err=I1-I2;
    ERGAS_index=0;
    for iLR=1:size(Err,3),
        ERGAS_index = ERGAS_index+mean2(Err(:,:,iLR).^2)/(mean2((I1(:,:,iLR))))^2;   
    end

    ERGAS_index = (100/ratio) * sqrt((1/size(Err,3)) * ERGAS_index);

end

