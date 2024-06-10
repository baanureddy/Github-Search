import subprocess

input_filename = "all_repos.txt"
output_filename = "all_repos_output1.txt"
search_file = "pom.xml"

with open(input_filename, "r") as file, open(output_filename, "w") as output_file:
    for line in file:
        repo = line.rstrip()
        command = [
            "gh", "api", "-H", "Accept: application/vnd.github+json",
            "-H", "X-GitHub-Api-Version: 2022-11-28", 
            f"/repos/{repo}/contents/{search_file}"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        
        output_file.write(f"Repository: {repo}\n")
        if result.returncode == 0:
            output_file.write(f"Output:\nsuccess\n")
        else:
            output_file.write(f"Error:\n{result.stderr}\n")
        output_file.write("\n" + "-"*40 + "\n\n")
