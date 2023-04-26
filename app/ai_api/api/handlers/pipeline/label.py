import csv


class LabelHandler:
    labels = {}
    with open(
        "/app/ai_api/api/handlers/pipeline/assets/yamnet_class_map.csv",
        newline="",
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            labels[int(row["index"])] = row["display_name"]

    labels_tree = []
    with open(
        "/app/ai_api/api/handlers/pipeline/assets/classes_tree.csv", newline=""
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for i in range(6):
                labels_tree.append([i for i in row.values()])
    using_labels = [item for sublist in labels_tree for item in sublist]
    using_labels = ["Animal", "Music", "Speech", "Dog"]
    using_labels = list(sorted(set(using_labels)))

    @classmethod
    def get_using_label(cls, label: str):
        labels = []
        for labels_group in cls.labels_tree:
            for i in range(6):
                if label in labels_group:
                    for j in range(i, -1, -1):
                        if labels_group[j] in cls.using_labels:
                            return labels_group[j]
        return labels
