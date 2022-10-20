function [] = drawpcolor(cowname, count)
a = importdata(['C:\Users\wuc\Desktop\±¸·Ý´ýÉ¾\Data\hist_similarity',cowname,'.txt']);
stat(a)

[X, Y] = meshgrid(1:1:count, 1:1:count);
Z = ones(size(X));
for i=1:count*(count-1)/2
    Z(a(i,1)+1,a(i,2)+1)=a(i,3);
end
fontsize = 18;
s = pcolor(X,Y,Z);
set(s, 'edgecolor', 'none');
colormap hot; colorbar;
caxis([0,1])
set(gca,'FontSize',fontsize,'FontName','Times New Roman','FontWeight','bold');
set(gcf,'Position',[100,100,1000,800]);
end


