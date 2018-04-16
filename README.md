# genie-backend
genie backend service


Neo4j config:
- [Environment Variables](https://neo4j.com/docs/operations-manual/current/installation/docker/#docker-environment-variables)
- [Auth Disable](https://neo4j.com/docs/operations-manual/current/reference/configuration-settings/#config_dbms.security.auth_enabled)
- Can set default auth with env `NEO4J_AUTH=neo4j/<password>`


Routes:
- Auth
  - Login
  - Check Token
  - Signup
- Records
- Tags
