
library(data.table)
library(gplots)
library(stringr)

order <- str_trim(toupper(gene_list_ordering[,1]))

gene_list_values <- gene_list_values[,2:78]
gene_list_values[,1] = str_trim(gene_list_values[,1])
gene_list_values <- as.data.table(gene_list_values)
colnames(gene_list_values)[1] <- "Gene"
gene_list_values <- gene_list_values[,.SD[which.max(V78)],by=Gene]

# write.table(gene_list_values,file=paste("condensed",sep="_"),sep="\t",row.names=FALSE)
# gene_list_values_condensed <- read.table(paste("condensed",sep="_"),sep="\t",row.names=1,skip=1)
gene_list_values_condensed <- gene_list_values

# for_heatmap <- as.matrix(gene_list_values_condensed[,1:75])
# rownames(for_heatmap) <- str_trim(rownames(for_heatmap))

# GENERATING HEATMAP
# heat_map_filename <- paste("heatmap.", heat_map_type)
# TODO(opadron): change heat_map_filename to absolute path
# if(heat_map_type == "pdf") {
#     pdf(paste(heat_map_filename,heat_map_type,sep="."),width=50,height=50)
# } else if(heat_map_type == "png") {
#     png(paste(heat_map_filename,heat_map_type,sep="."),width=50,height=50)
# }
# 
# for_heatmap <- for_heatmap[order,]
# setdiff(rownames(for_heatmap),order)
# for_heatmap[for_heatmap==-99] = NA
# heatmap.2(for_heatmap,trace="none",Colv=FALSE,Rowv=FALSE,scale="row",,col=colorRampPalette(c("red","red1","yellow","white"))(100),colsep=c(10,23,40,58,75),margins=c(10,10),na.color="grey",rowsep=c(51,62),sepwidth=c(1))
# dev.off()

