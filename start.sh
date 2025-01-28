#!/bin/bash

# Run multiple Python scripts in parallel using a loop
for i in {1..25}; do
    python split/scape3.py "$i" &
done

# Wait for all background processes to complete
wait
