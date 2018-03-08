case "$1" in
  start)
    docker run \
        --name some_neo4j \
        --publish=7474:7474 \
        --publish=7687:7687 \
        --volume=$HOME/neo4j/data:/data \
        --volume=$HOME/neo4j/logs:/logs \
        --env=NEO4J_dbms_security_auth__enabled=false \
        neo4j:3.3
    ;;
  delete)
    docker kill some_neo4j
    docker rm some_neo4j
    ;;

  *)
    echo "Usage: \"docker.sh {start|delete}\""

esac
