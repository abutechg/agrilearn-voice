from datasets import load_dataset

print("Downloading Yoruba AfriSwitch test data...")

dataset = load_dataset(
    "intronhealth/AfriSwitch",
    "yoruba",
    split="test"
)

print(dataset)
print(dataset.features)

dataset.save_to_disk("afriswitch_yoruba_test")

print("Dataset saved to benchmark/afriswitch_yoruba_test")
