function [SRE_vec,mSRE]=sre(X,Xhat)
if length(size(X))==3
    X=reshape(X,[size(X,1)*size(X,2) size(X,3)]);
    Xhat=reshape(Xhat,[size(Xhat,1)*size(Xhat,2) size(Xhat,3)]);
    for i=1:size(X,2)
        SRE_vec(i) = 10*log10(sum(X(:,i).^2)/ sum((Xhat(:,i)-X(:,i)).^2));
    end
    mSRE=mean(SRE_vec);
else
    X=X(:);
    Xhat=Xhat(:);
    SRE_vec=10*log10(sum(X.^2)/ sum((Xhat-X).^2));
    mSRE=SRE_vec;
end