
#!/bin/bash

# Set up PostgreSQL Database and Migrate Schema

DB_HOST="your_db_host"
DB_USER="your_db_user"
DB_NAME="your_db_name"
DB_PASSWORD="your_db_password"

# Export the password so it's available to psql or other commands
export PGPASSWORD=$DB_PASSWORD

echo "Starting database setup..."

# Create the database
psql -h $DB_HOST -U $DB_USER -c "CREATE DATABASE $DB_NAME;"

# Apply schema migrations
echo "Applying schema migrations..."
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f /mnt/data/AI_System_Structure/database/schema.sql

echo "Database setup and migration completed."

# Unset the password for security
unset PGPASSWORD
