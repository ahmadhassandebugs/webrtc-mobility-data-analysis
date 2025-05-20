# Data Analysis and Visualization

Data analysis and plotting scripts for the WebRTC Mobility study.

- PyCharm is highly recommended as an analysis tool
- Add the data folder location to [utils/context.py](./utils/context.py) file
- Do not push code to the main branch. Submit your code as a pull request
- Always use a virtual env to run the scripts. make sure the requirements.txt file is always up to date. don't add versions unless absolutely necessary

## Organization

- All analysis scripts go inside [scripts/analysis](./scripts/analysis)
- All plotting scripts go inside [scripts/plotting](./scripts/plotting)
- The plotting utility functions will be inside [utils/plotting.py](./utils/plotting.py)
- The project context (data folders etc.) info will go inside [utils/context.py](./utils/context.py)

## Index

Scripts and their brief descriptions.

- Numbering is important. Group similar scripts together.
- If an experiment has multiple scripts, use a, b, c,... for the ordering.
- Try to add descriptive names to the scripts. If the script is too long, add a short description in the script name.
- Add a docstring to the script with a brief description of the script and its usage.

### scripts/analysis

- [00a-template-analysis.py](scripts/analysis/00a-template-analysis.py) refers to the template for analysis scripts.


### scripts/plotting

- [00a-template-plotting.py](scripts/plotting/00a-template-plotting.py)
- 