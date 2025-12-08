---

# ✅ **FINAL `Reflection.md`**

```md
### Reflection

Implementing user login, registration, and protected calculation routes helped me understand how backend components work together to form a secure API. The existing SQLAlchemy models served as the structure for the users and calculations tables, and it became clear how the Pydantic schemas translate user input from the frontend into validated Python objects that can be stored in the database. Integrating JWT authentication required me to ensure that only authenticated users could access calculation routes and that each calculation was correctly tied to the user performing it.

Testing was a major step in validating reliability. Integration tests using Pytest verified that both authentication and calculation functionality worked correctly without the frontend. Running these automatically inside Docker in the CI pipeline helped guarantee that the backend did not rely on anything specific to my local machine. Playwright testing added another layer by simulating user flows—register, log in, perform calculations—which proved that the system worked end-to-end.

Security was an important part of this module. Storing passwords through hashing (bcrypt), verifying ownership of calculations, and protecting API routes with JWT ensured that user data is kept private. Overall, this project helped me connect database logic, authentication, API design, and automated testing into a single working system deployed through CI/CD.