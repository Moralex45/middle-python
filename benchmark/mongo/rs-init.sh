#!/bin/bash

# Init configsvr
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'

# Init shard1
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'

docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'

# Init shard2
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh' 

docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'

# Create DB
docker exec -it mongors1n1 bash -c 'echo "use UGC_data" | mongosh'

# enable sharding
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"UGC_data\")" | mongosh'

# creating collections
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"UGC_data.likes\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"UGC_data.reviews\")" | mongosh'
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"UGC_data.bookmarks\")" | mongosh'

# sharding collections
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"UGC_data.likes\", {\"user_id\": \"hashed\"})" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"UGC_data.reviews\", {\"movie_id\": \"hashed\"})" | mongosh'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"UGC_data.bookmarks\", {\"user_id\": \"hashed\"})" | mongosh'

# indexing collections
docker exec -it mongos1 bash -c 'echo "db.likes.createIndex( { \"user_id\": 1 } )" | mongosh'
docker exec -it mongos1 bash -c 'echo "db.reviews.createIndex( { \"movie_id\": 1 } )" | mongosh'
docker exec -it mongos1 bash -c 'echo "db.bookmarks.createIndex( { \"user_id\": 1 } )" | mongosh'