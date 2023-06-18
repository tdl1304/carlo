import fnmatch
import json
from pathlib import Path
import sys
import pandas as pd
from IPython.display import display


def read_json_results(json_file: Path):
    """
        Read the json file containing the results of an experiment.
    """
    with open(json_file, "r") as f:
        results = json.load(f)
    return results


def highlight_df(df):
    def highlight_max(s):
        is_max = s == s.max()
        return ['background-color: green' if v else '' for v in is_max]

    def highlight_min(s):
        is_min = s == s.min()
        return ['background-color: red' if v else '' for v in is_min]

    # Apply the highlight function to the 'psnr', 'ssim', and 'lpips' columns
    styled_df = df.style.apply(highlight_max, subset=['psnr', 'ssim', 'lpips'])
    styled_df = styled_df.apply(highlight_min, subset=['psnr', 'ssim', 'lpips'])

    # Display the styled DataFrame
    return styled_df


def highlight_df_in_latex(df):
    def highlight_max(s):
        is_max = s == s.max()
        return ['\\cellcolor{green!25}' if v else '' for v in is_max]

    def highlight_min(s):
        is_min = s == s.min()
        return ['\\cellcolor{red!25}' if v else '' for v in is_min]

    # Apply the highlight function to the 'psnr', 'ssim', and 'lpips' columns
    styled_df = df.style.apply(highlight_max, subset=['psnr', 'ssim', 'lpips'])
    styled_df = styled_df.apply(highlight_min, subset=['psnr', 'ssim', 'lpips'])

    # Display the styled DataFrame
    return styled_df


def save_html_render(styled_df, save_path: Path):
    """
        Save the html render of the styled DataFrame.
    """
    with open(save_path, "w") as f:
        f.write(styled_df.render())

def save_latex_render(styled_df, save_path: Path):
    """
        Save the latex render of the styled DataFrame.
    """
    with open(save_path, "w") as f:
        f.write(styled_df)


def compare_exp_res(exp_path: Path):
    """
        Compare the experimental results from an experiment.
    """
    eval_files = []

    # Loop the exp_path and find all directories
    ignore_dirs = ["images*", "renders", "camera_paths"]
    for exp_dir in exp_path.iterdir():
        if exp_dir.is_dir() and not any(fnmatch.fnmatch(exp_dir.name, ignore_dir) for ignore_dir in ignore_dirs):
            eval_dir = exp_dir
            temp_eval_files = list(eval_dir.glob("**/eval.json"))
            if len(temp_eval_files) == 0:
                print(f"No eval file found in {eval_dir}")
                return

            eval_file = temp_eval_files[0]
            eval_files.append(eval_file)

    json_files = []
    for eval_file in eval_files:
        json_res = read_json_results(eval_file)
        json_obj = {
            "exp_name": json_res["experiment_name"],
            "method_name": json_res["method_name"],
            **json_res["results"]
        }
        json_files.append(json_obj)

    df = pd.DataFrame(json_files)
    sorted_df = df.sort_values(by='exp_name', ascending=True).reset_index(drop=True)
    sorted_df = sorted_df[['psnr', 'ssim', 'lpips']]
    sorted_df.insert(0, "description", sorted_df.index)
    sorted_df = sorted_df.replace("_", "\_", regex=True)

    styled_df = highlight_df(sorted_df)
    styled_df = styled_df.to_latex(
        convert_css=True,
        position_float="centering",
        multicol_align="c",
        hrules=True,
        clines="all;data",
        label=f"tab:{df['exp_name'][0]}",
        caption=f"Results for {df['exp_name'][0]}",
        column_format=f"|l{'|c'*len(sorted_df.columns)}|")

    save_latex_render(styled_df, exp_path / "latex_table.tex")


if __name__ == "__main__":
    arguments = sys.argv[1:]
    exp_path = Path("./runs") / arguments[0]
    compare_exp_res(exp_path)
