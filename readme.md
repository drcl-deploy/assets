# assets

contains simulation assets in various file formats for different entities like robots, objects, etc.

## guide

1. every new entity should be at one level depth:: `assets/source/<entity name>/` 
2. add folder for each variant: `assets/source/<entity name>/<variant name>`
3. share meshes across variants, avoid duplication
4. add `.cfg` and `.py` for each variant and register in in a `__init__.py` for easy access. 
 
## usage

    git clone https://github.com/drcl-deploy/assets.git
    cd ./assets/
    pip install -e . # so local changes can take effect 

then add a global variable `SIM_ASSETS_PATH`

    cd ./assets/source/
    pwd # copy the output of this command
    sudo nano ~/.bashrc
    export SIM_ASSETS_PATH=<copied path> # add this to the end, save file, and restart terminal 

to load as file: `SIM_ASSETS_PATH/<entity name>/.../<file_name>`

to load in python code  `from assets.<entity_name>.<variant_name> import CFG, CONSTANT...`