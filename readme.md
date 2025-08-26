# assets

contains simulation assets in various file formats for different entities like robots, objects, etc.

## guide

1. every new entity should be at one level depth:: `assets/entity/` 
2. add folder for each variant: `assets/entity/variant`
3. share meshes across variants, avoid duplication
 
## usage

    git clone https://github.com/drcl-deploy/assets.git

then add a global variable `SIM_ASSETS_PATH`
    
for temporary usage:

    cd ./assets/
    export SIM_ASSETS_PATH="$(pwd)"

for permanent usage:

    cd ./assets/
    pwd # copy the out put of this command
    sudo nano ~/.bashrc
    export SIM_ASSETS_PATH=<copied path> # add this to the end, save file, and restart terminal 

in code load entity as `SIM_ASSETS_PATH/entity/.../<file_name>`    