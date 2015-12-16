
# inputs
#   input -> type: table, format: r.dataframe
#   num_clusters -> type: number, format: number
#
# outputs
#   centers -> type: r, format: serialized
#   clusters -> type: r, format: serialized

cl <- kmeans(input, num_clusters)
centers <- cl$centers
clusters <- cl$cluster

