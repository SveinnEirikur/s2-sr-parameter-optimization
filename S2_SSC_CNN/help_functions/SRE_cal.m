function[SRE_vec,aSRE]=SRE_cal(A,B)
[n,m,ch]=size(B);
A=double(A); % Ground-truth(GT)
B=double(B); %

A=reshape(A,m*n,ch);
B=reshape(B,m*n,ch);
SRE_vec=zeros(ch,1);
for i=1:ch
    SRE_vec(i)=10*log10(sum(A(:,i).^2)/sum((A(:,i)-B(:,i)).^2));
end
aSRE=mean(SRE_vec);
end
