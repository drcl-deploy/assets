# assets

contains simulation assets in various file formats for different entities like robots, objects, etc.

## guide

1. every new entity should be at one level depth:: `assets/source/<entity name>/` 
2. add folder for each variant: `assets/source/<entity name>/<variant name>`
3. share meshes across variants, avoid duplication
4. add configs in `.py` for each variant and register in `__init__.py` for easy access. 
5. add any entity-specific constants that can be resused in a seperate `constants.py` and register in `__init__.py`
6. resuse `isaaclab_assets` by simply importing it in `__init__.py` and augment with `constants` you want (refer [g1](source/g1) for example). Do not make redundant copies inside this repo. 
7. while making `.xml`s to work with [mj_sim](https://github.com/drcl-deploy/mj_sim), ensure the following are followed
    1. `<option timestep='0.001'>`
    2. armature and damping are added for joints `<default>` 
    3. actuators are off type `<general>` with 
        * `biastype="affine" gainprm="0.0 0 0 0 0 0 0 0 0 0" biasprm="0 0.0 0.0 0 0 0 0 0 0 0"` 
        * no `ctrlrange`
        * has `frcrange` (or has `actuatorfrcrange` in the corresponding joint)
    4. has the following sensors for the `root`  link
        * `<framepos name="root_pos"  ..../>`
        * `<framequat name="root_quat"  ..../>`
        * `<framelinvel name="root_linvel"  ..../>`
        * `<frameangvel name="root_angvel"  ..../>`
    5.  has the following sensors for the `imu`  link
        * `<framequat name="torso_imu_quat" ... />`
        * `<accelerometer name="torso_imu_acc" ... />`
        * `<gyro name="torso_imu_gyro" ... />`
    6. has the equality constraint `<weld name="world_root" active="true" ... />` , set to **true** by default.

## usage

    git clone https://github.com/drcl-deploy/assets.git
    cd ./assets/
    git lfs pull # to download mesh files
    pip install -e . # so local changes can take effect 

then add a global variable `SIM_ASSETS_PATH`

    cd ./assets/source/
    pwd # copy the output of this command
    sudo nano ~/.bashrc
    export SIM_ASSETS_PATH=<copied path> # add this to the end, save file, and restart terminal 

to load as file: `SIM_ASSETS_PATH/<entity name>/.../<file_name>`

to load in python code  `from assets.<entity_name>.<variant_name> import CFG, CONSTANT...`

## test

### Isaaclab

for loading and simulationg a model with zero ctrl, run

    python3 tests/load_robot_isaaclab.py --robot <robot moudle> --cfg <config name>

for example,

    python3 tests/load_robot_isaaclab.py --robot assets.hector_v2.feet --cfg WITHOUT_COUPLING_CFG


### MuJoCo

run,
    
    python -m mujoco.viewer

then drag and drop the `.xml` model to be tested