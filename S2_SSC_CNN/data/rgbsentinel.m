Y2=imread('B02.jp2');
Y3=imread('B03.jp2');
Y4=imread('B04.jp2');

Y(:,:,1)=Y2;
Y(:,:,2)=Y3;
Y(:,:,3)=Y4;

Y=Y(8000:10000,4600:7000,:);

Y=double(Y);
%% 

RGB=sentinel2RGB(Y,1);
imshow(RGB)