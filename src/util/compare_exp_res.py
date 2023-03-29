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
        return ['background-color: lightgreen' if v else '' for v in is_max]

    def highlight_min(s):
        is_min = s == s.min()
        return ['background-color: red' if v else '' for v in is_min]
    
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


def compare_exp_res(exp_path: Path):
    """
        Compare the experimental results from an experiment.
    """
    eval_files = []

    # Loop the exp_path and find all directories
    for exp_dir in exp_path.iterdir():
        if exp_dir.is_dir():
            eval_dir = exp_dir
            temp_eval_files = list(eval_dir.glob("exp*.json"))
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
    print(sorted_df)

    # Render and save the HTML
    styled_df = highlight_df(sorted_df)
    save_html_render(styled_df, exp_path / "results.html")


if __name__ == "__main__":
    arguments = sys.argv[1:]
    exp_path = Path("./runs") / arguments[0]
    compare_exp_res(exp_path)
