# Carlo

![credits to Stable Diffusion](media/logo-1.png)

Install requirements first:  

### Install carla
[Link](https://carla.readthedocs.io/en/latest/start_quickstart/)

#### We are using version 0.9.14 at the time of this project
- Download for Ubuntu via [Link](https://github.com/carla-simulator/carla/blob/master/Docs/download.md)
- Unzip in any location
- run ./CarlaUE4.sh -RenderOfScreen to run carla server without UI

add alias for carla:  
alias carla='/path/to/carla/CarlaUE4.sh'

Adjust sensitivity in Carla
<details>
<summary>Copy this into carla/CarlaUE4/Config/DefaultInput.ini</summary>

```
[/Script/Engine.InputSettings]
-AxisConfig=(AxisKeyName="Gamepad_LeftX",AxisProperties=(DeadZone=0.25,Exponent=1.f,Sensitivity=1.f))
-AxisConfig=(AxisKeyName="Gamepad_LeftY",AxisProperties=(DeadZone=0.25,Exponent=1.f,Sensitivity=1.f))
-AxisConfig=(AxisKeyName="Gamepad_RightX",AxisProperties=(DeadZone=0.25,Exponent=1.f,Sensitivity=1.f))
-AxisConfig=(AxisKeyName="Gamepad_RightY",AxisProperties=(DeadZone=0.25,Exponent=1.f,Sensitivity=1.f))
-AxisConfig=(AxisKeyName="MouseX",AxisProperties=(DeadZone=0.f,Exponent=1.f,Sensitivity=0.30f))
-AxisConfig=(AxisKeyName="MouseY",AxisProperties=(DeadZone=0.f,Exponent=1.f,Sensitivity=0.30f))
+AxisConfig=(AxisKeyName="Gamepad_LeftX",AxisProperties=(DeadZone=0.250000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="Gamepad_LeftY",AxisProperties=(DeadZone=0.250000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="Gamepad_RightX",AxisProperties=(DeadZone=0.250000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="Gamepad_RightY",AxisProperties=(DeadZone=0.250000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MouseX",AxisProperties=(DeadZone=0.000000,Sensitivity=0.300000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MouseY",AxisProperties=(DeadZone=0.000000,Sensitivity=0.300000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MouseWheelAxis",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="Gamepad_LeftTriggerAxis",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="Gamepad_RightTriggerAxis",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MotionController_Left_Thumbstick_X",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MotionController_Left_Thumbstick_Y",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MotionController_Left_TriggerAxis",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MotionController_Left_Grip1Axis",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MotionController_Left_Grip2Axis",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MotionController_Right_Thumbstick_X",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MotionController_Right_Thumbstick_Y",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MotionController_Right_TriggerAxis",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MotionController_Right_Grip1Axis",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="MotionController_Right_Grip2Axis",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="Gamepad_Special_Left_X",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
+AxisConfig=(AxisKeyName="Gamepad_Special_Left_Y",AxisProperties=(DeadZone=0.000000,Sensitivity=1.000000,Exponent=1.000000,bInvert=False))
bAltEnterTogglesFullscreen=True
bF11TogglesFullscreen=True
bUseMouseForTouch=True
bEnableMouseSmoothing=True
bEnableFOVScaling=True
FOVScale=0.011110
DoubleClickTime=0.200000
bCaptureMouseOnLaunch=False
DefaultViewportMouseCaptureMode=CaptureDuringMouseDown
bDefaultViewportMouseLock=False
DefaultViewportMouseLockMode=DoNotLock
+ActionMappings=(ActionName="RestartLevel",Key=R,bShift=False,bCtrl=False,bAlt=False,bCmd=False)
+ActionMappings=(ActionName="Handbrake",Key=SpaceBar,bShift=False,bCtrl=False,bAlt=False,bCmd=False)
+ActionMappings=(ActionName="ToggleManualMode",Key=M,bShift=False,bCtrl=False,bAlt=False,bCmd=False)
+ActionMappings=(ActionName="ToggleHUD",Key=G,bShift=False,bCtrl=False,bAlt=False,bCmd=False)
+ActionMappings=(ActionName="Jump",Key=Enter,bShift=False,bCtrl=False,bAlt=False,bCmd=False)
+ActionMappings=(ActionName="ToggleReverse",Key=Q,bShift=False,bCtrl=False,bAlt=False,bCmd=False)
+ActionMappings=(ActionName="UseTheForce",Key=F,bShift=False,bCtrl=False,bAlt=False,bCmd=False)
+ActionMappings=(ActionName="ToggleCamera",Key=Tab,bShift=False,bCtrl=False,bAlt=False,bCmd=False)
+ActionMappings=(ActionName="ChangeWeather",Key=C,bShift=False,bCtrl=False,bAlt=False,bCmd=False)
+ActionMappings=(ActionName="ToggleAutopilot",Key=P,bShift=False,bCtrl=False,bAlt=False,bCmd=False)
+AxisMappings=(AxisName="CameraZoom",Key=MouseWheelAxis,Scale=-20.000000)
+AxisMappings=(AxisName="CameraZoom",Key=PageUp,Scale=-10.000000)
+AxisMappings=(AxisName="CameraZoom",Key=PageDown,Scale=10.000000)
+AxisMappings=(AxisName="CameraUp",Key=Up,Scale=1.000000)
+AxisMappings=(AxisName="CameraUp",Key=Down,Scale=-1.000000)
+AxisMappings=(AxisName="CameraRight",Key=Right,Scale=1.000000)
+AxisMappings=(AxisName="CameraRight",Key=Left,Scale=-1.000000)
+AxisMappings=(AxisName="MoveForward",Key=W,Scale=1.000000)
+AxisMappings=(AxisName="MoveRight",Key=D,Scale=1.000000)
+AxisMappings=(AxisName="MoveRight",Key=A,Scale=-1.000000)
+AxisMappings=(AxisName="Brake",Key=B,Scale=1.000000)
+AxisMappings=(AxisName="MoveForward",Key=S,Scale=-1.000000)
+AxisMappings=(AxisName="MoveUp",Key=E,Scale=1.000000)
+AxisMappings=(AxisName="MoveUp",Key=Q,Scale=-1.000000)
bAlwaysShowTouchInterface=False
bShowConsoleOnFourFingerTap=True
DefaultTouchInterface=/Engine/MobileResources/HUD/DefaultVirtualJoysticks.DefaultVirtualJoysticks
ConsoleKey=None
-ConsoleKeys=Tilde
+ConsoleKeys=Tilde
```

</details>

### Install poetry  
```sh
curl -sSL https://install.python-poetry.org | python3 -
```
add to PATH permanentaly with
```sh
vi ~/.bashrc
```
then add this to .bashrc file
```sh
export PATH="/home/$USER/.local/bin:$PATH"
```
update poetry
```sh
poetry self update
```
validate installation
```sh
poetry --version
```

### Carla dependency only works with python 3.8
Therefore install [python 3.8](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/?utm_content=cmp-true)

Then run
```sh
poetry env use 3.8
poetry shell
poetry install
```

### Run data collection with

```sh
python -m src.main.generic_nerf_capture
```


edit /experiments to to setup different captures.


# Running on Idun

Running all of this on Idun is actually pretty straight forward.
First, I'll show how to do it manually on a login node,
and then we'll build a SLURM job file to run it on compute nodes.

The key part is that we build Singularity(/Apptainer) images from the Carla/Carlo docker images, and these are quite easy to run.

## Running Carla on Idun

```sh
singularity exec --nv /cluster/apps/dev/carla/carla_latest.sif /home/carla/CarlaUE4.sh -RenderOffScreen
```

## Running Carlo on Idun

Here we first need to build a Docker image, and then a Singularity image. I'm not sure if you can do this on Idun. I did the following steps locally on my laptop, then copied the image to Idun.

```sh
DOCKER_BUILDKIT=1 docker build . -t carlo:latest
docker save -o carlo.tar carlo:latest
apptainer build carlo.sif "docker-archive:$(pwd)/carlo.tar"
# Copy to Idun if you built locally
rsync -avzhP carlo.sif idun:carlo.sif
```

Then, on Idun, we can run Carlo with

```sh
mkdir output
singularity exec --nv --pwd /code carlo.sif python -m src.scripts.idun "$(pwd)/output"
```

## SLURM job file

Write the following to `carla.slurm`:

```sh
#! /usr/bin/bash
#SBATCH --job-name="CarlaSim"
#SBATCH --partition=GPUQ
#SBATCH --account=share-ie-idi
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=1
#SBATCH --array=0-0
#SBATCH --gres=gpu:1

cd ${SLURM_SUBMIT_DIR}
echo "Jobbnummer: ${SLURM_JOB_ID}"
echo "Task-id innad i array: ${SLURM_ARRAY_TASK_ID}"

mkdir worker-${SLURM_ARRAY_TASK_ID}
cd worker-${SLURM_ARRAY_TASK_ID}

export CARLA_PORT=$((57300 + ${SLURM_ARRAY_TASK_ID}))

echo Starting server on port ${CARLA_PORT}
singularity exec --nv /cluster/apps/dev/carla/carla_latest.sif /home/carla/CarlaUE4.sh -RenderOffScreen -carla-rpc-port=$CARLA_PORT &
CARLA_PID=$!

sleep 10
echo Starting client
singularity exec --nv --pwd /code ../carlo.sif python -m src.scripts.idun "$(pwd)"

echo Killing $CARLA_PID
kill $CARLA_PID

echo Bye
```

Then, run it with

```sh
sbatch carla.slurm
```
