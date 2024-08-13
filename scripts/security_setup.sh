
#!/bin/bash

# Script for setting up Role-Based Access Control (RBAC) and OAuth2 Integration

# Configuration
DB_HOST="your_db_host"
DB_USER="your_db_user"
DB_NAME="your_db_name"
DB_PASSWORD="your_db_password"
RBAC_TABLES=("roles" "permissions" "user_roles" "role_permissions")

# Export the password so it's available to psql or other commands
export PGPASSWORD=$DB_PASSWORD

echo "Setting up Role-Based Access Control (RBAC)..."

# Create tables for RBAC
for table in "${RBAC_TABLES[@]}"; do
  psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
  CREATE TABLE IF NOT EXISTS $table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT
  );
  "
done

# Populate roles and permissions
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
INSERT INTO roles (name, description) VALUES
('admin', 'Administrator with full access'),
('editor', 'Editor with limited access'),
('viewer', 'Viewer with read-only access')
ON CONFLICT (name) DO NOTHING;
"

psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
INSERT INTO permissions (name, description) VALUES
('read', 'Permission to read data'),
('write', 'Permission to write data'),
('delete', 'Permission to delete data')
ON CONFLICT (name) DO NOTHING;
"

# OAuth2 Integration
echo "Setting up OAuth2 Integration..."
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
CREATE TABLE IF NOT EXISTS oauth_providers (
    id SERIAL PRIMARY KEY,
    provider_name VARCHAR(255) NOT NULL,
    client_id VARCHAR(255) NOT NULL,
    client_secret VARCHAR(255) NOT NULL,
    redirect_uri VARCHAR(255) NOT NULL,
    scopes VARCHAR(255),
    UNIQUE (provider_name, client_id)
);
"

# Insert sample OAuth2 providers
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "
INSERT INTO oauth_providers (provider_name, client_id, client_secret, redirect_uri, scopes) VALUES
('google', 'your_google_client_id', 'your_google_client_secret', 'your_redirect_uri', 'profile email'),
('github', 'your_github_client_id', 'your_github_client_secret', 'your_redirect_uri', 'user repo')
ON CONFLICT (provider_name, client_id) DO NOTHING;
"

echo "RBAC and OAuth2 setup completed."

# Unset the password for security
unset PGPASSWORD
