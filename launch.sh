docker compose -f ./docker/docker-compose.yml \
                --env-file ./docker/envs/db.env \
                --env-file ./docker/envs/backend.env \
                --env-file ./docker/envs/frontend.env \
                up \
                # --build --force-recreate