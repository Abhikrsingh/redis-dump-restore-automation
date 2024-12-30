# Redis Dump and Restore Script

## Overview
This script provides functionality for both dumping and restoring data from Redis databases in a single script. It supports multiple Redis instances and databases through configurable JSON files.

---

# Dump Script

## Description
The dump functionality connects to specified Redis instances and databases, retrieves keys matching a pattern, and saves the key-value data along with their TTLs into JSON files. The dumps are organized into date-wise directories.

## Configuration
Configuration for the dump functionality is stored in a JSON file (`details.json`). Below is an example configuration:

```json
{
    "instances": [
        {
            "host": "host-1",
            "port": 6379,
            "password": "password",
            "databases": [3],
            "file_prefix": "redis_pattern1_",
            "dump_path": "redisdump/instance-1",
            "pattern": "pattern-1*",
            "limit": null
        }
    ]
}
```

### Key Points
- **`host`**: Redis host.
- **`port`**: Redis port.
- **`password`**: Redis password.
- **`databases`**: List of databases to dump.
- **`file_prefix`**: Prefix for the dump files.
- **`dump_path`**: Path to save the dump files.
- **`pattern`**: Key pattern to match (use `null` for all keys).
- **`limit`**: Maximum number of keys to dump (use `null` for no limit).

## Usage
Run the script with:
```bash
python3 redisDump.py
```
---

### Example Output Structure
```
redisdump/
└── instance-1/
    ├── 2024-12-30/
    │   ├── redis_pattern1_3.json
    │   └── redis_pattern2_2.json
└── allKeys/
    ├── 2024-12-30/
        └── redis_all_keys_0.json
```

# Restore Script

## Description
The restore functionality reads JSON dump files and restores the keys and their TTLs into the specified Redis databases.

## Configuration
Configuration for the restore functionality is stored in a JSON file (`restore.json`). Below is an example configuration:

```json
{
    "instances": [
        {
            "host": "host-new-1",
            "port": 6379,
            "password": "password",
            "databases": [3],
            "file_prefix": "redis_pattern1_",
            "dump_path": "redisdump/instance-1",
            "pattern": "pattern-1*",
            "limit": null
        }
    ]
}
```

### Key Points
- **`host`**: Redis host.
- **`port`**: Redis port.
- **`password`**: Redis password.
- **`databases`**: List of databases to restore.
- **`file_prefix`**: Prefix of the dump files.
- **`dump_path`**: Path where the dump files are located.

## Usage
Run the script with:
```bash
python3 redisRestore.py
```

---

## Important Notes
1. Ensure that the JSON configuration files (`details.json` and `restore.json`) are properly set up before running the script.
2. The dump files are saved in date-wise directories for better organization.
3. Use the `pattern` field to target specific keys for dumping.
4. The restore script will overwrite existing keys if they exist.
5. The script uses `redis-py` for interacting with Redis, so ensure it is installed:
   ```bash
   pip install redis
   ```
6. Ensure proper permissions for reading and writing to the specified dump directories.

---

## Example
### Dump Command Output
```bash
Dump for database 3 started at: 2024-12-30 10:00:00
Fetching keys matching pattern: pattern-1*
Total keys processed: 500
Dump saved to redisdump/instance-1/2024-12-30/redis_pattern1_3.json
```

### Restore Command Output
```bash
Restoration for database 3 on instance host-1 started at: 2024-12-30 11:00:00
Restoring keys from redisdump/instance-1/2024-12-30/redis_pattern1_3.json to database 3...
Restored key: user:123 with TTL: 3600
Total keys restored for database 3: 500
```

