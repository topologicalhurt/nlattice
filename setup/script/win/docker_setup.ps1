$conf = Get-Content ".\config.json" -raw | ConvertFrom-Json

if ( $null -eq $conf.Meta.ContainerId )
{
    $conf.Meta.ContainerId = docker run -it -d pymesh/pymesh
    $conf | ConvertTo-Json -depth 4 | set-content "config.json"
}

$CONTAINER_ID = $conf.Meta.ContainerId
docker cp install.tar "$($CONTAINER_ID):/root/"
docker exec -i $CONTAINER_ID /bin/bash -c `
"tar -xf install.tar; rm install.tar; cd install; ./install.sh $($args[0]) `"$($args[1])`""