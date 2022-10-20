function [] = drawpcolor_pair(cowname1, count1, cowname2, count2)
a = importdata(['C:\Users\wuc\Desktop\±¸·Ý´ýÉ¾\Data\hist_similarity',cowname1,'&',cowname2,'.txt']);
stat(a)

[X, Y] = meshgrid(1:1:count1, 1:1:count2);
Z = ones(size(X,1),size(X,2));
for i=1:count1*count2
    Z(a(i,2)+1,a(i,1)+1)=a(i,3);
end
fontsize = 18;
s = pcolor(X,Y,Z);
set(s, 'edgecolor', 'none');
colormap hot; colorbar;
caxis([0,1])
set(gca,'FontSize',fontsize,'FontName','Times New Roman','FontWeight','bold');
set(gcf,'Position',[100,100,1000,800]);
xlabel(['cow ',cowname1]);
ylabel(['cow ',cowname2]);
end


