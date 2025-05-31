#!/bin/bash

length="$1"
count="$2"
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
outfile="passwords_$timestamp.txt"

generate_password() {
    tr -dc 'A-Za-z0-9!@#$%^&*()_+=' < /dev/urandom | head -c "$length"
}

for i in $(seq 1 "$count"); do
    generate_password >> "$outfile"
    echo "" >> "$outfile"
done

echo "Generated $count passwords of length $length in file $outfile"