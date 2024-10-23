import numpy as np
import matplotlib.pyplot as plt
import os

def see_clusters_histogram(cluster_folder):
    clusters = np.load(os.path.join(cluster_folder, "clusters.npy"))
    cluster_count = {}
    for cluster in clusters:
        if cluster not in cluster_count:
            cluster_count[cluster] = 0
        cluster_count[cluster] += 1

    sorted_clusters = sorted(cluster_count.items(), key=lambda x: x[0])

    labels = [str(k) for k, v in sorted_clusters]
    sizes = [v for k, v in sorted_clusters]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, sizes)
    plt.xlabel('Cluster ID')
    plt.ylabel('Number of Items')
    plt.title('Cluster Distribution')

    n = max(1, len(labels) // 10)
    plt.xticks(ticks=range(0, len(labels), n), labels=[labels[i] for i in range(0, len(labels), n)], rotation=45)

    plt.tight_layout()
    plt.show()

def see_clusters_piechart(cluster_folder, threshold_percentage=1.0):
    clusters = np.load(os.path.join(cluster_folder, "clusters.npy"))
    cluster_count = {}
    
    for cluster in clusters:
        if cluster not in cluster_count:
            cluster_count[cluster] = 0
        cluster_count[cluster] += 1

    total_items = sum(cluster_count.values())
    threshold = (threshold_percentage / 100) * total_items 

    above_threshold = {}
    smaller_clusters_sum = 0
    
    for cluster, count in cluster_count.items():
        if count >= threshold:
            above_threshold[cluster] = count
        else:
            smaller_clusters_sum += count

    if smaller_clusters_sum > 0:
        above_threshold["Other"] = smaller_clusters_sum

    labels = [str(k) for k in above_threshold.keys()]
    sizes = [v for v in above_threshold.values()]

    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(sizes, autopct='%1.1f%%', startangle=90, pctdistance=0.85, 
                                       textprops={'fontsize': 10}, wedgeprops={'edgecolor': 'white'})

    plt.legend(wedges, labels, title="Clusters", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

    plt.title(f'Clusters bigger than {threshold_percentage}% of the total data')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    see_clusters_histogram(r'saved_cluster\cluster_D5')
    see_clusters_piechart(r'saved_cluster\cluster_D5',1.0)


