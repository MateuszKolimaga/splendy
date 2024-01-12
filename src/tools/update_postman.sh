./manage.py spectacular --color --file schema.yml
openapi2postmanv2 -s schema.yml -o collection.json -p -O folderStrategy=Tags,includeAuthInfoInExample=false
cat collection.json | jq '{collection: .}' > collection_temp.json
curl --location -g --request PUT "https://api.getpostman.com/collections/$SPENDID_COLLECTION_ID" \
--header 'Content-Type: application/json' \
--header "X-API-Key: $POSTMAN_API_KEY_SECRET" \
--data-binary "@collection_temp.json"
rm schema.yml
rm collection.json
rm collection_temp.json
