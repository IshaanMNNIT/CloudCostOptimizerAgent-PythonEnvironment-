from simulator.cloud_env import CloudEnvironment
from state_encoder import StateEncoder

env = CloudEnvironment()
encoder = StateEncoder()

state = env.step()
encoded = encoder.encode(state)

print("Shape:", encoded.shape)
print(encoded)