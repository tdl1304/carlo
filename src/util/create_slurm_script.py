
from src.util.confirm_overwrite import confirm_path_overwrite


def create_slurm_script(carlo_data_dir, input_data_dir, output_dir, experiment_name):
    # Create a slurm script
    slurm_script = f"""#!/usr/bin/bash

#SBATCH --partition=GPUQ
#SBATCH --gres=gpu:A100m40:1
#SBATCH --account=ie-idi
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=32000
#SBATCH --job-name="{experiment_name}"
#SBATCH --output=slurm_logs/carla-{experiment_name}-srun.out
#SBATCH --mail-user=olesto@stud.ntnu.no
#SBATCH --mail-type=ALL

WORKDIR=${{SLURM_SUBMIT_DIR}}

cd ${{WORKDIR}}
echo "we are running from this directory: $WORKDIR"
echo " the name of the job is: $SLURM_JOB_NAME"
echo "The job ID is $SLURM_JOB_ID"
echo "The job was run on these nodes: $SLURM_JOB_NODELIST"
echo "Number of nodes: $SLURM_JOB_NUM_NODES"
echo "We are using $SLURM_CPUS_ON_NODE cores"
echo "We are using $SLURM_CPUS_ON_NODE cores per node"
echo "Total of $SLURM_NTASKS cores"

# Purge modules
module purge

# Deactivate any spill-over environment from the login node
conda deactivate &>/dev/null

conda info
conda activate nerfstudio
conda info

# Run training
./nerf_carla_pipeline.py --model nerfacto --input_data {input_data_dir} --output_dir {output_dir}
    """

    slurm_script_path = carlo_data_dir / f"job.slurm"
    confirm_path_overwrite(slurm_script_path)
    with open(slurm_script_path, "w+") as f:
        f.write(slurm_script)
        print(f"✅ Created slurm script at {carlo_data_dir}")

    return slurm_script