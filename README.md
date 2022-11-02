# Carlo

![credits to Stable Diffusion](media/logo-1.png)

Install requirements first, then run with

```sh
python -m src.scripts.sicko
```

(or for a more pleasant experience)

```sh
python -m src.scripts.camera
```


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
