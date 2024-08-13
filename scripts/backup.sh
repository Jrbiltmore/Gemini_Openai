
#!/bin/bash

# Backup directory paths
SOURCE_DIR="/mnt/data/AI_System_Structure"
BACKUP_DIR="/mnt/backup"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

# Create a backup of the entire system structure
echo "Starting backup process..."
tar -czf $BACKUP_FILE $SOURCE_DIR

# Verify if the backup was successful
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_FILE"
else
    echo "Backup failed!"
    exit 1
fi

# Clean up old backups (retain only the last 7 backups)
echo "Cleaning up old backups..."
find $BACKUP_DIR -type f -name "*.tar.gz" -mtime +7 -exec rm {} \;

echo "Backup process completed."
