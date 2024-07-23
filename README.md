# Setup-Django-Project

This repository is dedicated to discovering best practices for setting up a basic Django project. It serves as a valuable resource for programmers worldwide, offering insights and guidelines to streamline the process of initiating a Django project efficiently.

## Libraries Used

- Django
- djangorestframework
- django-cors-headers
- python-decouple
- psycopg2
- dj-database-url
- colorlog
- isort
- pyjwt[crypto]
- python-dateutil

## Getting Started

### Setup Token Credential

1. Generate a private key using the command:

   ```sh
   openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
   ```

2. Generate a public key using the command:

   ```sh
   openssl rsa -in private_key.pem -pubout -out public_key.pem
   ```

(Add instructions on how to set up and run the project)

## Best Practices

(List some key best practices for setting up a Django project)

## Contributing

(Add information on how others can contribute to this project)

## License

(Add license information if applicable)
