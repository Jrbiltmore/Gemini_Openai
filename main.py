
import ldclient
from ldclient.config import Config

# Initialize the LaunchDarkly client with your SDK key
ldclient.set_config(Config("your-sdk-key"))

# Create a user context for feature flag evaluation
user = {
    "key": "user-12345",
    "name": "John Doe",
    "email": "john@example.com"
}

# Check if a feature is enabled using a feature flag
if ldclient.get().variation("new_dashboard", user, False):
    print("New dashboard is enabled.")
    # Code for the new dashboard feature
else:
    print("Using the old dashboard.")
    # Fallback to the old dashboard
