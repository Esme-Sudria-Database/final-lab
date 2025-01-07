#!/bin/bash

import_collection() {
    local db=$1
    local collection=$2
    local file=$3

    mongoimport \
        --host localhost \
        --db "$db" \
        --collection "$collection" \
        --type json \
        --jsonArray \
        --file "/esme_data/$file"
}

# Import sensors
import_collection "sensors" "sensors" "sensors.json"
