library(scater)
library(Seurat)


library(SeuratDisk)
library(SeuratData)
library(patchwork)

correct_integration_loom = Connect(filename = "~/passala/Generated_Tables/Temp_junk/slimmed_concatenated_rice_maize_genes_aligned_by_random_genes.loom", mode = "r")

correct_integration_seurat = as.Seurat(correct_integration_loom)

correct_integration_seurat.list <- SplitObject(correct_integration_seurat, split.by = "Species")

correct_integration_seurat.list <- lapply(X = correct_integration_seurat.list, FUN = function(x) {
  x <- NormalizeData(x)
  x <- FindVariableFeatures(x, selection.method = "vst", nfeatures = 1000)
})

features <- SelectIntegrationFeatures(object.list = correct_integration_seurat.list)




correct_integration_seurat.anchors <- FindIntegrationAnchors(object.list = correct_integration_seurat.list, anchor.features = features)


correct_integration_seurat.combined <- IntegrateData(anchorset = correct_integration_seurat.anchors)

DefaultAssay(correct_integration_seurat.combined) <- "integrated"

correct_integration_seurat.combined <- ScaleData(correct_integration_seurat.combined, verbose = FALSE)
correct_integration_seurat.combined <- RunPCA(correct_integration_seurat.combined, npcs = 30, verbose = FALSE)
correct_integration_seurat.combined <- RunUMAP(correct_integration_seurat.combined, reduction = "pca", dims = 1:20)
correct_integration_seurat.combined <- FindNeighbors(correct_integration_seurat.combined, reduction = "pca", dims = 1:30)
correct_integration_seurat.combined <- FindClusters(correct_integration_seurat.combined, resolution = 0.5)

p1 <- DimPlot(correct_integration_seurat.combined, reduction = "umap", group.by = "Species")
p2 <- DimPlot(correct_integration_seurat.combined, reduction = "umap", group.by = "Cell.Cluster.Annotation")
p1 + p2
correct_integration_seurat.combined.loom <- as.loom(correct_integration_seurat.combined, filename = "~/passala/Generated_Tables/Temp_junk/integrated_by_default_seurat_random_genes.loom", verbose = FALSE)
correct_integration_seurat.combined.loom
correct_integration_seurat.combined.loom$close_all()
