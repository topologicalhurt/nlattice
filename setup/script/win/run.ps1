$conf = Get-Content ".\config.json" -raw | ConvertFrom-Json

if ( $null -eq $conf.Meta.ContainerId )
{
    throw "No container ID found. Please either replace ContainerId with the target docker container id in config.json
or run: python nlattice_docker_install_V0.0.1.py --wipe-container=True"
}

docker start $conf.Meta.ContainerId | out-null
docker exec -it $conf.Meta.ContainerId /bin/bash