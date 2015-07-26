import yaml

with open('races.yaml', 'r') as f:
    race_descriptions = yaml.load(f)

with open('classes.yaml', 'r') as f:
    class_descriptions = yaml.load(f)

with open('backgrounds.yaml', 'r') as f:
    background_descriptions = yaml.load(f)
