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

# Import products
import_collection "ecommerce" "products" "products.json"

# Import prescriptions
import_collection "hospital" "prescriptions" "prescriptions.json"