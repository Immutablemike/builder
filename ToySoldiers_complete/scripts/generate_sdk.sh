#!/bin/bash

set -e

echo "Generating TypeScript and Python SDKs from OpenAPI specification..."

OPENAPI_FILE="./docs/ToySoldiers_API_OpenAPI.yaml"

if [ ! -f "$OPENAPI_FILE" ]; then
  echo "OpenAPI specification not found at $OPENAPI_FILE"
  exit 1
fi

echo "Installing openapi-generator-cli..."
npm install -g @openapitools/openapi-generator-cli

echo "Generating TypeScript client..."
openapi-generator-cli generate \
  -i $OPENAPI_FILE \
  -g typescript-axios \
  -o ./clients/typescript \
  --additional-properties=npmName=@toysoldiers/api-client,npmVersion=1.0.0

echo "Generating Python client..."
openapi-generator-cli generate \
  -i $OPENAPI_FILE \
  -g python \
  -o ./clients/python/toysoldiers_client \
  --additional-properties=packageName=toysoldiers_client,packageVersion=1.0.0

echo "Installing TypeScript client dependencies..."
cd ./clients/typescript
npm install
npm run build

echo "Installing Python client dependencies..."
cd ../python/toysoldiers_client
pip install -e .

echo "SDK generation completed successfully!"
echo "TypeScript client: ./clients/typescript"
echo "Python client: ./clients/python/toysoldiers_client"
