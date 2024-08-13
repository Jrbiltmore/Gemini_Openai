
#!/bin/bash

# Blue-Green Deployment Script

# Step 1: Deploy to Green environment
echo "Deploying to Green environment..."
kubectl apply -f deployment-green.yaml
kubectl rollout status deployment/my-app-green

# Step 2: Validate Green deployment
echo "Validating Green environment..."
if curl -f http://green.my-app.example.com/health; then
    echo "Green environment is healthy. Proceeding with traffic switch."
else
    echo "Green environment validation failed. Rolling back deployment."
    exit 1
fi

# Step 3: Switch traffic to Green environment
echo "Switching traffic to Green environment..."
kubectl patch service my-app -p '{"spec":{"selector":{"app":"my-app-green"}}}'

# Step 4: Monitor the new version
echo "Monitoring new version..."
if curl -f http://my-app.example.com/health; then
    echo "New version is healthy."
else
    echo "New version validation failed. Rolling back traffic to Blue environment."
    kubectl patch service my-app -p '{"spec":{"selector":{"app":"my-app-blue"}}}'
    exit 1
fi

# Step 5: Tear down Blue environment
echo "Tearing down Blue environment..."
kubectl delete -f deployment-blue.yaml

echo "Blue-Green Deployment completed successfully."
