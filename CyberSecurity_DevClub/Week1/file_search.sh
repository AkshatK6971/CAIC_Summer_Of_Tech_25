#!/bin/bash

DIR="$1"
echo "Scanning directory: $DIR"

find "$DIR" -type f -name "*.log" -mtime -7 | while read file; do
    count=$(wc -l < "$file")
    echo "$file: $count lines"
    total=$((total + count))
done

echo "Total lines in .log files modified in last 7 days: $total"
