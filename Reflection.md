# Reflection - Module 12

This module helped me understand how full back-end development comes together: routing, validation, database access, hashing, testing, and CI/CD. Implementing user registration and login showed me how to handle security concerns such as password hashing and input validation. The calculations CRUD endpoints helped reinforce BREAD operations and the role of Pydantic schemas in validating requests and shaping responses.

Setting up Docker and PostgreSQL taught me how to maintain a consistent environment across local development and deployment. The most challenging part was making tests run both locally and in GitHub Actions, and troubleshooting database connectivity. After fixing DATABASE_URL defaults and adjusting pytest configuration, tests became reliable and repeatable.

The CI/CD workflow was the highlight of this module. I now understand how automation ensures code quality and continuously delivers working images to Docker Hub. Seeing the workflow execute tests and push a Docker image on every commit made the project feel production-ready. Overall, this module strengthened my confidence with backend architecture and DevOps practices.