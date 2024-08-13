
#!/bin/bash

# Script for setting up PostgreSQL replication

# Configuration
PRIMARY_HOST="your_primary_host"
REPLICA_HOST="your_replica_host"
REPLICATION_USER="replication_user"
REPLICATION_PASSWORD="replication_password"
REPLICA_DATA_DIR="/var/lib/postgresql/12/main"

# Configure primary server
ssh $PRIMARY_HOST "
echo \"Configuring primary server...\"
sed -i \"s/#wal_level.*/wal_level = replica/\" /etc/postgresql/12/main/postgresql.conf
sed -i \"s/#max_wal_senders.*/max_wal_senders = 5/\" /etc/postgresql/12/main/postgresql.conf
sed -i \"s/#wal_keep_segments.*/wal_keep_segments = 32/\" /etc/postgresql/12/main/postgresql.conf
sed -i \"s/#hot_standby.*/hot_standby = on/\" /etc/postgresql/12/main/postgresql.conf
echo \"host replication $REPLICATION_USER $REPLICA_HOST/32 md5\" >> /etc/postgresql/12/main/pg_hba.conf
systemctl restart postgresql
"

# Create base backup and configure replica
echo "Configuring replica server..."
pg_basebackup -h $PRIMARY_HOST -U $REPLICATION_USER -D $REPLICA_DATA_DIR -Fp -Xs -P -R
echo "standby_mode = 'on'" >> $REPLICA_DATA_DIR/recovery.conf
echo "primary_conninfo = 'host=$PRIMARY_HOST port=5432 user=$REPLICATION_USER password=$REPLICATION_PASSWORD'" >> $REPLICA_DATA_DIR/recovery.conf
echo "trigger_file = '/tmp/postgresql.trigger'" >> $REPLICA_DATA_DIR/recovery.conf
systemctl start postgresql
echo "Replication setup completed."
