from dagster import pipeline, solid

@solid
def hello_world(context):
    print("Hello world!")
    return "Hello, world!"

@pipeline
def hello_world_pipeline():
    hello_world()